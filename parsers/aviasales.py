from datetime import datetime as dt, timedelta as td
from parsers.base import BaseParser
from parsers.requests_retry import requests_retry_session


class AviaSalesParser(BaseParser):
    def _create_url(self, origin_airport, destination_airport, depart_start, depart_end):
        depart_range = (dt.strptime(depart_end, '%Y-%m-%d') - dt.strptime(depart_start, '%Y-%m-%d')).days

        url = 'https://lyssa.aviasales.ru/price_matrix?' \
              'origin_iata={}&destination_iata={}&depart_start={}&depart_range={}&affiliate=true' \
            .format(origin_airport, destination_airport, depart_start, depart_range)
        return url

    def _fetch(self, url):
        _headers = {'origin': 'https://www.aviasales.ru',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
                    'x-compress': 'null',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    'accept': '*/*',
                    'referer': 'https://www.aviasales.ru',
                    'authority': 'lyssa.aviasales.ru'
                    }

        resp = requests_retry_session().get(url=url, headers=_headers)
        return resp

    def _parse_data(self, response, price):
        resp = response.json()
        return sorted([i for i in resp['prices'] if int(i['value']) <= price], key=lambda x: x['value'])


if __name__ == '__main__':
    try:
        a = AviaSalesParser()
        data = a.get_data(origin_airport='LWN',
                          destination_airport='MOW',
                          depart_start='2018-04-23',
                          depart_end='2018-05-01',
                          price=5200)

        print(data)
    except Exception as e:
        print(e)
