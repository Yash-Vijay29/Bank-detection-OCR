from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadImageForm
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_text(image):
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def detect_signature(image):
    height, width = image.shape
    signature_area = image[int(height * 0.75):height, int(width * 0.5):width]
    contours, _ = cv2.findContours(signature_area, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]
    return len(contours) > 0

def ocr_view(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            image = Image.open(image_file)
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            processed_image = preprocess_image(image_cv)
            extracted_text = extract_text(processed_image)
            signature_present = detect_signature(processed_image)
            context = {
                'text': extracted_text,
                'signature_present': signature_present,
            }
            return render(request, 'ocrapp/results.html', context)
    else:
        form = UploadImageForm()
    return render(request, 'ocrapp/upload.html', {'form': form})
