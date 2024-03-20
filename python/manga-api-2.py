import os
import sys

import requests
from PIL import Image
from fpdf import FPDF
from io import BytesIO


HOST_FILE_PATH = "/home/gabriel/.config/JetBrains/PyCharmCE2023.3/scratches"
PAGE_NOT_FOUND_END_CHAPTER = 3


def img_dir_to_epud(page_image_dir, manga, chapter):
    pdf = FPDF()
    pdf.add_page()
    imagelist = os.listdir(page_image_dir)
    for image in sorted(imagelist, key=get_page_number):
        try:
            print(f'{page_image_dir}{image}')
            pdf.image(f'{page_image_dir}{image}', w=190)
        except Exception as e:
            print("Error Download ", e)
    pdf.output("{}_{}.pdf".format(manga, chapter), "F")

def get_page_number(file):
    return int(file.split('.')[0])

class MangaAPI(object):
    def __init__(self, manga, initial_chapter=1, final_chapter=10):
        self.URL_jpg = "https://img.lermanga.org/B/{MANGA_NAME}/capitulo-{CHAPTER}/{PAGE_NUMBER}.jpg"
        self.URL_png = "https://img.lermanga.org/B/{MANGA_NAME}/capitulo-{CHAPTER}/{PAGE_NUMBER}.png"
        self.manga = manga
        self.manga_dir_full_path = f"{HOST_FILE_PATH}/{self.manga}"
        self.initial_chapter = initial_chapter
        self.final_chapter = final_chapter

    def get_request(self, **kwargs):
        chapter = kwargs.get("chapter")
        page = kwargs.get("page_number")
        manga = kwargs.get("manga")

        url_jpg = self.URL_jpg.format(
            MANGA_NAME=manga,
            CHAPTER=chapter,
            PAGE_NUMBER=page)

        url_png = self.URL_png.format(
            MANGA_NAME=manga,
            CHAPTER=chapter,
            PAGE_NUMBER=page)

        response = requests.get(url_jpg)
        print(url_jpg)
        if response.status_code != 200:
            print(f"Unable to get for {url_jpg}. Trying {url_png}")
            print(url_png)
            response = requests.get(url_png)

        return response

    def get_page_img_from_response(self, response, save_path=None):
        img = Image.open(BytesIO(response.content))
        if save_path:
            print(f"Saving img: {save_path}")
            img.convert('RGB')
            img.save(save_path, 'png')
        return img

    def _setup(self):
        if not self.manga:
            sys.exit()

        if os.path.exists(self.manga_dir_full_path):
            print(f"Path: {self.manga_dir_full_path} already created")
        else:
            print(f"Creating the folder: {self.manga_dir_full_path}")
            os.mkdir(f"{self.manga_dir_full_path}")

    def run(self):
        self._setup()
        for chapter_number in range(self.initial_chapter-1, self.final_chapter):
            end = 0
            if "-" not in str(self.initial_chapter):
                chapter_number = f"0{chapter_number}"
            chapter_already_in_local = os.path.exists(os.path.join(self.manga_dir_full_path, f'chapter{chapter_number}'))
            if not chapter_already_in_local:
                print(f"Creating the folder: {os.path.join(self.manga_dir_full_path, f'chapter{chapter_number}')}")
                os.mkdir(f"{os.path.join(self.manga_dir_full_path, f'chapter{chapter_number}')}")

            for page in range(1, 100):
                if not chapter_already_in_local:
                    if end < PAGE_NOT_FOUND_END_CHAPTER:
                       try:
                           response = self.get_request(manga=self.manga, chapter=chapter_number, page_number=page)
                           self.get_page_img_from_response(response, f"{self.manga_dir_full_path}/chapter{chapter_number}/{page}.png")
                       except Exception as e:
                           print(e)
                           end += 1

if __name__ == '__main__':
    mapi = MangaAPI("berserk", 0, 1)
    mapi.run()
    # response = mapi.get_request(chapter="-16", page_number="10", manga="berserk")
    # mapi.get_page_img_from_response(response, "/home/gabriel/.config/JetBrains/PyCharmCE2023.3/scratches/dumpy/test69.png")
    # for chapter in range():
    #    print(chapter)
   # img_dir_to_epud(f"/home/gabriel/.config/JetBrains/PyCharmCE2023.3/scratches/berserk/chapter00/", 'berserk', '00')