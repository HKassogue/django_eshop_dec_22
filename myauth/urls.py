from django.urls import path
from myauth import views

urlpatterns = [
    path('login', views.login, name='login'),
]