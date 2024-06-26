import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def extract_ifsc(image):
    image = image[100:200, 1100:1670] 
    ifsc_pattern = r'[A-Z]{4}[\d]{7}'
    text = pytesseract.image_to_string(image, lang='eng')
    ifsc_match = re.search(ifsc_pattern, text)
    if ifsc_match:
        return ifsc_match.group(0)
    return ""
def extract_cheque_number(image):
    # Pattern to match 'SAN: ' followed by digits and a space, then the 6-digit cheque number
    image = image[945:1050, 500:1900] 
    text = pytesseract.image_to_string(image,lang='mcr') 
    cheque_pattern1 = r'[c][\d]{6}[c]'
    cheque_match1 = re.search(cheque_pattern1, text)
    if cheque_match1:
        return cheque_match1.group(0)
    return ""
def extract_account_number(image):
    # Example: Extract account number assuming it's a 10-digit number
    image = image[540:660, 300:1100] 
    text = pytesseract.image_to_string(image, lang='eng')
    account_pattern = r'[\d]{13}'  
    # Search for the pattern in the text
    account_match = re.search(account_pattern, text)
    print(text)
    if account_match:
        account_number = account_match.group(0)
    else:
        account_number = ""
    return account_number

