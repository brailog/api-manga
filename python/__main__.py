import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import os
import shutil

class UrlManga():
    def __init__(self,name):
        '''
        :param name: Nome do anime a ser buscado
        Método construtor.
        '''
        base = 4 # Base para index HTML
        i = 1
        search_url = 'https://mangayabu.com/?s='
        name = name.replace(" ","+")
        url = search_url + name
        page = requests.get(url) #MODULAR ISSO 
        soup = BeautifulSoup(page.text, 'html.parser') 
        #titles = soup.find_all('h4',{'class':'video-title'})
        titles = soup.find_all('h4',{'class':'video-title'})
        if len(titles) > 1:
            for x in titles:
                print(i,' - ',x.text)
                i += 1
            choose = int(input('\nChoose a mangá: '))
            self.__manga_url = soup.find_all('a', href=True)[base+(choose*4)]['href']
            self.name = titles[choose-1].text
        else:
            self.__manga_url = soup.find_all('a', href=True)[base+base]['href'] # MELHORAR
            self.name = titles[0].text 
    
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
        os.mkdir('src')
        self.__FindCap(cap)
        page = requests.get(self.__listofcaps) #MODULAR ISSO 
        soup = BeautifulSoup(page.text, 'html.parser')  
        images = (soup.find_all('img'))
        i = 0
        size = 800, 900
        for image in images:
            try:
                response = requests.get(image['src'])
                img = Image.open(BytesIO(response.content))
                img.thumbnail(size)
                img = img.convert('LA')
                
                img.save('src/img{}.png'.format(i))
                i+=1
            except Exception as x:
                print("Error Download ",x)
                
        pdf = FPDF()
        pdf.add_page()
        imagelist = os.listdir('src')
        print(imagelist)
        i = 0
        for image in imagelist:
            try:
                if image != '__main__.py':
                    img = Image.open('src/img{}.png'.format(i))
                    pdf.image('src/img{}.png'.format(i),w=187)
                    i += 1
            except Exception as x:
                print("Error Download ",x)
        pdf.output("{}_{}.pdf".format(self.name,cap), "F")
        shutil.rmtree('src')
        
    
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
    t = UrlManga('Claymore')
    t.DownloadCap(82)