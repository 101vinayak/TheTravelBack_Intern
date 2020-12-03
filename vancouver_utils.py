import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from lxml import html

from PIL import Image
import io
from selenium.common.exceptions import ElementClickInterceptedException

import requests
import time
import csv
import re 
import os

import numpy as np
import pandas as pd
import random

def get_urls():
    
    filename = 'VancouverTrails_links.csv'
    if not os.path.exists(filename):
        with open(filename, "w", encoding='utf8',newline="\n") as f:
            
            path_chrome = r"C:\Users\Lenovo\chromedriver"
            driver = webdriver.Chrome(path_chrome)

            url = 'https://www.vancouvertrails.com/trails/'
            driver.get(url)
            time.sleep(2)

            print("{} got loaded".format(url))
            soup = bs(driver.page_source, 'html.parser')

            trails = soup.find_all('li', class_='col-lg-12 col-md-12 col-sm-12 col-12 trail-listing')

            csvwriter=csv.writer(f)
            csvwriter.writerow(["Title", "rating", "region", 'difficulty', 'time', 'distance', 'season', 'link'])

            for trail in trails:

                url_ = 'https://www.vancouvertrails.com' + trail.find('a')['href']
                title = trail.find('span').text
                print(title)

                try:
                    details = trail.find('ul', class_='row trail-row trail-odd').find_all('li')

                except:
                    details = trail.find('ul', class_='row trail-row').find_all('li')

                row = [i.text for i in details]
                row.insert(0, title)
                row.append(url_)

                csvwriter.writerow(row)
            
            driver.close()
    
    df = pd.read_csv(filename)
    return df

def download_img(img_url, title):
    
    baseDir=os.getcwd() + '\VancouverTrails_Images\{}'.format(title)
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)
    
    for i, url in enumerate(img_url):
        
        file_name = f"{i}.jpg"

        try:
            image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - COULD NOT DOWNLOAD {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')

            file_path = os.path.join(baseDir, file_name)

            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)

            #print(f"SAVED - {url} - AT: {file_path}")

        except Exception as e:
            continue

def scrape_trail(i):
    
    df = get_urls()
    urls = df['link']
    titles = df['Title']
    rating = df['rating']
    region = df['region']
    
    tags = ['Difficulty', 'Time', 'Trip length', 'Elevation gain', 'season', 
            'camping', 'time from vancouver', 'public transit', 'dog friendly']
    
    try:
        path_chrome = r"C:\Users\Lenovo\chromedriver"
        link = 'https://www.vancouvertrails.com'

        driver = webdriver.Chrome(path_chrome)
        driver.get(urls[i])
        time.sleep(30)
        print("{} got loaded".format(urls[i]))

        soup = bs(driver.page_source, 'html.parser')

        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div/a').click()
        time.sleep(5)

        soup = bs(driver.page_source, 'html.parser')
        images = soup.find('div', class_='top-gallery-link')
        num = int(images.text.replace('\n', '')[0])
        #print(num)

        url = []
        for j in range(min(5, num)):

            soup = bs(driver.page_source, 'html.parser')
            img_url = soup.find('img', class_='mfp-img')
            url.append(link + img_url['src'])
            #print(link + img_url['src'])

            driver.find_element_by_xpath('/html/body/div[2]/div/button[2]').click()
            time.sleep(5)

        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/button').click()
        time.sleep(2)
        download_img(url, titles[i])

        #### COMMENT PAGE
        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div/div/div[2]/ul/li[1]/a').click()
        time.sleep(5)
        comment_soup = bs(driver.page_source, 'html.parser')
        comment_list = comment_soup.find_all('div', class_='comment-list')

        comments = []
        for j in range(len(comment_list)):
            name = 'NULL'
            rate = 'NULL'
            comment = 'NULL'
            try:
                name = comment_list[j].find('strong').text.split(' writes:')[0]
            except:
                name = 'NULL'

            try:
                rate = comment_list[j].find('input', class_='rating form-control hide')['value']
            except:
                rate = 'NULL'

            try:
                comment = comment_list[j].text.split('\n')[1].split(':')[1]
            except:
                comment = 'NULL'

            comments.append({'Name' : name, 'rate' : rate, 'comment' : comment})

        driver.back()
        time.sleep(3)
        ####

        details = soup.find('ul', class_='trail-stats').find_all('li')
        details = [i.find('span', class_='value').text for i in details]

        detail_dict = dict((tags[i], details[i]) for i in range(len(tags)))
        detail_dict['rating'] = df['rating'][i]
        detail_dict['region'] = df['region'][i]

        info = soup.find('div', class_='trail-info')
        info = info.text.replace('\n', '')

        trail_dict = ({'Title' : titles[i], 'Info' : info, 'Details' : detail_dict, 'Comments' : comments})
        filename = os.path.join("vancouver_extract.csv")
        if not os.path.exists(filename):
            with open(filename, "w", encoding='utf8',newline="\n") as f:
                csvwriter=csv.writer(f)
                csvwriter.writerow(['Title', 'Info', 'Details', 'Comments'])
                csvwriter.writerow([titles[i], info, detail_dict, comments])

        else:
            with open(filename, "a", encoding='utf8',newline="\n") as f:
                csvwriter=csv.writer(f)
                csvwriter.writerow([titles[i], info, detail_dict, comments])

        driver.close()
        return
    
    except:
        return