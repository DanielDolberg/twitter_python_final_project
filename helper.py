import requests
from bs4 import BeautifulSoup
import numpy
import geonamescache #this gives us a list of the countries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


gc = geonamescache.GeonamesCache()
countries = gc.get_countries_by_names()
states = gc.get_us_states_by_names()


def getTrendingTopics(api,country): #returns the current trend in the country
    weed = -1;
    for x in api.available_trends():
        if(x["country"] == country):
            weed = x['woeid'];
    
    return api.get_place_trends(weed);


def getAge(name,driver):
    # Navigate to the Twitter profile page
    driver.get('https://twitter.com/' + name)

    # Wait for the birthday element to be present
    wait = WebDriverWait(driver, 2)

    try:
        birthday_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(3) > div > div > div > div > div:nth-child(4) > div > span:nth-child(3)")))
        birthday_text = birthday_element.text

        year_of_birth = int(birthday_text[-5:-1].reverse())
        return 2023 - year_of_birth
    except:
        return numpy.nan
    
    
def check_country_real(loc):  
    
    for d in countries:
        if(loc.lower() in d.lower()):
            return loc
       
    for d in states:
        if(loc.lower() in d.lower()):
            return loc
        
    return None
            