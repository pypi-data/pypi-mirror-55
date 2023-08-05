##system imports##
from sys import argv

##selenium imports##
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##data analysis imports##
import pandas as pd
import numpy as np

## input##
place = argv[1]
if ',' in place:
    place = place.replace(',','%20')
forecast_type = None
if len(argv) == 3:
    forecast_type = argv[2]

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options = options, service_log_path = r'logs.txt')

    driver.get(f"https://weather.com/search/enhancedlocalsearch?where={place}&loctypes=1/4/5/9/11/13/19/21/1000/1001/1003/&from=hdr")

    # wait for DOM to appear
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul>li>a.styles__itemLink__23h5a')))
    
    values = driver.find_elements_by_class_name('styles__itemLink__23h5a')

    options = dict()
    print(f'Available option for {place} are: ')
    for x, y in enumerate(values):
        options[x+1] = y.get_attribute("href")
        print(str(x+1)+' --> ', y.text)
    
    desired_place = int(input("\nEnter your desired choice of place :-> \n"))
    if desired_place in options.keys():
        link = options[desired_place]
    
    def daily():
        driver.get(link)
        print(driver.find_element_by_class_name('today_nowcard-location').text)
        print(driver.find_element_by_class_name(
            'today_nowcard-timestamp').text)
        print(driver.find_element_by_class_name('today_nowcard-temp').text)
        print(driver.find_element_by_class_name('today_nowcard-phrase').text)
        print(driver.find_element_by_class_name('today_nowcard-feels').text)
        print(driver.find_element_by_class_name('today_nowcard-hilo').text)
    
    def hourly():
        driver.get("https://weather.com/weather/hourbyhour/l/" + link[36:])

        hourly_place_title = driver.find_element_by_class_name('hourly-page-title').text
        print(hourly_place_title+'\n')
        m = []
        p = []
        hourly_info_head = driver.find_elements_by_css_selector('.twc-table>thead>tr>th')
        hourly_info = driver.find_elements_by_css_selector('.twc-table>tbody>tr')
        for x in hourly_info_head:
            p.append(x.text)
        p.insert(1, "DAY")
        s = ','.join(p)
        s = s.replace(',', " ")
        m.append(s)
        for y in hourly_info:
            trim = y.text.replace('\n', ' ')
            m.append(trim)
        for i in m:
            print(i)
    
    def five_days():
        driver.get("https://weather.com/weather/5day/l/"+ link[36:])
        five_day_place_title = driver.find_element_by_class_name('five-day-page-title').text
        print(five_day_place_title)
        m = []
        p = []
        five_day_info_head = driver.find_elements_by_css_selector('.twc-table>thead>tr>th')
        five_day_info = driver.find_elements_by_css_selector('.twc-table>tbody>tr')
        for x in five_day_info_head:
            p.append(x.text)
        s = ','.join(p)
        s = s.replace(',', " ")
        m.append(s)
        for y in five_day_info:
            trim = y.text.replace('\n', ' ')
            m.append(trim)
        for i in m:
            print(i)
    
    def ten_days():
        driver.get("https://weather.com/weather/10day/l/"+ link[36:])
        ten_day_place_title = driver.find_element_by_class_name('ten-day-page-title').text
        print(ten_day_place_title)
        m = []
        p = []
        ten_day_info_head = driver.find_elements_by_css_selector('.twc-table>thead>tr>th')
        ten_day_info = driver.find_elements_by_css_selector('.twc-table>tbody>tr')
        for x in ten_day_info_head:
            p.append(x.text)
        s = ','.join(p)
        s = s.replace(',', " ")
        m.append(s)
        for y in ten_day_info:
            trim = y.text.replace('\n', ' ')
            m.append(trim)
        for i in m:
            print(i)
    
    def weekend():
        driver.get("https://weather.com/weather/weekend/l/"+ link[36:])
        weekend_place_title = driver.find_element_by_class_name('weekend-page-title').text
        print(weekend_place_title)
        m = []
        p = []
        table_info = driver.find_element_by_css_selector('#twc-scrollable>div.weather-table>div')
        p = table_info.text.replace('\n',' ')
        m.append(p)
        table = driver.find_elements_by_css_selector('.wx-weather__day')
        for i in table:
            m.append(i.text.replace('\n',' '))
        data = np.array(m)
        df = pd.DataFrame(data)
        print(df.to_string(header=False, index=False))

    def monthly():
        driver.get("https://weather.com/weather/monthly/l/" + link[36:])
        monthly_place_title = driver.find_element_by_class_name('monthly-page-title').text
        print(monthly_place_title)
        monthly_place_days = driver.find_elements_by_css_selector(
            '.forecast-monthly__days>dt')
        monthly_place_date = driver.find_elements_by_css_selector('.date')
        monthly_place_main = driver.find_elements_by_css_selector('.temps>.hi')
        q, r, s = [], [], []
        for x in monthly_place_days:
            q.append(x.text)
        for y in monthly_place_main:
            r.append(y.text)
        for x in monthly_place_date:
            s.append(x.text)
        for i, j in zip(r, s):
            q.append(j+" -> "+i+"F")
        data = np.array(q)
        data = data.reshape(6, 7)
        df = pd.DataFrame(data)
        print(df.to_string(header=False, index=False))
    
    if forecast_type == None or forecast_type == "daily":
        daily()
    elif forecast_type == "hourly":
        hourly()
    elif forecast_type == 'five_days':
        five_days()
    elif forecast_type == 'ten_days':
        ten_days()
    elif forecast_type == 'weekend':
        weekend()
    elif forecast_type == "monthly":
        monthly()

    driver.quit()

except Exception as e:
    print(e)