from cgitb import lookup
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_nested import routers

router= routers.SimpleRouter()


# router.register(r'room', views.RoomViewSet)
# room_router = routers.NestedSimpleRouter(router, r'room', lookup='room')
# room_router.register(r'message', views.MessageViewSet, basename='room-message')

urlpatterns = [
    path("", include(router.urls)),
    path('room/', views.RoomViewSet.as_view()),
    path('room@profile/', views.RoomProfileLinkView.as_view()),
    path('connect/', views.ProfileLinkView.as_view()),
    path('profile/', views.ProfileViewSet.as_view()),

]