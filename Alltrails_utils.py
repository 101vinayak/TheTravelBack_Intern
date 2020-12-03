import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
from lxml import html

import time
import csv
import re 
import os

import numpy as np
import pandas as pd
import random

def get_url():
    
    city_name = 'canada/british-columbia'
    path_chrome = r"C:\Users\Lenovo\chromedriver"

    driver = webdriver.Chrome(path_chrome)
    url = 'https://www.alltrails.com/' + city_name
    driver.get(url)
    time.sleep(2)

    print("{} got loaded".format(url))
    print('getting trails in {}'.format(city_name))
    
    while(True):
        try:
            driver.find_element_by_class_name("styles-module__button___1nuva").click()
            time.sleep(random.randint(1, 5))
        
        except:
            break
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup)
    data = soup.find_all('div', class_='styles-module__containerDescriptive___3aZqQ styles-module__trailCard___2oHiP')
    
    links = []
    trail_title = []
    difficulty = []
    rating = []
    num_ratings = []
    description = []

    for i in range(len(data)):

        bs = data[i]
        print('--------{}------'.format(i))

        links.append('https://www.alltrails.com' + bs.find('a')['href'])

        title = bs.find('div', class_='styles-module__content___1eARw styles-module__content___3dWXB styles-module__descriptive___3ATWV')
        trail_title.append(title.find('a')['title'])

        diff = bs.find('span', class_="styles-module__diff___22Qtv styles-module__moderate___3w1it styles-module__selected___3fawg")
        if diff != None:
            difficulty.append(diff.text)

        else:
            diff = bs.find('span', class_="styles-module__diff___22Qtv styles-module__hard___3zHLb styles-module__selected___3fawg")

            if diff != None:
                difficulty.append(diff.text)

            else:
                difficulty.append('easy')

        rate = bs.find('span', class_='MuiRating-root default-module__rating___1k45X MuiRating-sizeLarge MuiRating-readOnly')
        rating.append(rate['aria-label'].split(' ')[0])

        num = bs.find('span', class_="styles-module__count___2pQCU")
        num_ratings.append(num.text.split('(')[1].split(')')[0])

        disc = bs.find('div', class_='xlate-none styles-module__description___QlXBP styles-module__description___fUlLc')
        try:
            description.append(disc.text.split('Show')[0])
        except:
            description.append('NULL')
        
    dict = {'Title' : trail_title, 'Rating' : rating, 'Number of ratings': num_ratings, 
            'Difficulty' : difficulty, 'Description' : description, 'Links' : links}
    df = pd.DataFrame(dict)
    
    ## Saving data
    df.to_csv('Alltrails_links.csv')

    driver.close()
    return df
            
            
            
            
            
            
            
            
            
            
            
            
            
            