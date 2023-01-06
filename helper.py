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


def getTrendingTopics(api,country): #returns the current trend in the country
    
    weed = None;
    
    if(country == None):
        return weed
    
    country = country.replace(',',' ').split()[0].capitalize()
    
    
    for x in WOEID:
        if(x["name"] == country):
            weed = x['woeid']
            trends = api.get_place_trends(weed) #get a strange dict
            trends = trends[0]['trends'] #extract the actual list we need
            return [t['name'] for t in trends] #extract the names of the trending
    
    return None


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
    if(loc == ''): #if the user doesn't have a location the API will give '' back, which is basically None
        return None
    
    for d in countries:
        if(d.lower() in loc.lower()):
            return loc
       
    for d in states:
        if(d.lower() in loc.lower()):
            return loc
        
    return None


def getGender(bio,location,name):
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
            return 'F'
    
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