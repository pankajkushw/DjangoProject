
from django.urls import path
from help_page import views


urlpatterns = [
    path('',views.help, name="help"),
]