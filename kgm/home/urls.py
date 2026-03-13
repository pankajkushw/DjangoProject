from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('gallery/', views.gallery, name='gallery'),
    path('donations/', views.donations, name='donations'),
    path('contact/', views.contact, name='contact'),
]