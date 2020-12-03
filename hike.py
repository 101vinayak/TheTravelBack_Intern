import requests
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import random
import time
import csv
from selenium import webdriver
import re
import os
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


def trials(trial):
    chrome_options = webdriver.ChromeOptions()
    ua = head()
    user_agent = "user-agent="+ua['User-Agent']
    chrome_options.add_argument(user_agent)
    driver1 = webdriver.Chrome(options = chrome_options)
    driver1.get(trial)
    soup = bs(driver1.page_source,'html.parser')
    try:
        name = driver1.find_element_by_xpath('//h1[@class="xlate-none styles-module__name___1nEtW"]').text
    except:
        name = "N/A"
    try:
        difficulty_level = driver1.find_element_by_xpath('//div[@class="styles-module__info___1Mbn6 styles-module__thin___3YRdx"]').text.split("\n")[0]
    except:
        difficulty_level = "N/A"
    try:
        Overall_rating = driver1.find_element_by_xpath('//meta[@itemprop="ratingValue"]').get_attribute('content')
    except:
        Overall_rating = "N/A"
    try:
        worst_rating = driver1.find_element_by_xpath('//meta[@itemprop="worstRating"]').get_attribute('content')
    except:
        worst_rating = "N/A"
    try:
        best_rating = driver1.find_element_by_xpath('//meta[@itemprop="bestRating"]').get_attribute('content')
    except:
        best_rating = "N/A"
    try:
        review_count = driver1.find_element_by_xpath('//meta[@itemprop="reviewCount"]').get_attribute('content')
    except:
        review_count = "N/A"
    try:
        location = driver1.find_element_by_xpath('//a[@class="xlate-none styles-module__location___11FHK styles-module__location___3wEnO"]').text
    except:
        location = "N/A"
    try:
        length = driver1.find_elements_by_xpath('//span[@class="detail-data xlate-none"]')[0].text
    except:
        length = "N/A"
    try:
        elevation_gain = driver1.find_elements_by_xpath('//span[@class="detail-data xlate-none"]')[1].text
    except:
        elevation_gain = "N/A"
    try:
        route_type = driver1.find_element_by_xpath('//span[@class="detail-data"]').text
    except:
        route_type = "N/A"
    try:
        tags = driver1.find_element_by_xpath('//section[@class="tag-cloud"]').text
    except :
        tags = "N/A"
    if not tags == "N/A":
        tags = re.findall('[A-Z][^A-Z]*', tags)
    try:
        description = driver1.find_element_by_xpath('//p[@class="styles-module__displayText___17Olo styles-module__lineClamp___1u_mB"]').text
    except:
        description = "N/A"
    if not description=="N/A":
        description = description.replace('\n',"")
    waypoints = soup.findAll('h3',class_="styles-module__name___1kcf_")
    waypoints_list = []
    for w in waypoints:
        waypoints_list.append(w.text)
    lat_long = soup.findAll('p',class_="styles-module__latLng___2uavK")
    lat_long_list = []
    for l in lat_long:
        lat_long_list.append(l.text)
    waypoint_description =soup.findAll('p',class_="styles-module__description___YwFBe")
    waypoint_description_list = []
    for d in waypoint_description:
        waypoint_description_list.append(d.text.replace("\n","").replace("\r","")) 
    waypoint_dict = dict(zip(list(zip(waypoints_list,lat_long_list)),waypoint_description_list))
    headings = []
    try:
        for header in soup.findAll('span',class_="MuiTab-wrapper styles-module__tabWrapper___1nPqf")[1:4]:
            headings.append(header.text.upper())
    except:
        headings = []
    heading_desc = [] 
    try:
        for desc in soup.findAll('p',class_="styles-module__displayText___17Olo styles-module__lineClamp___1u_mB")[1:4]:
            heading_desc.append(desc.text)
    except:
        heading_desc = []
    heads = dict(zip(headings,heading_desc))
    try:
        contact = heads['CONTACT']
    except:
        contact = "N/A"
    try:
        tips = heads['TIPS']
    except:
        tips = "N/A"
    try:
        getting_there = heads['GETTING THERE']
    except:
        getting_there = "N/A"
    try:   
        weather = soup.find('ul',class_="styles-module__list___3n1tr false").text
        weather_elements = re.findall('[A-Z][^A-Z]*[A-Z]',weather)
    except:
        weather_elements = "N/A"
    try:
        uv_bt = driver1.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/article/div[3]/div/div/div[3]/div/button[2]/span').click()
        uv_elements = driver1.find_element_by_xpath('//ul[@class="styles-module__list___3n1tr false"]').text
        lis=[]
        for i in uv_elements.split("\n"):
            if i.isdigit()==False:
                lis.append(i)
        uv_index = {}
        for uv in range(len(lis)):
            if uv%2==0:
                uv_index[lis[uv]]=lis[uv+1]
    except:
        uv_index = "N/A"
    try:
        day_light_bt = driver1.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/article/div[3]/div/div/div[3]/div/button[3]/span').click()
        day_light_elements = driver1.find_element_by_xpath('//ul[@class="styles-module__list___3n1tr styles-module__activeDayLight___2K2K0"]').text
        day_light_elements = day_light_elements.split("\n")
        day_light = {}
        for dl in range(len(day_light_elements)):
            if dl%2==0:
                day_light[day_light_elements[dl]]=day_light_elements[dl+1]
    except:
        day_light = "N/A"
    folder = r"D:Hikes"
    if not os.path.exists(folder):
        os.mkdir(folder)
    fil_name = "AllTrials"
    filename = os.path.join(folder,fil_name+".csv")
    with open(filename,"w",encoding="utf8",newline="\n") as hf:
        csvwriter=csv.writer(hf)
        csvwriter.writerow(['Name','Difficulty Level','Overall Rating','Worst Rating','Best Rating','Number of Reviews','Location','Length','Elevation Gain','Route Type','Tags','Description','Waypoints','Contact','Tips','Getting There','Weather','UV Index','Day Light'])
        csvwriter.writerow([name,difficulty_level,Overall_rating,worst_rating,best_rating,review_count,location,length,elevation_gain,route_type,tags,description,waypoint_dict,contact,tips,getting_there,weather_elements,uv_index,day_light])
        print(name,difficulty_level,Overall_rating,worst_rating,best_rating,review_count,location,length,elevation_gain,route_type,tags,description,waypoint_dict,contact,tips,getting_there,weather_elements,uv_index,day_light)
    reviews_path = "D:Hikes_reviews"
    reviews_file = os.path.join(reviews_path,name+".csv")
    if not os.path.exists(reviews_file):
        try:
            printed_no_of_results = driver1.find_element_by_xpath('//div[@class="styles-module__showing___14AKF"]').text.split("-")[1].split("of")[0]
            no_of_results = driver1.find_element_by_xpath('//div[@class="styles-module__showing___14AKF"]').text.split("of")[1]
        except:
            printed_no_of_results = "N/A"
            no_of_results = "N/A"
        if not printed_no_of_results == "N/A" and no_of_results == "N/A":
            while(int(printed_no_of_results) != int(no_of_results)):
                try:
                    see_more_reviews_bt = driver1.find_element_by_xpath('//button[@class="styles-module__button___1nuva styles-module__whiteBackground___2TOXY"]').click()
                    printed_no_of_results = driver1.find_element_by_xpath('//div[@class="styles-module__showing___14AKF"]').text.split("-")[1].split("of")[0]
                    no_of_results = driver1.find_element_by_xpath('//div[@class="styles-module__showing___14AKF"]').text.split("of")[1]
                except:
                    print("complete")
                    break
        try:
            reviews = driver1.find_elements_by_xpath('//div[@class="styles-module__content___1eARw styles-module__content___3z_PR"]')
        except:
            reviews = "N/A"
        if not reviews=="N/A":
            revs=[]
            for rev in reviews:
                revs.append(rev.text)
            user_names = []
            review_dates = []
            review_tags = []
            for r in revs:
                content = r.split("\n")
                user_names.append(content[0])
                review_dates.append(content[1])
                review_tags.append(re.findall('[A-Z][^A-Z]*',content[2]))
            soup_reviews = bs(driver1.page_source,'html.parser')
            all_review_tags=soup_reviews.findAll('div',attrs = {'itemprop':'review'})
            review_summaries = []
            for rt in all_review_tags:
                if 'reviewBody' in str(rt):
                    review_summaries.append(str(rt).split('itemprop="reviewBody">')[1].split("</p>")[0])
                else:
                    review_summaries.append("N/A") 
            rating = driver1.find_elements_by_xpath('//span[@class="MuiRating-root default-module__rating___1k45X MuiRating-sizeLarge MuiRating-readOnly"]')
            all_ratings=[]
            for rate in rating:
                all_ratings.append(rate.get_attribute('aria-label'))
            ratings = all_ratings[1:int(no_of_results)+1]
            data = pd.DataFrame(columns=['User Name','Rating','Date','Tags','Summary'])
            data['User Name']=pd.Series(user_names)
            data['Rating']=pd.Series(ratings)
            data['Date']=pd.Series(review_dates)
            data['Tags']=pd.Series(review_tags)
            data['Summary']=pd.Series(review_summaries)
            data.to_csv(reviews_file,index=False)
            chrome_options.arguments.remove(user_agent)

    
        