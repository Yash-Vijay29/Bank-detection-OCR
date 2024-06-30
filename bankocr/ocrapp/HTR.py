import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
import subprocess
from paddleocr import PaddleOCR
def extract_transfer_to(image):
    image = image[190:340, 150:1700]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 125, 250, cv2.THRESH_BINARY)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    image = cv2.erode(image, kernel2, iterations=1)
    cv2.imwrite("static/temp/roi_transfer_to.png", image) 
    ocr = PaddleOCR(cls=True, lang='en', use_gpu=False)
    result = ocr.ocr(image)
    if result is None or len(result) == 0 or result[0] is None or len(result[0]) == 0:
     return ""
    
    txts = [line[1][0] for line in result[0]]
    string1 = ' '.join(txts)
    return string1


    return result
def extract_transfer_amt_eng(image):
    image = image[295:400, 300:2200]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 125, 250, cv2.THRESH_BINARY)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    image = cv2.erode(image, kernel2, iterations=1)
    cv2.imwrite("static/temp/roi_transfer_amt_eng.png", image)
    ocr = PaddleOCR(cls=True, lang='en', use_gpu=False)
    result = ocr.ocr(image)
    if result is None or len(result) == 0 or result[0] is None or len(result[0]) == 0:
     return ""
    txts = [line[1][0] for line in result[0]]
    string1 = ' '.join(txts)
    return string1
def extract_transfer_amt(image):
    image = image[400:500, 1800:2400]
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image,125,250,cv2.THRESH_BINARY)[1]
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    image= cv2.dilate(image,kernel2,iterations=1)
    cv2.imwrite("static/temp/roi_transfer_amt.png", image)
    ocr = PaddleOCR(cls=True, lang='en', use_gpu=False)
    result = ocr.ocr(image)
    if result is None or len(result) == 0 or result[0] is None or len(result[0]) == 0:
     return ""
    txts = [line[1][0] for line in result[0]]
    string1 = ' '.join(txts)
    return string1
def extract_signature(image):
 image = image[600:950, 1720:2320]
 gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 threshw = cv2.threshold(gray, 125 , 255, cv2.THRESH_BINARY)[1]
 thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY_INV)[1]
 kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (55,2))
 kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
 dilate = cv2.dilate(thresh,kernel2,iterations=1)
 threshw = cv2.erode(threshw,kernel2,iterations=1)
 dilate = cv2.dilate(thresh,kernel,iterations=1)
 cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 cnts = cnts[0] if len(cnts) == 2 else cnts[1]
 cnts = sorted(cnts, key = lambda x: cv2.boundingRect(x)[0])
 for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h>28:
                roi = gray[y:y + h, x:x + w]
                cv2.imwrite("static/temp/roi_signature.png", roi)
                return True
                # Handle the error in a meaningful way if necessary
 return False
