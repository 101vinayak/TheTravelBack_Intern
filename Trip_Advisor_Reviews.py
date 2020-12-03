from bs4 import BeautifulSoup as bs
import requests
from lxml import html
import pandas as pd
import random
import time
import os
import csv

user_agents = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.813.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.794.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.864.0 Safari/535.2'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.815.10913 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.813.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.813.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.812.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.810.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.810.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.809.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.794.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1'},
{'User-Agent':'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1'}
]
def head():
    n = random.randint(0,19)
    return user_agents[n]


main_pages = []
url = "https://www.tripadvisor.in/Restaurants-g154943-Vancouver_British_Columbia.html"
main_pages.append(url)
for i in range(30,2911,30): # Collecting all pages
  url = "https://www.tripadvisor.in/Restaurants-g154943-oa"+str(i)+"-Vancouver_British_Columbia.html"
  main_pages.append(url)


subpages = []
for j in main_pages: # Iterating through main pages and getting restaurants pages
  content_1 = requests.get(j,headers = head())
  soup_1 = bs(content_1.text,'html.parser')
  for k in soup_1.findAll('a',class_="_15_ydu6b"):
    page = "https://www.tripadvisor.in"+str(k.get('href'))
    subpages.append(page)
print(len(subpages))

from google.colab import drive 
drive.mount('/content/drive')
folder = r"/content/drive/My Drive/Reviews_folder"
print(folder)
if not os.path.exists(folder):
    os.mkdir(folder)
h=0
for i in subpages:
    #will extract name from subpage
    content_2 = requests.get(i,headers = head() )
    soup_2 = bs(content_2.text,'html.parser')
    Name = soup_2.find('h1',class_="_3a1XQ88S").text
    name_f = "_".join(Name.split(" "))
    name_f = name_f.replace("/","_")
    h=h+1
    print(h,end=" ")
    print(name_f,end="\n")
    filename = os.path.join(folder,name_f+".csv")
    if not os.path.exists(filename):
        with open(filename, "w", encoding='utf8',newline="\n") as f:
            csvwriter=csv.writer(f)
            csvwriter.writerow(["Name","Review_Quote","Review_Summary","Date_of_Review","Date_of_Visit"])
            review_pages = []
            review_pages.append(i)
            try:
              number_of_rev = soup_2.find('a', class_="_10Iv7dOs").text.split(" ")[0]
            except:
              number_of_rev = '0'
            print(number_of_rev,end=" ")
            if int(number_of_rev)>10 :
                iter = soup_2.find('a',class_="pageNum last cx_brand_refresh_phase2").text
                for j in range(10,int(iter)*10,10):
                  splits = i.split("Reviews")
                  page = splits[0]+"Reviews-or"+str(j)+splits[1]
                  review_pages.append(page)
            print(len(review_pages),end=" ")
            for m in review_pages:
                content_3 = requests.get(m,headers = head())
                soup_3 = bs(content_3.text,'html.parser')
                for link in soup_3.findAll('a',class_="title"):
                    req = "https://www.tripadvisor.in/"+str(link.get('href'))
                    content_4 = requests.get(req,headers = head() )
                    soup_4 = bs(content_4.text,'html.parser')
                    try:
                        Date_of_Review = soup_4.find('span',class_="ratingDate relativeDate").text[8:]
                    except:
                        Date_of_Review = "N/A"
                    try:
                        Review_Quote = soup_4.find('span',class_="noQuotes").text
                    except:
                        Review_Quote = "N/A"
                    try:
                        Review_Summary = soup_4.find('p',class_="partial_entry").text
                    except:
                        Review_Summary = "N/A"
                    try:
                        Date_of_Visit = soup_4.find('div',class_="prw_rup prw_reviews_stay_date_hsx").text.split(":")[1]
                    except:
                        Date_of_Visit = "N/A"
                    csvwriter.writerow([Name,Review_Quote,Review_Summary,Date_of_Review,Date_of_Visit])
        print("Done",end="\n")
