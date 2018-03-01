import requests
url = 'https://lyssa.aviasales.ru/price_matrix?origin_iata=LWN&destination_iata=MOW&depart_start=2018-04-23&depart_range=6&affiliate=true' 

_header = {'origin': 'https://www.aviasales.ru', 
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'x-compress': 'null',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'accept': '*/*',
        'referer': 'https://www.aviasales.ru/search/LWN2404MOW1',
        'authority': 'lyssa.aviasales.ru'
          }

resp = requests.get(url, headers=_header).json()
print(sorted(resp['prices'], key=lambda x:x['value']))
