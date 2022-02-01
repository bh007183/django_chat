from cgitb import lookup
from posixpath import basename
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_nested import routers

router= routers.SimpleRouter()


# router.register(r'room', views.RoomViewSet)
# room_router = routers.NestedSimpleRouter(router, r'room', lookup='room')
# room_router.register(r'message', views.MessageViewSet, basename='room-message')
#Note, all routes with profile/<int:pk>/ are protected to verify the current user can only access that view. No one else is permited access.


urlpatterns = [
    path("", include(router.urls)),
    path('profile/<int:pk>/room/', views.RoomProfileLinkList.as_view()),
    path('profile/<int:pk>/room/<int:room_pk>/', views.RoomProfileLinkDetail.as_view()),
    path('profile/', views.ProfileListView.as_view()),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view()),
    path('profile/<int:pk>/connections/', views.ProfileLinkListView.as_view()),
    path('profile/<int:pk>/connections/<int:connections_pk>/', views.ProfileLinkDetail.as_view()),

]