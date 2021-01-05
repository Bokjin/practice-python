
import time
import csv
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl import load_workbook

path = "C:\\Users\\Admin\\Desktop\\python\\hypoxia\\국립수산과학원\\chromedriver.exe"
today = datetime.today().strftime('%Y-%m-%d')
browser = webdriver.Chrome(path)
browser.maximize_window()
browser.get('http://www.nifs.go.kr/femo/data_obs.femo')

# 진해만 선택
Jinhae_select = browser.find_element_by_xpath('//*[@id="fishery"]/option[text()="진해만"]').click()

# 관측 일자 선택

browser.find_element_by_id("sea_obs_from").send_keys("2000-01-01")
browser.find_element_by_id("sea_obs_to").send_keys(today)

# 데이터 검색

browser.find_element_by_xpath('//*[@id="contents"]/div[2]/div[2]/div[2]/div/section/div[2]/div[1]/div[1]/div/div[2]/a').click()
time.sleep(2) ## 로딩 대기

# 50개로 보기
browser.find_element_by_xpath('//*[@id="div_page_sea_center"]/table/tbody/tr/td[8]/select/option[text()="50"]').click()

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
tables = pd.read_html(html)
column = pd.DataFrame(tables[0])


total_page_number = browser.find_elements_by_id('sp_1_div_page_sea')

for i in total_page_number :
    last_page = int(i.text)+ 1  ## 36

data_list = []


Number = 1
curr_page = 1
id_number = 0
while curr_page < last_page:
    try:

        if Number < 51 :
            elem = browser.find_element_by_xpath(f'//*[@id="{Number}"]')
            raw_text = elem.text
            text = raw_text.replace("  "," -")
            text_list = text.split(" ")
            data_list.append(text_list)


            Number += 1

        elif Number == 51 :
            Number = 1
            browser.find_element_by_class_name('ui-pg-input').clear()
            page_input = browser.find_element_by_class_name('ui-pg-input')
            page_input.click()
            page_input.send_keys(curr_page + 1)
            page_input.send_keys(Keys.ENTER)

            curr_page += 1

            #if curr_page  == last_page :
                #print("마지막 페이지 입니다.")
    except NoSuchElementException:
        if Number < 50 :
            print("완료됐습니다.")
            break
        else :
            print("오류를 확인해주세요.")
            break
        

excel_data = pd.DataFrame(data_list)
#columns.to_excel(excel_writer='연습_1.xlsx',index = False, encoding='cp949')
#excel_data.columns =[columns]
column.to_csv('진해만_어장.csv',mode = "w",encoding='cp949')
excel_data.to_csv("진해만_어장.csv", mode='a', header=False,encoding='cp949')
#excel_data.to_csv(excel_writer='진해만_raw_data.csv',encoding='euc-kr')
#print("excel 저장 완료 : 5초뒤 자동 종료됩니다.")
#time_pd.to_csv("filename.csv", mode='w')
time.sleep(5)
browser.quit()
        