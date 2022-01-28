from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router= routers.SimpleRouter()

# router.register(r'connect', views.ProfileLinkViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('connect/', views.ProfileLinkView.as_view()),
    path('profile/', views.ProfileList.as_view()),
    path('profile/<int:pk>/', views.ProfileDetail.as_view())
]