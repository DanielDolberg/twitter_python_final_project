import requests
import tweepy
from bs4 import BeautifulSoup
import numpy as np
import json
import geonamescache #this gives us a list of the countries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#credit https://codebeautify.org/jsonviewer/f83352
WOEID = json.load(open('twitter_woeid.json'))#the list of all twitter WOEID


gc = geonamescache.GeonamesCache()
countries = gc.get_countries_by_names()
states = gc.get_us_states_by_names()


def getAge(driver):
    
    
    wait = WebDriverWait(driver, 1)
    # Navigate to the Twitter profile page
    try:
        #birthday_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-901oao css-16my406 r-14j79pv r-4qtqp9 r-poiln3 r-1b7u577 r-bcqeeo r-qvutc0")))
        birthday_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(3) > div > div > div > div > div:nth-child(4) > div > span:nth-child(3)")))
        birthday_text = birthday_element.text

        year_of_birth = int(birthday_text[-4:])
        return 2023 - year_of_birth
    except:
        return np.nan
    
    
def check_country_real(loc):  
    if(loc == '' or loc == None): #if the user doesn't have a location the API will give '' back, which is basically None
        return None
    
    for d in countries:
        if(d.lower() in loc.lower()):
            return loc
       
    for d in states:
        if(d.lower() in loc.lower()):
            return loc
        
    return None


def getGender(bio,location,name):
    
    
    if type(bio) != 'str':
        bio = 'x'
    if type(location) != 'str':
        location = 'x'
    if type(name) != 'str':
        name = 'x'    
    
    bio = bio.lower().strip().replace(" ", "")#removes spaces
    location = location.lower().strip().replace(" ", "")#removes spaces
    name = name.lower().strip().replace(" ", "")#removes spaces

    she_her = 'she/her'
    he_him = 'he/him'
    they_them = 'they/them'
    
    #check she/her
    if she_her in bio.lower() or she_her in location.lower() or she_her in name.lower() :
        return 'F'
    
    #check he/him
    if he_him in bio.lower() or he_him in location.lower() or he_him in name.lower() :
        return 'M'
    
    #check they/them
    if they_them in bio.lower() or they_them in location.lower() or they_them in name.lower() :
            return 'T'
    
    return None

def countWordsInString(str):
    if len(str) == 0:#return 0 if it's empty
        return 0
    
    strip = str.strip()
    i = 1
    for c in strip:
        if c == ' ':
            i+=1
    
    return i

def get_WOEID(name,country):
    for x in WOEID:
        if x['name'].lower() == name.lower():
            return x['woeid']

        if x['country'].lower() == country.lower():
            return x['woeid']
        
def getAllTrends():#returns a dictionary of all the trends
    trends = {}
    us_link = 'https://trends24.in/united-states/'
    nz_link = 'https://trends24.in/new-zealand/'    
    uk_link = 'https://trends24.in/united-kingdom/'    
    au_link = 'https://trends24.in/australia/'
    ca_link = 'https://trends24.in/canada/'
    
    main_links = [us_link,nz_link,uk_link,uk_link,au_link,ca_link]
    
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 1)
    
    for l in main_links:
        driver.get(l)
        city_elements = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".suggested-locations__list")))
        country_name = driver.find_element(By.CSS_SELECTOR,'#app-bar-toggle > span:nth-child(1)').text #get the area name
        trends[country_name] = []
        tr = driver.find_element(By.CSS_SELECTOR, "div.trend-card:nth-child(1) > ol:nth-child(2)")
        tr = tr.find_elements(By.TAG_NAME,'a')
        for y in tr:
            trends[country_name].append(y.text)
        
        tmp_links = [x.get_attribute('href') for x in city_elements.find_elements(By.TAG_NAME,'a')]
        
        for x in tmp_links:
            driver.get(x)
            tr = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.trend-card:nth-child(1) > ol:nth-child(2)")))
            name = driver.find_element(By.CSS_SELECTOR,'#app-bar-toggle > span:nth-child(1)').text #get the area name
            name = name[:-(2+len(country_name))] #remove the name at the end, for example ', United States' at the end
            trends[name] = []
            tr = tr.find_elements(By.TAG_NAME,'a')
            for y in tr:
                trends[name].append(y.text)

    driver.quit()
    return trends

def getTrendsByLoc(city,country,trends):#returns an array of a trend in the loc
    for t in trends:
        if city == t.title():
            return trends[city]
    
    return trends[country]

def areTrendUsed(text,trends):
    text = text.lower()
    
    for t in trends:
        if t.lower() in text:
            return True
        
    return False