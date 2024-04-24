from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.signupview, name='signup_url'),
    path('', views.loginview, name='login_url'),
    path('logout/', views.logoutview, name='logout_url'),
    path('con/',views.formView, name = 'loginform'),
]
