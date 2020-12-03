import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

import random
import cssutils

from bs4 import BeautifulSoup as bs
import re as r
import os
import time
import numpy as np
import csv

#this part of the code below chooses a header at random from a collection of 10 headers
header_list=[{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36COOKIE: 5=2; ax=v167-7'},
       {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/74.0.3729.157 Safari/537.36'},
       {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/79.0.3945.88 Safari/537.36'},
       {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'},
       {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'},
       {'User-Agent':'Mozilla/5.0 (X11; Datanyze; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'},
       {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.24 Safari/537.36'}]


def head():
    n = random.random()
    n=int(n*7)
    return header_list[n]

def scrape_site(name):
    
    path_chrome = r"/chromedriver"
    url  = 'https://maps.roadtrippers.com/?lng=-126.35144998641863&lat=55.342552909447306&z=4.320481614698682'

    driver = webdriver.Chrome(path_chrome)
    driver.get(url)
    print("{} got loaded".format(url))
    
    time.sleep(40)
    for i in range(3):
        driver.find_element_by_xpath('//*[@id="trip-creation"]/section[{}]/div/span'.format(i+1)).click()
    
    element = driver.find_element_by_xpath('//*[@id="search-text"]')
    search  = driver.find_element_by_xpath('//*[@id="search"]/div[3]/div[1]')
    element.clear()
    element.send_keys(name + ' British Columbia')
    search.click()

    try:
        time.sleep(40)
        driver.find_element_by_xpath('//*[@id="layer-panel"]/div/div/div/ul/li[1]/div/div/a/div[1]').click()
    
    except:
        print('not found')
        driver.close()
        return
    
    try:
        driver.find_element_by_xpath('//*[@id="place"]/div[4]/div[2]/div[1]/div[1]/div/div[2]').click()
    except:
        pass

    time.sleep(10)
    soup = bs(driver.page_source, 'html.parser')
    
    description = {}
    try:
        desc = soup.find('div', class_='description')
        description['title'] = desc.find('h2').text
        
        desc = soup.find('div', class_='description-content')
        description['title'] = desc.find('p').text
    except:
        pass
    
    try:
        timings = soup.find('section', class_='hours')
        timings = timings.find('li').text
        print(timings)
    except:
        timings = None

    try:
        driver.find_element_by_xpath('//*[@id="place"]/div[4]/div[2]/div[2]/div[4]/div/div[2]/div').click()
        time.sleep(3)
        soup = bs(driver.page_source, 'html.parser')
        
        general = soup.find('section', class_='general-attributes')
        
        try:
            general_no = general.find_all('li', class_='false')
        except:
            general_no = []
        
        try:
            general_unk = general.find_all('li', class_='unknown')
        except:
            general_unk = []
        
        try:
            general = general.find_all('li')
        except:
            general = []
        
        set1 = set(general_no)
        set2 = set(general_unk)
        set3 = set(general)
        res = list(set3 - set1)
        res

        Tags = []
        for i in res:
            Tags.append(i.text)
        
        general = soup.find('div', class_='secondary-attributes')
        
        try:
            general_no = general.find_all('li', class_='false')
        except:
            general_no = []
        
        try:
            general_unk = general.find_all('li', class_='unknown')
        except:
            general_unk = []
        
        try:
            general = general.find_all('li')
        except:
            general = []
        
        set1 = set(general_no)
        set2 = set(general_unk)
        set3 = set(general)
        res = list(set3 - set1)
        res

        for i in res:
            Tags.append(i.text)
        
        print(Tags)

    except:
        Tags = []
    
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div[2]').click()
    time.sleep(10)
    
    urls = []
    try:
        print('#######3')
        driver.find_element_by_xpath('//*[@id="place"]/div[1]/div[2]/div[3]/div/div[1]/div/a/div/div[2]').click()
        time.sleep(2)
        
        print('#######3')
        driver.find_element_by_xpath('//*[@id="gallery"]/div/div/div[1]/div/div[4]').click()
        time.sleep(10)
        print('#######3')
        soup = bs(driver.page_source, 'html.parser')
        imgs = soup.find_all('a', class_='js-route image-hover')
        
        print(len(imgs))
        
        for i in range(min(5, len(imgs))):
            img = imgs[i].find('div', class_='image loaded')
            print(img)
            img = img['style']
            urls.append(img)
            
        driver.back()
        driver.back()
        time.sleep(3)
        
    except:
        pass    
    
    filename = os.path.join("_tag.csv")
    if not os.path.exists(filename):
        with open(filename, "w", encoding='utf8',newline="\n") as f:
            csvwriter=csv.writer(f)
            csvwriter.writerow(["Name","Tags","Timings","Images","Description"])
            csvwriter.writerow([name + ' British Columbia', Tags, timings, urls, description])
    
    else:
        with open(filename, "a", encoding='utf8',newline="\n") as f:
            csvwriter=csv.writer(f)
            csvwriter.writerow([name + ' British Columbia', Tags, timings, urls, description])

    #driver.close()

def scrape_gmap(name):
    
    path_chrome = r"C:\Users\Lenovo\chromedriver"
    ua = head()
    user_agent = "user-agent="+ua['User-Agent']
    chrome_options= webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument(user_agent)
    #print('user-agent\n',user_agent)
    driver = webdriver.Chrome(path_chrome,options=chrome_options)
    #print('opening defualt page')
    url  = 'https://www.google.com/maps/@30.7678096,76.4684188,14z'

    driver.get(url)
    time.sleep(10)
    
    try:
        element = driver.find_element_by_xpath("//input[@id='searchboxinput']")
        search  = driver.find_element_by_xpath("//button[@id='searchbox-searchbutton']")
        
        element.clear()
        element.send_keys(name)
        search.click()
        
        time.sleep(60)

        soup = bs(driver.page_source, 'html.parser')
        loc = ''
        details = []
        try:
            det = soup.find_all('div', class_='ugiz4pqJLAG__primary-text gm2-body-2')
            loc = det[0].text

            for i in det:
                details.append(i.text)
        except:
            try:
                det = soup.find_all('div', class_='section-info-line')
                loc = det[0].text
                
                for i in det:
                    details.append(det[i].text)
            except:
                pass
        print(loc)
        print(details)
            
        x = soup.find('div', class_='cX2WmPgCkHi__root gm2-body-2 cX2WmPgCkHi__dense')
        timing_dic = {}
        
        if x is not None:
            try:
                element = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[12]/div[1]')
            except:
                driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[11]/div[1]').click()

            time.sleep(2)

            soup = bs(driver.page_source, 'html.parser')
            timings = soup.find_all('tr', class_='lo7U087hsMA__row-row')

            timing_dic = {}
            try:
                for i in timings:
                    timing_dic[i.text.split('   ')[0].replace(' ', '')] = i.text.split('   ')[1]
            except:
                pass
        print(timing_dic)
            
        title = soup.find_all('title')
        title = title[0].text.split(' - ')[0]
        print(title)

        ratings = soup.find('span', class_='section-star-display')
        rating = ratings.text
        
        print(rating)
        try:
            driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[7]/button').click()
            time.sleep(5)
            soup = bs(driver.page_source, 'html.parser')
            services = soup.find_all('div', class_='section-attribute-group-item')

            serv_dic = {}
            
            for i in services:
                if not i.find('div', class_='section-attribute-group-item-icon maps-sprite-place-attributes-not-interested'):
                    serv_dic[i.text.replace(' ', '')] = 1
                else:
                    serv_dic[i.text.replace(' ', '')] = 0
            
            driver.back()
            time.sleep(5)
            soup = bs(driver.page_source, 'html.parser')
        except:
            serv_dic = 'None'
        
        print(serv_dic)
        
        Tags = []
        try:
            tags = soup.find_all('div', class_='tuPVDR7ouq5__has-right-neighbor')
            for i in tags[1:]:
                s = i.text
                result = ''.join([i for i in s if not i.isdigit()])
                Tags.append(result)
        except:
            pass
        
        print(Tags)

        driver.find_element_by_xpath('//*[@class="allxGeDnJMl__button allxGeDnJMl__button-text"]').click()
        time.sleep(5)
        
        print('#####')

        while(True):
            try:
                element = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[10]')
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
            except:
                break
                
        time.sleep(2)
        rev_soup = bs(driver.page_source, 'html.parser')
        reviews = rev_soup.find_all('div', class_='section-review ripple-container GLOBAL__gm2-body-2')

        comments = []
        for i in range(len(reviews)):
            try:
                rev_title = reviews[i].find('div', class_='section-review-title').text.replace(' ','')
            except:
                rev_title = 'none'
            
            try:
                stars = reviews[i].find('span', class_='section-review-stars')['aria-label']
            except:
                stars = 'none'
                
            try:
                rev_text = reviews[i].find('span',class_='section-review-text').text
            except:
                rev_text = 'none'

            rev_dict = ({'title' : rev_title, 'rate' : stars, 'info' : rev_text})
            comments.append(rev_dict)
        print(comments[0])

        driver.back()
        coord = driver.current_url.split('z')[0].split('@')[1].split(',')[:2]
        
        filename = os.path.join("gmap.csv")
        if not os.path.exists(filename):
            with open(filename, "w", encoding='utf8',newline="\n") as f:
                csvwriter=csv.writer(f)
                csvwriter.writerow(["Name", "Rating", 'Services', 'Tags', 'Timings', 'Coordinates', 'Comments', 'Details', 'Address'])
                csvwriter.writerow([name + ' British Columbia', rating, serv_dic, Tags, timing_dic, coord, comments, details, loc])
        
        else:
            with open(filename, "a", encoding='utf8',newline="\n") as f:
                csvwriter=csv.writer(f)
                csvwriter.writerow([name + ' British Columbia', rating, serv_dic, Tags, timing_dic, coord, comments, details, loc])
        driver.close()

    except:
        
        print('error')
        driver.close()
        return