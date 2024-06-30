import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
def preprocess_image(image):
    image2 = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (55, 27))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    image = cv2.erode(image,kernel2,iterations=2)
    image = cv2.dilate(image, kernel, iterations=1)
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
    rois = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if 35 < h < 130 and w > 13:
                roi = image2[y:y + h, x:x + w]
                rois.append(roi)
                # Handle the error in a meaningful way if necessary
    return rois
def extract_ifsc(image):
    # Define the patterns for IFSC code
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshw = cv2.threshold(gray, 200 , 270, cv2.THRESH_BINARY)[1]
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    threshw = cv2.dilate(threshw,kernel2,iterations=2)
    ifsc_pattern = r'[A-Z]{4}[0][\d]{6}|[A-Z]{4}[O][O][\d]{5}|[A-Z]{4}[O][\d]{6}|[A-Z]{4}[\d]{6} [\d]|[A-z]{5}[\d]{5} [\d]'
    text = pytesseract.image_to_string(threshw, lang='eng')
    # Search for matches with each pattern
    ifsc_match = re.search(ifsc_pattern, text)
    if ifsc_match:
        return ifsc_match.group(0)
    # Return an empty string if no match is found
    return ""
def extract_cheque_number(image):
    # Pattern to match 'SAN: ' followed by digits and a space, then the 6-digit cheque number
    image = image[945:1050, 500:1900] 
    text = pytesseract.image_to_string(image, lang='mcr')
    cheque_pattern1 = r'[c][\d]{6}[c]'
    cheque_match1 = re.search(cheque_pattern1, text)
    if cheque_match1:
        return cheque_match1.group(0)
    return ""
def extract_account_number(image):
    # Example: Extract account number assuming it's a 10-digit number

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshw = cv2.threshold(gray, 200 , 270, cv2.THRESH_BINARY)[1]
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    threshw = cv2.dilate(threshw,kernel2,iterations=2)
    threshw = cv2.erode(threshw,kernel3,iterations=2)
    text = pytesseract.image_to_string(threshw, lang='eng')
    account_pattern = r'[\d]{13} [\d]{1}|[\d]{14}|[$][\d]{13}'  
    # Search for the pattern in the text
    account_match = re.search(account_pattern, text)
    print(text)
    if account_match:
        account_number = account_match.group(0)
    else:
        account_number = ""
    return account_number






