from django.contrib import admin
from django.urls import path
from bot import views

urlpatterns = [
    path('', views.index,name='home'),
    path('get', views.get,name='get'),
]
