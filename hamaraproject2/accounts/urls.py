"""hamaraproject2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import GeneratePdf

urlpatterns = [
    path('register',views.register,name="register"),
    path('rescue',views.rescue,name="rescue"),
    path('login',views.login,name="login"),
    path('rescue2', views.rescue2, name="rescue2"),
    path('main', views.main, name="main"),
path('logout', views.logout, name= 'logout'),
path('contact', views.contact, name= 'contact'),
path('', views.simple_upload, name= 'simple_upload'),
path('export_excel', views.export_excel, name= 'export_excel'),
path('pdf', GeneratePdf.as_view()),
path('dlt', views.dlt, name= 'dlt')


]
