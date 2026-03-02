from django.urls import path
from basicforms import views

urlpatterns = [
    path('', views.index, name='index')
    path('formpage/', views.for)
]