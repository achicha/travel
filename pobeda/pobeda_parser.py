from collections import namedtuple
from datetime import datetime as dt, timedelta as td

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from lxml import etree

Structure = namedtuple('Structure', ['flight_from', 'flight_to', 'date', 'cost'])


def parse(resp_obj):
    """
        parse HTML
    :param resp_obj:
    :return: list
    """
    found_tickets = []
    myparser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(resp_obj.content, parser=myparser)
    for li in tree.xpath('//ul[@class="airtickets"]/li[@class="airtickets-item clearfix"]'):
        _from = ''
        _to = ''
        _date = ''
        _cost = ''
        for item in li.xpath('//div'):
            if item.get('class') == 'airtickets-cities':
                elem = list(item.itertext())
                _from = elem[0]
                _to = elem[1]
            elif item.get('class') == 'airtickets-cost':
                _cost = item.text.strip().replace(' ', '')
            elif item.get('class') == 'airtickets-date':
                _date = item.text.strip()
            elif item.get('class') == 'airtickets-buy__wrapper':
                found_tickets.append(Structure(_from, _to, _date, _cost))
    return found_tickets


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
):
    """
        create session with retry
    :param retries: total retries
    :param backoff_factor:
    :param status_forcelist: 5xx statuses will retry
    :param session:
    :return:
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def fetch(min_price=800, max_price=800, aeroport_from='VKO', aeroport_to='', return_flight=False):
    """get all cheapest flights from pobeda.aero"""

    # constant parameters
    url = 'https://www.pobeda.aero/information/book/search_cheap_tickets'
    headers = {
        'Accept': '*/*'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        , 'Connection': 'keep-alive'
        , 'Content-Length': '209'
        , 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        # ,'Cookie':'geobase=a%3A2%3A%7Bs%3A4%3A%22city%22%3Bs%3A12%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%3Bs%3A16%3A%22member_city_iata%22%3Bs%3A3%3A%22VKO%22%3B%7D; _ym_uid=1506177868902209905; _gat=1; _gat_UA-56206873-1=1; _ym_isad=2; _ga=GA1.2.829744325.1506177868; _gid=GA1.2.1987493675.1510230597; userSearchConfiguration=%7B%22MinADT%22%3A0%2C%22MinCHD%22%3A0%2C%22MinINFT%22%3A0%2C%22MaxPax%22%3A0%2C%22LinkBooking%22%3Anull%2C%22MinDepartureDate%22%3Anull%2C%22MaxDepartureDate%22%3Anull%2C%22MinArrivalDate%22%3Anull%2C%22MaxArrivalDate%22%3Anull%2C%22Success%22%3Atrue%2C%22AnyFieldWithData%22%3Afalse%2C%22From%22%3A%22VKO%22%2C%22InboundDate%22%3A%222017-11-15%22%2C%22To%22%3A%22SGC%22%2C%22OutboundDate%22%3A%222017-11-12%22%2C%22SelectedADT%22%3A%221%22%2C%22SelectedCHD%22%3A%220%22%2C%22SelectedINFT%22%3A%220%22%2C%22TripType%22%3A%22RoundTrip%22%2C%22Culture%22%3A%22ru%22%2C%22CurrencyCode%22%3A%22RUB%22%7D; _ym_visorc_26844807=w; tmr_detect=0%7C1510230624679'
        , 'Host': 'www.pobeda.aero'
        , 'Origin': 'https://www.pobeda.aero'
        , 'Referer': 'https://www.pobeda.aero/information/book/search_cheap_tickets'
        ,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        , 'X-Compress': 'null'
        , 'X-Requested-With': 'XMLHttpRequest'
    }
    # xml params
    data = {'search_tickets': 1
        , 'city_code_from': aeroport_from  # from Moscow
        , 'city_code_to': aeroport_to
        , 'date_departure_from': dt.now().strftime('%d/%m/%Y')
        , 'date_departure_to': (dt.now() + td(180)).strftime('%d/%m/%Y')
        , 'date_return_from': dt.now().strftime('%d/%m/%Y')
        , 'date_return_to': (dt.now() + td(180)).strftime('%d/%m/%Y')
        , 'min_price': min_price
        , 'max_price': max_price
            }

    # find tickets
    all_tickets = []
    try:
        resp = requests_retry_session().post(url=url, headers=headers, data=data)
        all_tickets += parse(resp)
        # g.go(url, post=params)
    except BaseException:
        pass

    if return_flight:
        data.update({'city_code_from': aeroport_to, 'city_code_to': aeroport_from})
        resp = requests_retry_session().post(url=url, headers=headers, data=data)
        all_tickets += parse(resp)

    return all_tickets


if __name__ == '__main__':
    # testing
    tickets = fetch(min_price=1000, max_price=1000, return_flight=True)
    for t in tickets:
        print(t)
