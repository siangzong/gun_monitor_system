from django.contrib import admin
from django.urls import path
from Lineapp import views
from django.conf import settings
import os
from django.conf.urls.static import static
from django.shortcuts import redirect



urlpatterns = [
    path('callback/', views.callback),
]
