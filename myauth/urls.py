from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from myauth import views

urlpatterns = [
    path('login', views.login, name='login'),
    # path('login', 
    #     view=LoginView.as_view(template_name='myauth/login.html', 
    #         redirect_authenticated_user=True), 
    #     name='login'),
    path('logout', view=LogoutView.as_view(), name='logout'),
    path('register', views.register, name='register'),
]