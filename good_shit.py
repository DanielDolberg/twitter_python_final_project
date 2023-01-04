import requests
from bs4 import BeautifulSoup
import numpy

def getTrendingTopics(api,country): #returns the current trend in the country
    weed = -1;
    for x in api.available_trends():
        if(x["country"] == country):
            weed = x['woeid'];
    
    return api.get_place_trends(weed);



def getAge(name):
    r = requests.get('https://twitter.com/' + name);
    soup = BeautifulSoup(r.content , 'html.parser');
    html = soup.find('div', attrs = {'class':'css-1dbjc4n r-1ifxtd0 r-ymttw5 r-ttdzmv'});
    
    
    html = html.find('span', attrs = {'class': 'css-901oao css-16my406 r-14j79pv r-4qtqp9 r-poiln3 r-1b7u577 r-bcqeeo r-qvutc0'});
    
    if type(html) == 'NoneType':
        return numpy.nan;
    
    return html.string
    
    
            