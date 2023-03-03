#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import xlrd
import csv
import re
import sys
import mysql.connector
import csv
import requests
import random
from requests_toolbelt.adapters import source
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException  


# In[ ]:


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\u2728"
                               u"\uff5e"
                               u"\u2763"
                               u"\ufe0f"
                               u"\U0001f9f6"
                               u"\u2661"
                               u"\U0001f49e"
                               u"\U0001f60d"
                               u"\u2764"
                               u"\U0001f499"
                               u"\U0001f497"
                               u"\U0001f970"
                               u"\U0001f90e"
                               u"\U0001f90d"
                               u"\U0001f496"
                               u"\U0001f929"
                               u"\U0001f97a"
                               u"\u9834"
                               u"\U0001f495"
                               u"\U0001f493"
                               u"\U0001f64f"
                               u"\U0001f3fb"
                               u"\u51c3"
                               u"\u5afa"
                               u"\U0001f49d"
                               u"\U0001f4e6"
                               u"\u4f03"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

    
def save_as_csv(xlsx_file):
    
    csv_file_name=xlsx_file[:-5]+'.csv'
    with open(csv_file_name,'w', newline = "", encoding="big5") as f:
    
        ob = csv.writer(f)
        data = xlrd.open_workbook(xlsx_file).sheet_by_index(0)


        for r in range(data.nrows):
            if r==0:
                HEADER=['ORDER_ID','STATUS','FAIL_REASON','RETURN_STATUS','CUSTOMER_ID','EFFDT','PRODUCT_GROSS','CUSTOMER_SHIP_FEE','SHOPEE_SHIP_FEE','RETURN_SHIP_FEE','TOTAL_PAID','SHOPEE_SUBSIDY','SHOPEE_REDEEM','CREDIT_DISCOUNT','DISCOUNT_CODE','CUSTOMER_COUPON','CUSTOMER_GIVEBACK','SHOPEE_COUPON','TRANSCATION_FEE','SERVICE_FEE','CASHFLOW_FEE','INSTALLMENTS','CREDIT_CHARGE','MAIN_COMMODITY_NM','SUB_COMMODITY_NM','ORG_PRICE','DIS_PRICE','MAIN_COMMODITY_ID','SUB_COMMODITY_ID','COUNT','PROMOTION_METRIC','SHOPEE_PROMOTION','RECIPIENT_ADDR','RECIPIENT_PHONE','PICKUP_STORE_ID','CITY','DISTRICT','POSTAL','RECIPIENT_NAME','SHIPPING_TYPE','DELIVER_TYPE','PREPARE_TIME','PAYMENT_TYPE','LAST_SHIP_TIME','SHIIPPING_CODE','CUSTOMER_PAID_TIME','ACTUAL_SHIP_TIME','ORDER_COMPLETE_TIME','CUSTOMER_COMMENT','COMMENT']
                ob.writerow(HEADER)
            else:     
                temp=[]
                for i in range(0,len(data.row_values(r))):

                    text=data.cell(rowx=r,colx=i).value
                    text=str(text)
                    text=remove_emoji(text)
                    temp.append(text)
                ob.writerow(temp)   
                
def insert_to_ORDERS(csv_file):
    file = open(csv_file)
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    rows = []
    count=0
    mydb = mysql.connector.connect(
      host="aws-florine.ciyg45dcrwqw.us-west-2.rds.amazonaws.com",
      user="admin",
      password="Rainbow0612",
      database="AWS_FLORINE_DEV"
    )
    mycursor = mydb.cursor()
    for row in csvreader:
       
        rows.append(row) 
        #sql = "INSERT INTO ORDERS (ORDER_ID,STATUS,FAIL_REASON,RETURN_STATUS,CUSTOMER_ID,EFFDT,PRODUCT_GROSS,CUSTOMER_SHIP_FEE,SHOPEE_SHIP_FEE,RETURN_SHIP_FEE,TOTAL_PAID,SHOPEE_SUBSIDY,SHOPEE_REDEEM,CREDIT_DISCOUNT,DISCOUNT_CODE,CUSTOMER_COUPON,CUSTOMER_GIVEBACK,SHOPEE_COUPON,TRANSCATION_FEE,SERVICE_FEE,CASHFLOW_FEE,INSTALLMENTS,CREDIT_CHARGE,MAIN_COMMODITY_NM,SUB_COMMODITY_NM,ORG_PRICE,DIS_PRICE,MAIN_COMMODITY_ID,SUB_COMMODITY_ID,COUNT,PROMOTION_METRIC,SHOPEE_PROMOTION,RECIPIENT_ADDR,RECIPIENT_PHONE,PICKUP_STORE_ID,CITY,DISTRICT,POSTAL,RECIPIENT_NAME,SHIPPING_TYPE,DELIVER_TYPE,PREPARE_TIME,PAYMENT_TYPE,LAST_SHIP_TIME,SHIIPPING_CODE,CUSTOMER_PAID_TIME,ACTUAL_SHIP_TIME,ORDER_COMPLETE_TIME,CUSTOMER_COMMENT,COMMENT) VALUES (%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s)"
        #val = row
        #mycursor.execute(sql, val)
        count+=1
    sql = "INSERT INTO ORDERS (ORDER_ID,STATUS,FAIL_REASON,RETURN_STATUS,CUSTOMER_ID,EFFDT,PRODUCT_GROSS,CUSTOMER_SHIP_FEE,SHOPEE_SHIP_FEE,RETURN_SHIP_FEE,TOTAL_PAID,SHOPEE_SUBSIDY,SHOPEE_REDEEM,CREDIT_DISCOUNT,DISCOUNT_CODE,CUSTOMER_COUPON,CUSTOMER_GIVEBACK,SHOPEE_COUPON,TRANSCATION_FEE,SERVICE_FEE,CASHFLOW_FEE,INSTALLMENTS,CREDIT_CHARGE,MAIN_COMMODITY_NM,SUB_COMMODITY_NM,ORG_PRICE,DIS_PRICE,MAIN_COMMODITY_ID,SUB_COMMODITY_ID,COUNT,PROMOTION_METRIC,SHOPEE_PROMOTION,RECIPIENT_ADDR,RECIPIENT_PHONE,PICKUP_STORE_ID,CITY,DISTRICT,POSTAL,RECIPIENT_NAME,SHIPPING_TYPE,DELIVER_TYPE,PREPARE_TIME,PAYMENT_TYPE,LAST_SHIP_TIME,SHIIPPING_CODE,CUSTOMER_PAID_TIME,ACTUAL_SHIP_TIME,ORDER_COMPLETE_TIME,CUSTOMER_COMMENT,COMMENT) VALUES (%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s)"
    val = rows
    mycursor.executemany(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()
    print(count, " record inserted.")


# In[ ]:



dir_file_name='Order.all.20220701_20220731'
csv_string=dir_file_name+'.csv'
xlsx_string=dir_file_name+'.xlsx'
save_as_csv(xlsx_string)
insert_to_ORDERS(csv_string)
df = pd.DataFrame(pd.read_csv(csv_string, encoding="big5"))
  
    


# In[ ]:


def get_product_total_page(url):
    #今天講個特別的，我們可以不讓瀏覽器執行在前景，而是在背景執行（不讓我們肉眼看得見）
    #如以下宣告 options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')



    #打開瀏覽器,確保你已經有chromedriver在你的目錄下
    # 然後將options加入Chrome方法裡面，至於driver請用executable_path宣告進入
    browser=webdriver.Chrome(options=options, executable_path='./chromedriver')
    browser.get(url)
    #browser.get("https://shopee.tw/florine__20#product_list")

    time.sleep(5)
    total_page_html=browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div[2]/div/span[2]")
    total_page=total_page_html.text.strip()
    
    return total_page

def check_exists_by_xpath(xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def get_emoji_list(total_page):
    product_list=[]
    for i in range(int(total_page)):
    #今天講個特別的，我們可以不讓瀏覽器執行在前景，而是在背景執行（不讓我們肉眼看得見）
    #如以下宣告 options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')



    #打開瀏覽器,確保你已經有chromedriver在你的目錄下
    # 然後將options加入Chrome方法裡面，至於driver請用executable_path宣告進入
    browser=webdriver.Chrome(options=options, executable_path='./chromedriver')
    page_url="https://shopee.tw/florine__20?page="+str(i)
    browser.get(page_url)
    time.sleep(5)
    for j in range(1,31):
        product_name_xpath="/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/div["+str(j)+"]/a/div/div/div[2]/div[1]/div/div"
        if check_exists_by_xpath(product_name_xpath)==True:
            product_name_html=browser.find_element_by_xpath(product_name_xpath)
            product_name=product_name_html.text.strip()
            product_list.append(product_name)
    browser.quit()
    
    return product_list


# In[ ]:


len(product_list)


# In[ ]:


product_list


# In[ ]:


## Main Function ##
def CJK_cleaner(string):
    #Keep CJS Characters, Latin Letters and Digits (listed above)
    filters = re.compile(u'[^0-9a-zA-Z\u0083\u008a\u008c\u008e\u009a\u009c\u009e\u009f\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff\u0100-\u017f\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\u3130-\u318f\uff00-\uffef\u00A0\u0020\u3000]+', re.UNICODE)
    return filters.sub('?', string) #remove special characters
#------
CJK_cleaner("自留款💝設計感露後腰綁帶套裝\U0001f90d短版上衣 T恤 棉質休閒喇叭長褲 2022夏季")

