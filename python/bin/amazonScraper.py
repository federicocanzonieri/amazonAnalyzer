from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import socket
import time
import json
import requests
from fake_useragent import UserAgent


###FUNCTION TO RETRIEVE REVIEWS AND OTHER DATA
def get_reviews(soup,s):
    
    
    print("START GENERAL")
    reviews = soup.find_all('div',{'data-hook':'review'})
    for item in reviews:
        
       
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
            if helpful_vote.lower()=='una' or helpful_vote.lower()=='one' :
                helpful_vote=1
            
        except Exception as e:
            helpful_vote=0
            print(e)
        

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
        if DEBUG=='yes':
            print(review)
            
        s.send(json.dumps(review).encode())
        s.send(bytes(REQUIRED_CHARACTER,'utf-8'))
        time.sleep(int(TIMEOUT_BEFORE_SEND_TO_LOGSTASH))
        print(title)

    print("END GENERAL",flush=True)



#https://m.media-amazon.com/images/I/81SiQ9hXnDL._AC_SX679_.jpg
def get_photos(url):
    print(url)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    img_container=soup.find_all("div",{"id":"imgTagWrapperId"})
    download_url=""
    for item in img_container:
        print(item)
        
        for img in item.find_all("img"):
            
            print(img.get('data-a-dynamic-image').split(":")[1])
            download_url="https:"+str(img.get('data-a-dynamic-image').split(":")[1])
            print(download_url[:-1])
        

    response = requests.get(str(download_url[:-1]))
    file = open("images/product_image.jpg", "wb")
    file.write(response.content)
    file.close()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
ua=UserAgent()
userAgent=ua.random
print(userAgent)
chrome_options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(chrome_options=chrome_options)

CODE_PRODUCT=os.getenv("CODE_PRODUCT")                             ##CODICE PRODOTTO DA ANALIZZARE
HOST_LOGSTASH=os.getenv("HOST_LOGSTASH")                           ##IP LOGSTASH
PORT_LOGSTASH=os.getenv("PORT_LOGSTASH")                           ##PORT LOGSTASH
TIMEOUT_BEFORE_LOGSTASH=os.getenv("TIMEOUT_BEFORE_LOGSTASH")       ##SECONDI DA ASPETTARE PRIMA CHE LOGSTASH PARTE (100 sec) DEPRECATO
TIMEOUT_BEFORE_SEND_TO_LOGSTASH=os.getenv("TIMEOUT_BEFORE_SEND_TO_LOGSTASH")##SECONDI DA ASPETTARE PRIMA DI INVIARE DATI A LOGSTASH PARTE (1 sec) DEPRECATO
TIMEOUT_FETCH_ANOTHER_PAGE=os.getenv("TIMEOUT_FETCH_ANOTHER_PAGE") ##SECONDI PRIMA CHE PRENDI UN'ALTRA PAGINA (5 sec) (SERVE A EVITARE DI ESSERE BANNATO)
START_PAGE=int(os.getenv("START_PAGE"))                            ##PAGINA DA CUI INIZIARE (PREFERIBILMENTE 0)
END_PAGE=int(os.getenv("END_PAGE"))                                ##PAGINA FINALE 
DEBUG=os.getenv("DEBUG")                                           ##MODALITA DEBUG SKIPPA CONNESSIONE LOGSTASH SOLO PER TEST E ESPERIMENTI!
DOMAIN_URL=os.getenv("DOMAIN_URL")
MODE_REVIEWS=os.getenv("MODE_REVIEWS")

months={}
if DOMAIN_URL=='it':
    months={'gennaio':'01','febbraio':'02','marzo':'03','aprile':'04','maggio':'05','giugno':'06','luglio':'07','agosto':'08','settembre':'09','ottobre':'10','novembre':'11','dicembre':'12'}
else:
    months={'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}



HOST=HOST_LOGSTASH
PORT=int(PORT_LOGSTASH)
REQUIRED_CHARACTER="\n"                                            ##REQUIRED FOR LOGSTASH TO TAKE EVENT SEPARATED (TCP PLUGIN)
s="PLACEHOLDER"                                                    ##PLACEHOLDER FOR SOCKET

## WAIT UNTIL LOGSTASH IS UP 
##time.sleep(int(TIMEOUT_BEFORE_LOGSTASH)) <--- DEPRECATED
if DEBUG=='no':
    error=True
    while(error):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST_LOGSTASH, int(PORT_LOGSTASH)))
            sock.close()
            error = False
        except:
            print("ERROR:")
            print('Connection error. There will be a new attempt in 5 seconds\n')
            time.sleep(5)

    ##ESTABLISH CONNECTION TO LOGSTASH
    s=socket.socket()
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))




##TAKE PHOTOS
url_photo="https://www.amazon."+str(DOMAIN_URL)+"/dp/"+str(CODE_PRODUCT)
get_photos(url_photo)




for i in range(START_PAGE,END_PAGE):
    url="https://www.amazon."+str(DOMAIN_URL) + "/product-reviews/"+ str(CODE_PRODUCT) +"/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&"+"sortBy="+str(MODE_REVIEWS) +"&pageNumber="+str(i)
    driver.get(url)

    ####CANCELLARE DOPO
    print(url)
    ####

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    get_reviews(soup,s)
    time.sleep(int(TIMEOUT_FETCH_ANOTHER_PAGE))

    if DEBUG=='yes' :
        print(url)
        print(i)

    
if DEBUG=='no':
    s.close()

print("FINISHED FETCH PAGES")



