from django.urls import path
from . import views
from .views import RecruitmentDataInputView


urlpatterns = [
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('verify_account/', views.verify_account, name="verify_account"),
    
    path('forgot_password/', views.send_password_reset_link, name="send_password_reset_link"),
    path('verify_password_reset_link/<str:email>/<str:reset_token>/', views.verify_password_reset_link, name="verify_password_reset_link"),
    path('recurtiment_data_input/', views.RecruitmentDataInputView.as_view(), name='recurtiment_data_input')
]