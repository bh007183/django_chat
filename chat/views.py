from collections import namedtuple
from logging import exception
import re
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Profile, ProfileLink, Room, ProfileRoomLink, Message
from .serializers import ProfileSerializer, ProfileLinkSerializer, RoomSerializer, RoomProfileLinkSerializer, MessageSerializer
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from .utils import ConnectionObject

# Create your views here.
# Manages Profile Operations
class ProfileList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        request.data["user_id"] = self.request.user.id
        serializer = ProfileSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def delete(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Manages Connection Operations.
#TODO refactor ProfileLinViews to use helper methods like add or get
class ProfileLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # creates a connection request. pending is by default set to true as the recipient has yet to accept.
    def post(self, request):
        data = ConnectionObject(request)
        # sets connection for solicitor
        solicitor = ProfileLinkSerializer(data = data.set_solicitor())
        solicitor.is_valid(raise_exception=True)
        solicitor.save()
        # sets connection for recipient
        recipient = ProfileLinkSerializer(data = data.set_recipient())
        recipient.is_valid(raise_exception=True)
        recipient.save()
        return Response(status=status.HTTP_201_CREATED)
    # this patch only worries about updating the pending field, otherwise there is nothing to update.
    def patch(self, request):
        # gets current user connection object.
        userlink = get_object_or_404(ProfileLink, profile_id=request.user.id, friend_id=request.data['friend_id'])
        serializer1 = ProfileLinkSerializer(userlink, data={'pending': False}, partial=True)
        serializer1.is_valid(raise_exception=True)
        serializer1.save()
        # gets same object but from the friends perspective.
        friendlink = get_object_or_404(ProfileLink, profile_id=request.data['friend_id'], friend_id=request.user.id)
        serializer2 = ProfileLinkSerializer(friendlink, data={'pending': False}, partial=True)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        userlink = get_object_or_404(ProfileLink, profile_id=request.user.id, friend_id=request.data['friend_id'])
        friendlink = get_object_or_404(ProfileLink, profile_id=request.data['friend_id'], friend_id=request.user.id)
        userlink.delete()
        friendlink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        queryset = ProfileLink.objects.filter(profile_id=request.user.id)
        serializer = ProfileLinkSerializer(queryset, many=True)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomProfileLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # Creates and adds a Room to the current user.
    def post(self, request):
        # Checkes to see if data is coming through in right format
        roomserializer = RoomSerializer(data = request.data)
        roomserializer.is_valid(raise_exception=True)
        # Gets Current users Profile if exists, Creates room, and adds it to user profile
        profile = get_object_or_404(Profile, id=request.user.id)
        profile.rooms.create(name=roomserializer.data["name"])
        profileserializer = ProfileSerializer(profile)
        return Response(profileserializer.data, status=status.HTTP_201_CREATED)
    #Adds users to an existing room.
    def put(self, request):
        # Checkes to see if data is coming through in right format
        serailizer = RoomProfileLinkSerializer(data=request.data)
        serailizer.is_valid(raise_exception=True)
        # Gets Current users Profile if exists
        userprofile = get_object_or_404(Profile, id=request.user.id)
        try:
            #check to see if Current user is associated with the user and room
            # If not, exception is raised.
            userprofile.connections.get(id=request.data["profile_id"])
            userprofile.rooms.get(id=request.data["room_id"])
            # If all is good, then save.
            serailizer.save()
            return Response(status=status.HTTP_200_OK)  
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request):
        print(request.data)
        userprofile = get_object_or_404(Profile, id=request.user.id)
        try:
            userprofile.rooms.get(id=request.data["room_id"])
            serializer = MessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


    
       


        
       

        



    

        

        




    


        












