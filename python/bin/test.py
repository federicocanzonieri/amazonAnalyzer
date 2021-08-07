from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import socket
import time
import json
import datetime 


s=socket.socket()
HOST="10.0.100.2"
PORT=6000
REQUIRED_CHARACTER="\n" #### REQUIRED FOR LOGSTASH TO TAKE EVENT SEPARATED (TCP PLUGIN)



months={'gennaio':'01','febbraio':'02','marzo':'03','aprile':'04','maggio':'05','giugno':'06','luglio':'07','agosto':'08','settembre':'09','ottobre':'10','novembre':'11','dicembre':'12'}

def confronting_date(date,today):
    if date[0]==today[-1] and months[date[1]]==today[1] and date[2]==today[0]:
        return True
    return False

def get_reviews_stream(html,last_item):


    reviews = soup.find_all('div',{'data-hook':'review'})
    first_new=True
    last_item_new=None
    for item in reviews:
        try:
            body=item.find('span', {'data-hook': 'review-body'}).text.strip()
        except Exception as e:
            print(e)
        



        ###quando leggo nuovi item last_item is not None ad confronting date (oggi!) last_item!=current body

       
        

        try:
            date=item.find('span',{'data-hook':'review-date'}).text.strip()
            country=" ".join(date.split(" ")[2:-4])
            date=date.split(" ")[-3:]
            #print("Date:",date)
            today=str(datetime.datetime.now()).split(" ")[0].split("-")
           # print("Datetime:",today)
            if last_item is None and confronting_date(date,today):
                print("oook")
                last_item=body
                #last_item.update(body)
        except Exception as e:
            print(e)


        if last_item is not None and confronting_date(date,today) and last_item!=body:
            print("nuova recensione")
            if first_new:
                last_item_new=body ## nuovo primo elemento
                first_new=False
                print("dovrei modificare last item")
            print("send()... ",body)


        if  body==last_item:
            print("breaaaak")
            print(last_item)
            break
        


    if last_item_new is not None:
        last_item=last_item_new
    
    return last_item







chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
driver = webdriver.Chrome(chrome_options=chrome_options)
   
    
    #driver.get("https://www.amazon.it/product-reviews/"+ str(CODE_PRODUCT) +"/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i))
   
    
date=datetime.datetime.now() #.year .month .day
url="https://www.amazon.it/amazon-echo-dot-3-generazione-altoparlante-intelligente-con-integrazione-alexa-tessuto-antracite/product-reviews/B07PHPXHQS/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"
last_item=None
while True:
    time.sleep(60*5) ##OGNI 5 MINUTI
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    last_item=get_reviews_stream(soup,last_item)
    print("ereras")