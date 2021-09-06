from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import socket
import time
import json
import datetime 
from fake_useragent import UserAgent

#########SISTEMARE LINGUA INGLESE PURE QUAAAAAAAAAAAAAAA

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
driver = webdriver.Chrome(chrome_options=chrome_options)
ua=UserAgent()
userAgent=ua.random
print(userAgent)
chrome_options.add_argument(f'user-agent={userAgent}')

HOST=os.getenv("HOST_LOGSTASH")
PORT=os.getenv("PORT_LOGSTASH")
CODE_PRODUCT=os.getenv("CODE_PRODUCT")
MINUTES_TO_WAIT=int(os.getenv("MINUTES_TO_WAIT"))
REQUIRED_CHARACTER="\n" #### REQUIRED FOR LOGSTASH TO TAKE EVENT SEPARATED (TCP PLUGIN)
DOMAIN_URL=os.getenv("DOMAIN_URL")

months={}
if DOMAIN_URL=='it':
    months={'gennaio':'01','febbraio':'02','marzo':'03','aprile':'04','maggio':'05','giugno':'06','luglio':'07','agosto':'08','settembre':'09','ottobre':'10','novembre':'11','dicembre':'12'}
else:
    months={'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}



error=True
while(error):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, int(PORT)))
        
        sock.close()
        error = False
    except:
        print("ERROR:")
        print('Connection error. There will be a new attempt in 5 seconds\n')
        time.sleep(5)

##ESTABLISH CONNECTION TO LOGSTASH
s=socket.socket()
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, int(PORT)))

print("STREAM CONNESSO")


def confronting_date(date,today):
    if date[0]==today[-1] and months[date[1]]==today[1] and date[2]==today[0]:
        return True
    return False

def get_reviews_stream(html,last_item):


    reviews = soup.find_all('div',{'data-hook':'review'})
    first_new=True
    last_item_new=None
    for item in reviews:
        ####print(last_item)
        try:
            body=item.find('span', {'data-hook': 'review-body'}).text.strip()
        except Exception as e:
            print(e)
        #print(body)
        

        try:
            date=item.find('span',{'data-hook':'review-date'}).text.strip()
            country=" ".join(date.split(" ")[2:-4])
            date=date.split(" ")[-3:]
            
            today=str(datetime.datetime.now()).split(" ")[0].split("-")
           
            if last_item is None:# and confronting_date(date,today):
                print("ok modified")
                last_item=body
                
        except Exception as e:
            print(e)

        if  body==last_item:
            print("break")
            print(last_item)
            break

        if last_item is not None and confronting_date(date,today) and last_item!=body:
            print("nuova recensione")
            if first_new:
                last_item_new=body ## nuovo primo elemento
                first_new=False
                #print("dovrei modificare last item")
            #print("send()... ")
            ###
            title,rating,body,date,name,helpful_vote,verified_buy,country="","","","","","","",""
            try:
                title=item.find('a', {'data-hook': 'review-title'}).text.strip()
            except Exception as e:
                title=item.find('span', {'data-hook': 'review-title'}).text.strip()
                print(e)

            try:
                rating=item.find('span', {'class': 'a-icon-alt'}).text[:1].strip()
            except Exception as e:
                print(e)

            try:
                body=item.find('span', {'data-hook': 'review-body'}).text.strip()
            except Exception as e:
                print(e)

            try:
                date=item.find('span',{'data-hook':'review-date'}).text.strip()
                country=" ".join(date.split(" ")[2:-4])
                date=" ".join(date.split(" ")[-3:])
                lst=date.split(" ")
                if int(lst[0])<10:
                    date=lst[2]+"-"+months[lst[1].lower()]+"-0" +lst[0]
                else:
                    date=lst[2]+"-"+months[lst[1].lower()]+"-" +lst[0]
                
            except Exception as e:
                print(e)

            try:
                name=item.find('span',{'class':'a-profile-name'}).text.strip()
            except Exception as e:
                print(e)

            try:
                verified_buy=item.find('span',{'data-hook':'avp-badge'}).text.strip()
            except Exception as e:
                verified_buy="NO"
                print(e)
            
            try:
                helpful_vote=item.find('span',{'data-hook':'helpful-vote-statement'}).text.strip().split(" ")[0].replace(",","")
                if helpful_vote.lower()=='una' or helpful_vote.lower()=='one':
                    helpful_vote=1
            except Exception as e:
                helpful_vote=0
                print(e)
            ###
            review = {
                'title': title,
                'rating': rating,
                'body': body,
                'date': date,
                'name':name,
                'verified_buy':verified_buy,
                'helpful_vote': helpful_vote,
                'country':country
            }
            print(review)
            s.send(json.dumps(review).encode())
            s.send(bytes(REQUIRED_CHARACTER,'utf-8'))
            time.sleep(1)

        if  body==last_item:
            print("break")
            print(last_item)
            break
        


    if last_item_new is not None:
        last_item=last_item_new
    
    return last_item





   
    
#driver.get("https://www.amazon.it/product-reviews/"+ str(CODE_PRODUCT) +"/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i))
date=datetime.datetime.now() #.year .month .day
url="https://www.amazon."+str(DOMAIN_URL)+"/product-reviews/"+ str(CODE_PRODUCT) +"/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"
    

last_item=None

while True:
     ##OGNI 5 MINUTI
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    last_item=get_reviews_stream(soup,last_item)
    print("wait",flush=True)
    
    time.sleep(MINUTES_TO_WAIT*60)