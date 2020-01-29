#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:54:36 2020

@author: gabriel
"""
#    pdf.image(name, x,y,w,h)
# http://vip.mangalivre.com/vip_download/q0_wDv1KSjUcGRNRwBmU8Q/1580267272/53/5047/5566/Claymore_-_75_-_Chrono.zip

from fpdf import FPDF
import os
import cv2
count = 0

pdf =  FPDF('P', 'mm', (100,150))
l = os.listdir('/home/gabriel/Documentos/Manga/content')
l.sort()
pdf.add_page()
for i in l:
    img = cv2.imread('/home/gabriel/Documentos/Manga/content/'+i, cv2.IMREAD_UNCHANGED)
    scale_percent = 31 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image    
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite('/home/gabriel/Documentos/Manga/cv2save/img{}.png'.format(count),resized)
    pdf.image('/home/gabriel/Documentos/Manga/cv2save/img{}.png'.format(count))
    count += 1

pdf.output("Claymore.pdf", "F")

