from django.contrib import admin
from django.urls import path
from . import views
from rest_framework import status

urlpatterns = [
    path('', views.ProfileList.as_view()),
    path('<int:pk>/', views.ProfileDetail.as_view())
]