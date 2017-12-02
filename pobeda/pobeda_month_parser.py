# from selenium import webdriver
from time import sleep
from lxml import etree
from datetime import datetime as dt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# todo: remove this depricated file
def page_parser(page_source):
    html_parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(page_source, parser=html_parser)
    # city
    for item in tree.xpath('//div[@class="path"]'):
        elem = list(item.itertext())
        _from = elem[0]
        _to = elem[1]
        print(_from, ' | ', _to)

    # tickets
    prev_date = ''
    for item in tree.xpath('//ul/li/div'):
        if item.attrib['data-type'] == 'dayMonth':
            elem = list(item.itertext())
            date = dt.strptime(item.attrib['data-date'], '%Y-%m-%d')
            if prev_date == '' or prev_date < date:
                prev_date = date
                price = elem[5].replace('\\xa', '').strip()
                if price.endswith('руб.'):
                    print(date, price)
            else:
                break


def run_webdriver(webdriver_path):
    #### settings
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    driver = webdriver.Chrome(executable_path=webdriver_path,
                              chrome_options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get('https://booking.pobeda.aero/ScheduleSelect.aspx')

    #### parsing
    # fill in flights form and go to the tickets page
    one_way_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="newSearchWidget"]/div[1]/div[2]/label'))
    step21 = wait.until(one_way_elem, 'one_way form is not found')
    step21.click()
    print('one_way')

    airport_from_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="nameDepartureStation"]'))
    step22 = wait.until(airport_from_elem, 'airport_from form is not found')
    step22.clear()
    step22.send_keys('Милан')
    # step22.send_keys(Keys.ENTER)
    print('airport_from')

    airport_to_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="newSearchWidget"]/div[1]/div[4]/div[2]/input'))
    step23 = wait.until(airport_to_elem, 'airport_to form is not found')
    step23.clear()
    step23.send_keys('Сочи')
    # step23.send_keys(Keys.ENTER)
    print('airport_to')

    find_button_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="searchButton"]'))
    step24 = wait.until(find_button_elem, 'find_button_elem is not found')
    step24.click()
    print('click find')

    # find tickets
    month_calendar_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="selectMainBody"]/div[5]/div[2]'))
    step31 = wait.until(month_calendar_elem, 'month calendar is not found')
    step31.click()
    sleep(2)
    print('1st month')
    page_parser(driver.page_source)     # find tickets on this page

    # go to the next month's page
    second_month_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="carouselMonthContainer1"]/div/div[2]/div/a[2]'))
    step34 = wait.until(second_month_elem, 'next month is not found')
    step34.click()
    sleep(2)
    print('2nd month')
    page_parser(driver.page_source)

    third_month_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="carouselMonthContainer1"]/div/div[2]/div/a[2]'))
    step35 = wait.until(third_month_elem, 'next month is not found')
    step35.click()
    sleep(2)
    print('3rd month')
    page_parser(driver.page_source)

    forth_month_elem = EC.presence_of_element_located((By.XPATH, '//*[@id="carouselMonthContainer1"]/div/div[2]/div/a[2]'))
    step36 = wait.until(forth_month_elem, 'next month is not found')
    step36.click()
    sleep(2)
    print('4th month')
    page_parser(driver.page_source)

    # close driver
    driver.close()


if __name__ == '__main__':
    path = '/home/achicha/PyProjects/Github/travel/helpers/chromedriver'
    run_webdriver(path)
