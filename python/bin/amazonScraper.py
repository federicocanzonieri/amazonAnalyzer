from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import socket
import time
import json



def get_reviews(soup,s):
    source_geo=soup.find('h3',{'data-hook':"arp-local-reviews-header"})
    global_geo=soup.find('h3',{'data-hook':"dp-global-reviews-header"})
    
    source_geo="rer"
    global_geo="ere"

    ###ONLY 1 FOR
    print("START GENERAL")
    reviews = soup.find_all('div',{'data-hook':'review'})
    for item in reviews:
        #print(item)
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
            helpful_vote=item.find('span',{'data-hook':'helpful-vote-statement'}).text.strip().split(" ")[0]
            if helpful_vote.lower()=='una':
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
        print(review)
        s.send(json.dumps(review).encode())
        s.send(bytes(REQUIRED_CHARACTER,'utf-8'))
        time.sleep(1)

    print("END GENERAL")
    """
    if DEBUG=='no':
        if source_geo is not None:
            print("SOURCE")
            reviews = soup.find_all('div', {'data-hook': 'review'})
            try:
                for item in reviews:
                    #print(item.find('span', {'data-hook': 'review-title'}).text.strip())
                    review = {
                    #'product': soup.title.text.replace('Amazon.it:Customer reviews:', '').strip(),
                    'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                    'rating':  (item.find('span', {'class': 'a-icon-alt'}).text[:1].strip()),
                    'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                    'date': item.find('span',{'data-hook':'review-date'}).text.strip()
                    }

                    
                    # s.send(json.dumps(review).encode())
                    # s.send(bytes(REQUIRED_CHARACTER,'utf-8'))
                    # time.sleep(1)
                    
                    #s.sendall(bytes(REQUIRED_CHARACTER,'utf-8'))
                    #reviewlist.append(review)
                    #print(item.text.split('\n\n\n')) ##PROVARE
            except Exception as e:
                print(e)
                pass
        
        if global_geo is not None:
            print("GLOBAL")
            reviews = soup.find_all('div', {'data-hook': 'review'})
            try:
                for item in reviews:
                    print(item.find('span', {'data-hook': 'review-title'}).text.strip())
                    review = {
                    #'product': soup.title.text.replace('Amazon.it:Customer reviews:', '').strip(),
                    'title': item.find('span', {'data-hook': 'review-title'}).text.strip(),
                    'rating':  (item.find('span', {'class': 'a-icon-alt'}).text[:1].strip()),
                    'body': item.find('span', {'class': 'cr-original-review-content'}).text.strip(),
                    'date': item.find('span',{'data-hook':'review-date'}).text.strip()
                    }
                    
                    # s.send(json.dumps(review).encode())
                    # s.send(bytes(REQUIRED_CHARACTER,'utf-8'))
                    # time.sleep(1)
                    
            except Exception as e:
                print(e)
                pass
    """




chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
driver = webdriver.Chrome(chrome_options=chrome_options)

CODE_PRODUCT=os.getenv("CODE_PRODUCT")
HOST_LOGSTASH=os.getenv("HOST_LOGSTASH")
PORT_LOGSTASH=os.getenv("PORT_LOGSTASH")
TIMEOUT_BEFORE_LOGSTASH=os.getenv("TIMEOUT_BEFORE_LOGSTASH")       ##SECONDI PRIMA CHE LOGSTASH PARTE (100) va bene
TIMEOUT_FETCH_ANOTHER_PAGE=os.getenv("TIMEOUT_FETCH_ANOTHER_PAGE") ##SECONDI PRIMA CHE PRENDI UN'ALTRA PAGINA (5) (SERVE A EVITARE DI ESSERE BANNATO)
START_PAGE=int(os.getenv("START_PAGE"))                            ##PAGINA DA CUI INIZIARE (PREFERIBILMENTE 0)
END_PAGE=int(os.getenv("END_PAGE"))                                ##PAGINA FINALE 
DEBUG=os.getenv("DEBUG")

HOST=HOST_LOGSTASH
PORT=int(PORT_LOGSTASH)
REQUIRED_CHARACTER="\n"                                            ## REQUIRED FOR LOGSTASH TO TAKE EVENT SEPARATED (TCP PLUGIN)
s="PLACEHOLDER"

## WAIT UNTIL LOGSTASH IS UP 
##time.sleep(int(TIMEOUT_BEFORE_LOGSTASH)) <--- DEPRECATED
if DEBUG=='no':
    error=True
    while(error):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST_LOGSTASH, int(PORT_LOGSTASH)))
            #sock.sendall(json.dumps(data).encode())
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
## B00ZYDLE80 paperino
## B093T7GQWB moco



for i in range(START_PAGE,END_PAGE):
    url="https://www.amazon.it/product-reviews/"+ str(CODE_PRODUCT) +"/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i)
    print(url)
    driver.get(url)
    #driver.get("https://www.amazon.it/product-reviews/"+ str(CODE_PRODUCT) +"/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    get_reviews(soup,s)
    print(i)
    time.sleep(int(TIMEOUT_FETCH_ANOTHER_PAGE))

if DEBUG=='no':
    s.close()



##SISTEMARE ALTRI PAESI / ITALIA FATTO
###CREARE DIREC PROG, git init, completare script con logstash e vedere cosa invia, poi kafka, spark, elastic, kibana

