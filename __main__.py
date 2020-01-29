# mangayabu
from lxml import html
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import cv2
from fpdf import FPDF
import os

class UrlManga():
    def __init__(self,name):
        '''
        :param name: Nome do anime a ser buscado
        Método construtor.
        '''
        search_url = 'https://mangayabu.com/?s='
        self.__name = name.replace(" ","+")
        url = search_url + self.__name
        page = requests.get(url) #MODULAR ISSO 
        soup = BeautifulSoup(page.text, 'html.parser') 
        #titles = soup.find_all('h4',{'class':'video-title'})
        self.__manga_url = soup.find_all('a', href=True)[8]['href'] 
    
    def GetAll(self):
        raise NotImplementedError
        
    def __FindCap(self,cap):
        '''
        :param cap: Capitulo a ser baixado        
        '''
        page = requests.get(self.__manga_url) #MODULAR ISSO 
        soup = BeautifulSoup(page.text, 'html.parser')  
        self.__listofcaps = (soup.find_all('a',{'class':'chapter-link'}))[-cap]['href']
       
    
    def DownloadCap(self,cap):
        '''
        self.__FindCap(cap)
        page = requests.get(self.__listofcaps) #MODULAR ISSO 
        soup = BeautifulSoup(page.text, 'html.parser')  
        images = (soup.find_all('img'))
        i = 0
        for image in images:
            try:
                response = requests.get(image['src'])
                img = Image.open(BytesIO(response.content))
                img.save('/home/gabriel/Documentos/GIT/manga-api/img{}.png'.format(i))
                i+=1
            except Exception as x:
                print("Error Download ",x)
        '''
        pdf = FPDF()
        # imagelist is the list with all image filenames
        pdf.add_page()
        imagelist = os.listdir('/home/gabriel/Documentos/GIT/manga-api')
        print(imagelist)
        i = 0
        for image in imagelist:
            try:
                if image != '__main__.py':
                    pdf.image('/home/gabriel/Documentos/GIT/manga-api/img{}.png'.format(i),w=180)
                    i += 1
            except Exception as x:
                print("Error Download ",x)
        pdf.output("yourfile.pdf", "F")
        
                
            
                
    
    '''
    FUTURA MODULAÇÃO
    @property
    def __GetAllCaps(self):
        page = requests.get(self.__manga_url) #MODULAR ISSO 
        soup = BeautifulSoup(page.text, 'html.parser')  
        _len = (len(soup.find_all('a',{'class':'chapter-link'})))
        return _len
    '''
        
        
if __name__ == "__main__":
    t = UrlManga('claymore')
    t.DownloadCap(75)