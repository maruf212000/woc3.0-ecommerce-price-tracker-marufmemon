from selenium import webdriver
import json
import os
import datetime
import time
import sys
import smtplib
from email.message import EmailMessage
sleeptime = 120 # enter number of seconds for time interval cur time is 2 minutes

def create_file():
    link = input("Please enter the product link:- ")
    email = input("Please enter your email id:- ")
    price = input("Please input your desired price:- ")
    data = {
        'starttime' : datetime.datetime.now().timestamp(),
        'link' : link,
        'email' : email,
        'price' : int(price),
        'lastchecktime' : 0
    }
    with open('amazon.json', 'w') as outfile:
        json.dump(data, outfile)
    automating()

def automating():
    with open('amazon.json') as json_file:
        data = json.load(json_file)
    if(data['lastchecktime'] == 0):
        scrapping(data)
    else:
        cur_time = datetime.datetime.now().timestamp()
        time_interval = cur_time - data['lastchecktime']
        if(time_interval > sleeptime):
            scrapping(data)
        else:
            time.sleep(sleeptime - time_interval)
            scrapping(data)

def scrapping(data):
    opts=webdriver.ChromeOptions()
    opts.headless=True
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH,options=opts)
    driver.get(data['link'])
    price = driver.find_element_by_id("priceblock_ourprice")
    try:
        d_price = driver.find_element_by_id("priceblock_dealprice")
        deal_p = ''
        for i in d_price.text:
            if i.isdigit():
                deal_p += i
            if i == '.':
                break
    except:
        deal_p = 100000000000
    cur_price = ''
    for i in price.text:
        if i.isdigit():
            cur_price += i
        if i == '.':
            break
    cur_price = int(cur_price)
    deal_p = int(deal_p)
    if(cur_price > deal_p):
        cur_price = deal_p
    # print(cur_price)
    if(cur_price <= data['price']):
        name_ele = driver.find_element_by_id('productTitle')
        s = name_ele.text
        mailprice(data['link'],s,cur_price,data['email'])
        sys.exit()
    data['lastchecktime'] = datetime.datetime.now().timestamp()
    with open('amazon.json', 'w') as outfile:
        json.dump(data, outfile)
    # print(datetime.datetime.now())
    time.sleep(sleeptime)
    scrapping(data)

def mailprice(link, name, price, email):
    msg = EmailMessage()
    msg['Subject'] = 'Congratulations!!! Product at Low Price'
    msg['From'] = 'YOUR EMAIL ADDRESS'
    msg['To'] = email
    msg.set_content('Product Details \n Name:- ' + name +'\n Price:- ' + price +'\n URL:- ' + link + '\n')

    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('YOUR EMAIL ADDRESS','YOUR EMAIL PASSWORD') #email and password
        smtp.send_message(msg)

# main
if os.path.exists('amazon.json'):
    val = input("Press 0 for old product and 1 for entering new product:- ")
    if(int(val)==0):
        automating()
    else:
        os.remove('amazon.json')
        create_file()
else:
    create_file()