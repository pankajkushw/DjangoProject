from django.urls import path
from bio_data.views import home

urlpatterns = [
    path('', home, name = 'home')
]