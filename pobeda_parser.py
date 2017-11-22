from datetime import datetime as dt, timedelta as td
from grab import Grab


def fetch(min_price=2000, max_price=2000, aeroport_from='VKO', aeroport_to='', return_flight=False):
    """get all cheapest flights from pobeda.aero"""

    # constant parameters
    found_flights = []

    url = 'https://www.pobeda.aero/information/book/search_cheap_tickets'
    params = {
        'Accept': '*/*'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        , 'Connection': 'keep-alive'
        , 'Content-Length': 209
        , 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        # ,'Cookie':'geobase=a%3A2%3A%7Bs%3A4%3A%22city%22%3Bs%3A12%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%3Bs%3A16%3A%22member_city_iata%22%3Bs%3A3%3A%22VKO%22%3B%7D; _ym_uid=1506177868902209905; _gat=1; _gat_UA-56206873-1=1; _ym_isad=2; _ga=GA1.2.829744325.1506177868; _gid=GA1.2.1987493675.1510230597; userSearchConfiguration=%7B%22MinADT%22%3A0%2C%22MinCHD%22%3A0%2C%22MinINFT%22%3A0%2C%22MaxPax%22%3A0%2C%22LinkBooking%22%3Anull%2C%22MinDepartureDate%22%3Anull%2C%22MaxDepartureDate%22%3Anull%2C%22MinArrivalDate%22%3Anull%2C%22MaxArrivalDate%22%3Anull%2C%22Success%22%3Atrue%2C%22AnyFieldWithData%22%3Afalse%2C%22From%22%3A%22VKO%22%2C%22InboundDate%22%3A%222017-11-15%22%2C%22To%22%3A%22SGC%22%2C%22OutboundDate%22%3A%222017-11-12%22%2C%22SelectedADT%22%3A%221%22%2C%22SelectedCHD%22%3A%220%22%2C%22SelectedINFT%22%3A%220%22%2C%22TripType%22%3A%22RoundTrip%22%2C%22Culture%22%3A%22ru%22%2C%22CurrencyCode%22%3A%22RUB%22%7D; _ym_visorc_26844807=w; tmr_detect=0%7C1510230624679'
        , 'Host': 'www.pobeda.aero'
        , 'Origin': 'https://www.pobeda.aero'
        , 'Referer': 'https://www.pobeda.aero/information/book/search_cheap_tickets'
        ,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        , 'X-Compress': 'null'
        , 'X-Requested-With': 'XMLHttpRequest'
        # xml params
        , 'search_tickets': 1
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
    g = Grab()
    g.go(url, post=params)
    for i in g.doc.select('//ul[@class="airtickets"]//div[@class="airtickets-item__holder"]'):
        found_flights.append(i.text())

    # find return ticket if need so.
    if return_flight:
        params.update({'city_code_from': aeroport_to, 'city_code_to': aeroport_from})
        g.go(url, post=params)
        for i in g.doc.select('//ul[@class="airtickets"]//div[@class="airtickets-item__holder"]'):
            found_flights.append(i.text())

    return found_flights

# testing
tickets = fetch(return_flight=True)
for t in tickets:
    print(t)
