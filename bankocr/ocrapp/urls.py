from django.urls import path
from . import views

app_name = 'ocrapp'

urlpatterns = [
    path('', views.ocr_view, name='upload'),
]
