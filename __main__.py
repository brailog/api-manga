# mangayabu
from lxml import html
import requests
from bs4 import BeautifulSoup

class UrlManga():
    def __init__(self,name):
        self.__url = 'https://mangayabu.com/?s='
        self.__name = name.replace(" ","+")
        url = self.__url + self.__name
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        titles = soup.find_all('h4',{'class':'video-title'})
        if len(titles) > 1: 
            raise NotImplementedError
        else:
            print('No Plus')

        
if __name__ == "__main__":
    t = UrlManga('boku no hero')