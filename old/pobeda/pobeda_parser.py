from collections import namedtuple
from datetime import datetime as dt, timedelta as td
from time import sleep
from lxml import etree

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from helpers.requests_retry import requests_retry_session


Structure = namedtuple('Structure', ['airport_from', 'airport_to', 'date', 'cost'])


def _cheap_tickets(resp_obj):
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
        all_tickets += _cheap_tickets(resp)
        # g.go(url, post=params)
    except BaseException:
        pass

    if return_flight:
        data.update({'city_code_from': aeroport_to, 'city_code_to': aeroport_from})
        resp = requests_retry_session().post(url=url, headers=headers, data=data)
        all_tickets += _cheap_tickets(resp)

    return all_tickets


def airports():
    url = 'https://www.pobeda.aero/SearchWidgetData.json'
    resp = requests_retry_session().get(url).json()
    return [(i,
             resp['stations'][i]['cultures']['en'],
             resp['stations'][i]['cultures']['ru']) for i in resp['stations']]  # [(code, city),]


def destinations(airport_from):
    url = 'https://www.pobeda.aero/SearchWidgetData.json'
    resp = requests_retry_session().get(url).json()
    return [i['TLC'] for i in resp['markets'][airport_from]]

# month parser with selenium -------------------------------------------------


def _month_parser(page_source):
    # Structure = namedtuple('Structure', ['airport_from', 'airport_to', 'date', 'cost'])
    found_tickets = []
    html_parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(page_source, parser=html_parser)
    # city
    _from = ''
    _to = ''
    for item in tree.xpath('//div[@class="path"]'):
        elem = list(item.itertext())
        _from = elem[0]
        _to = elem[1]
        #print(_from, ' | ', _to)

    # tickets
    prev_date = ''
    for item in tree.xpath('//ul/li/div'):
        if item.attrib['data-type'] == 'dayMonth':
            elem = list(item.itertext())
            date = dt.strptime(item.attrib['data-date'], '%Y-%m-%d')
            if prev_date == '' or prev_date < date:
                prev_date = date
                price = elem[5].replace('\xa0', '').strip()
                if price.endswith('руб.'):
                    #print(date, price)
                    found_tickets.append(Structure(_from, _to, date, int(price[:-4])))
            else:
                break
    return found_tickets


def run_webdriver(webdriver_path, city_from, city_to):
    # todo: better logging
    #### settings
    print(city_from,' -> ', city_to)
    found_tickets = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    driver = webdriver.Chrome(executable_path=webdriver_path,
                              chrome_options=chrome_options)
    wait = WebDriverWait(driver, 30)
    driver.get('https://booking.pobeda.aero/ScheduleSelect.aspx')
    sleep(2)

    #### parsing
    # fill in flights form and go to the tickets page
    driver.execute_script('window.scrollTo(0, 0)')
    one_way_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="newSearchWidget"]/div[1]/div[2]/label'))
    step21 = wait.until(one_way_elem, 'one_way form is not found')
    step21.click()
    print('one_way')

    driver.execute_script('window.scrollTo(0, 0)')
    airport_from_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="nameDepartureStation"]'))
    step22 = wait.until(airport_from_elem, 'airport_from form is not found')
    step22.clear()
    step22.send_keys(city_from)
    print('airport_from')

    driver.execute_script('window.scrollTo(0, 0)')
    airport_to_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="newSearchWidget"]/div[1]/div[4]/div[2]/input'))
    step23 = wait.until(airport_to_elem, 'airport_to form is not found')
    step23.clear()
    step23.send_keys(city_to)
    print('airport_to')

    driver.execute_script('window.scrollTo(0, 0)')
    find_button_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="searchButton"]'))
    step24 = wait.until(find_button_elem, 'find_button_elem is not found')
    #step24.sendKeys(Keys.Enter)
    step23.clear()
    step24.click()
    print('find_tickets button')

    # find tickets for next 4 months
    try:
        driver.execute_script('window.scrollTo(0, 0)')
        month_calendar_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="selectMainBody"]/div[5]/div[2]'))
        step31 = wait.until(month_calendar_elem, 'month calendar is not found')
        step31.click()
    except:
        return []
    finally:
        sleep(2)
        print('1st month')

    found_tickets += _month_parser(driver.page_source)

    for i in range(2, 5):
        try:
            driver.execute_script('window.scrollTo(0, 0)')
            second_month_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="carouselMonthContainer1"]/div/div[2]/div/a[2]'))
            step34 = wait.until(second_month_elem, 'next month is not found')
            step34.click()
        except:
            print('{} is already opened'.format(i))
            continue
        finally:
            sleep(2)
            print('{} month'.format(i))
        found_tickets += _month_parser(driver.page_source)

    # close driver
    driver.close()

    return found_tickets


def month_trips():
    # todo: how/where to get this cookie? need to build good userSearchConfiguration row
    from grab import Grab
    g = Grab()
    url = 'https://booking.pobeda.aero/AjaxMonthLowFareAvailaibility.aspx'
    headers = {'Cookie': 'ASP.NET_SessionId=21ct5f2osvv5y2bv1ixw3n1f; \
               CultureCode=%7b%22Value%22%3a%22ru-RU%22%7d; \
               skysales=!Nnf0/LJnRyPnqRB26j6ok5cv2bHz0cdeINHGmEqHIJBCFRJfwAK5n253Fan5AJd7uagOX1WR3QCitE8=; \
               PassengersInfoCookie=%7b%22Value%22%3a%22%22%7d; \
               dtSa=-; \
               userSearchConfiguration=%7B%22From%22%3A%22VKO%22%2C%22InboundDate%22%3A%222017-12-11%22%2C%22To%22%3A%22SGC%22%2C%22OutboundDate%22%3A%222017-12-08%22%2C%22MinADT%22%3A0%2C%22MinCHD%22%3A0%2C%22MinINFT%22%3A0%2C%22SelectedADT%22%3A%221%22%2C%22SelectedCHD%22%3A%220%22%2C%22SelectedINFT%22%3A%220%22%2C%22MaxPax%22%3A0%2C%22TripType%22%3A%22RoundTrip%22%2C%22LinkBooking%22%3Anull%2C%22MinDepartureDate%22%3Anull%2C%22MaxDepartureDate%22%3Anull%2C%22MinArrivalDate%22%3Anull%2C%22MaxArrivalDate%22%3Anull%2C%22Culture%22%3A%22ru%22%2C%22CurrencyCode%22%3A%22RUB%22%2C%22Success%22%3Atrue%2C%22AnyFieldWithData%22%3Afalse%7D; \
               dtPC=3$496961232_348h-vCRDIHUPXBDJPBHJGJILFKIAEOODOHLHSOQ; \
               dtCookie=3$2B3EAF72CD66D7CD233F16EA2C693C8A|RUM+Default+Application|1; \
               rxVisitor=1511890404724BSGLKFH5U7NNCUC0MQG38QMSEJ0S3PV1; \
               rxvt=1512498768913|1512496961238; \
               dtLatC=2; \
               sessionControl=%7B%22ownership%22%3A%7B%22sessionOwnerId%22%3A%22213d9100-e07d-85d5-8342-7bab90906705%22%2C%22sessionOwnerPage%22%3A%22https%3A%2F%2Fbooking.pobeda.aero%2FScheduleSelect.aspx%22%2C%22lastUpdated%22%3A1512497216699%7D%7D'

        , 'Origin': 'https://booking.pobeda.aero'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8'
        , 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        , 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        , 'Accept': '*/*'
        , 'Referer': 'https://booking.pobeda.aero/ScheduleSelect.aspx'
        , 'X-Requested-With': 'XMLHttpRequest'
        , 'Connection': 'keep-alive'
               }
    data = 'indexTrip=1&dateSelected=2017-12-08'

    g.go(url, headers=headers)  # , get=data)
    g.doc.cookies.items()
    """
    [('ASP.NET_SessionId', 'epbjyktiryhop10k3djznz4y'),
     ('CultureCode', '%7b%22Value%22%3a%22ru-RU%22%7d'),
     ('skysales','!WZvl5L969mTSUEF26j6ok5cv2bHz0fPZY2mzH98Nv46Li49EuXw/waLGKP/x74Qlh1ra4dWDFITIElI='),
     ('dtCookie', '3$EC06CA9214B85E48260003E96FA25E3D|RUM+Default+Application|1')]
    """

if __name__ == '__main__':
    # new cheap tickets
    # _tickets = fetch(min_price=1000, max_price=1000, return_flight=True)
    # for t in _tickets:
    #     print(t)

    # all airports
    # _airports = parse_airports()
    # for a in _airports:
    #     print(a)

    # all destinations
    # _destinations = destinations('VKO')
    # for d in _destinations:
    #     print(d)

    path = '/home/achicha/PyProjects/Github/travel/helpers/chromedriver'
    tickets = run_webdriver(path, 'Милан', 'Москва')
    for t in tickets:
        print(t)

