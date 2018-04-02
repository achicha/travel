from lxml import etree, html
from datetime import datetime as dt, timedelta as td
from parsers.base import BaseParser
from parsers.msg_sender import requests_retry_session
from pprint import pprint


class AviobiletParser(BaseParser):
    def _create_url(self, origin_airport, destination_airport, depart_start=None, depart_end=None):
        url = 'https://aviobilet.com/routeInline.php?lang=ru&from={}&to={}&su=' \
            .format(origin_airport, destination_airport)
        return url

    def _fetch(self, url):
        base_url = 'https://aviobilet.com'
        _headers = {'Accept-Encoding': 'gzip, deflate, br'
                    , 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8'
                    , 'X-Compress': 'null'
                    , 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                    , 'Accept': 'application/json, text/javascript, */*; q=0.01'
                    , 'Referer': base_url
                    , 'X-Requested-With': 'XMLHttpRequest'
                    , 'Connection': 'keep-alive'
                    }
        # get cookie
        resp1 = requests_retry_session().get(base_url, headers=_headers)
        _cookies = resp1.cookies.get_dict()
        # add cookie
        _headers['Cookie'] = '; '.join(['{}={}'.format(k, v) for k, v in _cookies.items()])
        # download data
        resp = requests_retry_session().get(url=url, headers=_headers)
        return resp

    def _parse_data(self, response, origin_airport, destination_airport, depart_start, depart_end, price=None):
        """
           Get data from response
        :param response: response
        :param origin_airport:
        :param destination_airport:
        :param price: maximum ticket price for filtering out
        :return: data
        """
        my_parser = etree.HTMLParser(encoding="utf-8")
        tree = etree.HTML(response.content, parser=my_parser)
        filtered_by_price = []
        for item in tree.xpath('//div[@class="SortItem1"]'):
            ticket = {}
            airport = ''

            # find all divs
            lst = []
            for el in item:
                # print(el.attrib)
                lst.append(el)
                lst += [i for i in el.findall('div')]
                for j in el:
                    lst += [i for i in j.findall('div')]

            # find all elements in divs
            for el in lst:
                if 'href' in el.attrib:
                    ticket['link'] = 'https://aviobilet.com' + el.attrib['href']
                if el.get('class') == 'TicketListPrice_v2':
                    ticket['value'] = int(''.join(list(el.itertext())[1:-1]).replace(' ', ''))
                if el.get('class') == 'TicketCityTitle':
                    dest = el.text.strip()

                    if 'SVO' in dest:
                        airport = 'SVO'
                    elif 'DME' in dest:
                        airport = 'DME'
                    ticket['origin_airport'] = airport or origin_airport
                    ticket['destination_airport'] = destination_airport
                if el.get('class') == 'TicketListData':
                    time = dt.strptime(''.join(list(el.itertext())[1:]).split('-')[0].strip(), '%d.%m.%Y / %H:%M')
                    ticket['depart_date'] = time
                    ticket['resource'] = 'aviobilet'
                    ticket['number_of_changes'] = 0
                    ticket['gate'] = 'non'

            # add ticket filtered by price and date range
            if ticket and ticket['value'] <= price and dt.strptime(depart_start, '%Y-%m-%d') <= \
                    ticket['depart_date'] <= dt.strptime(depart_end, '%Y-%m-%d'):
                    filtered_by_price.append(ticket)
            airport = ''

        return filtered_by_price


if __name__ == '__main__':
    try:
        a = AviobiletParser()
        data = a.get_data(origin_airport='MOW',
                          destination_airport='BOJ',
                          depart_start=None,
                          depart_end=None,
                          price=10000)

        pprint(data)
    except Exception as e:
        print(e)
