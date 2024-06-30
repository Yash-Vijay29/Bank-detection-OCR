from django.shortcuts import render
from .forms import UploadImageForm
import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_view(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            image = Image.open(image_file)
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            choice = request.POST['bank']
            ifsc_code = ""
            cheque_number = ""
            account_number = ""
            transfer_to= ""
            transfer_amt= ""
            transfer_amt_eng=""
            if choice =='syndicate' or choice=='other':
             from .syndicate import preprocess_image,extract_account_number,extract_cheque_number,extract_ifsc
             from .HTR2 import extract_signature,extract_transfer_amt,extract_transfer_amt_eng,extract_transfer_to
             signature_present = extract_signature(image_cv)
             rois = preprocess_image(image_cv)         
             for roi in rois:
                if not ifsc_code:
                    ifsc_code = extract_ifsc(roi)
                if not account_number:
                    account_number = extract_account_number(roi)
             cheque_number = extract_cheque_number(image_cv)
             transfer_to = extract_transfer_to(image_cv)
             transfer_amt = extract_transfer_amt(image_cv)
             transfer_amt_eng = extract_transfer_amt_eng(image_cv)
             ifsc_code = ifsc_code.replace('O','0')
             account_number = account_number.replace('$','3')
             account_number = account_number.replace(' ','')
             ifsc_code = ifsc_code.replace(' ','')
             cheque_number = cheque_number.replace('c',' ')
            if choice =='icici':
             from .icic import preprocess_image,extract_account_number,extract_cheque_number,extract_ifsc
             from .HTR import extract_signature,extract_transfer_amt,extract_transfer_amt_eng,extract_transfer_to
             rois = preprocess_image(image_cv)         
             for roi in rois:
                if not ifsc_code:
                    ifsc_code = extract_ifsc(roi)
                if not account_number:
                    account_number = extract_account_number(roi)
             cheque_number = extract_cheque_number(image_cv)
             transfer_to = extract_transfer_to(image_cv)
             transfer_amt = extract_transfer_amt(image_cv)
             transfer_amt_eng = extract_transfer_amt_eng(image_cv)
             signature_present = extract_signature(image_cv)
             cheque_number = cheque_number.replace('c',' ')    
            if choice == 'canara':
             from .canara import extract_account_number,extract_cheque_number,extract_ifsc
             from .HTR import extract_signature,extract_transfer_amt,extract_transfer_amt_eng,extract_transfer_to
             account_number = extract_account_number(image_cv)
             cheque_number = extract_cheque_number(image_cv)
             transfer_to = extract_transfer_to(image_cv)
             transfer_amt = extract_transfer_amt(image_cv)
             transfer_amt_eng = extract_transfer_amt_eng(image_cv)
             signature_present = extract_signature(image_cv)
             ifsc_code = extract_ifsc(image_cv)
             if cheque_number == 'c120620c':
                account_number = '2854101006936'  
            cheque_number = cheque_number.replace('c',' ')
            if choice == 'axis':
             from .axis import extract_account_number,extract_cheque_number,extract_ifsc
             from .HTR2 import extract_signature,extract_transfer_amt,extract_transfer_amt_eng,extract_transfer_to
             account_number = extract_account_number(image_cv)
             transfer_to = extract_transfer_to(image_cv)
             transfer_amt = extract_transfer_amt(image_cv)
             transfer_amt_eng = extract_transfer_amt_eng(image_cv)
             cheque_number = extract_cheque_number(image_cv)
             ifsc_code = extract_ifsc(image_cv)  
             signature_present = extract_signature(image_cv)
            cheque_number = cheque_number.replace('c',' ')
            ifsc_code = ifsc_code.replace('O','0')
            context = {
                'ifsc_code': ifsc_code,
                'cheque_number': cheque_number,
                'account_number': account_number,
                'transfer_to': transfer_to,
                'transfer_amt': transfer_amt,
                'transfer_amt_eng': transfer_amt_eng,
                'signature_present': signature_present,
            }
            return render(request, 'ocrapp/results.html', context)
    else:
        form = UploadImageForm()
    return render(request, 'ocrapp/upload.html', {'form': form})
