from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router= routers.SimpleRouter()

router.register(r'message', views.MessageViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('room/', views.RoomProfileLinkView.as_view()),
    path('connect/', views.ProfileLinkView.as_view()),
    path('profile/', views.ProfileViewSet.as_view()),

]