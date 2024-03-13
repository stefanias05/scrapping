from django.urls import path
from .views import scrapping_data
urlpatterns = [
    path("", scrapping_data, name='download_data')
]
