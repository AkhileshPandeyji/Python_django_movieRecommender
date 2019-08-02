from django.urls import path,include
from django.shortcuts import render
from . import views

app_name = "app"

urlpatterns = [
    path('/',views.index,name='index'),
    path('',views.watched,name='watched')
]