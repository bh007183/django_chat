from collections import namedtuple
from logging import exception
import profile

from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions
from uritemplate import partial
from .permissions import IsCurrentUser

from chat.pagination import DefaultPagination
from .models import Profile, ProfileLink, Room, ProfileRoomLink, Message
from .serializers import ProfileSerializer, ProfileLinkSerializer, RoomSerializer, RoomProfileLinkSerializer, MessageSerializer,RoomDetailSerializer
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin,ListModelMixin
from .utils import ConnectionObject
from chat import serializers

# Create your views here.
# Manages Profile Operations
class ProfileListView(APIView):
    def post(self, request):
        request.data["user_id"] = self.request.user.id
        serializer = ProfileSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# All operations here must be current user
class ProfileDetailView(APIView):
    # request.user.id
    permission_classes =[IsCurrentUser] 
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
        serializer = ProfileSerializer(profile, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    

# Manages Connection Operations.
#Because there are additional fields on the ProfileLink table, I opted to not use the helper functions for creating connections for the sake of consistency.
#hidden URIs
class ProfileLinkListView(APIView):
    # creates a connection request. pending is by default set to true as the recipient has yet to accept.
    #AnyOne who is logged in can access this route as it reliews on the JWT info.
    permission_classes =[IsCurrentUser] 
    def post(self, request, pk):
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
        #retrieves all connections with pending connections
    def get(self,request, pk):
        queryset = Profile.objects.filter(connections=request.user.id)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
class ProfileLinkDetail(APIView):
    # this patch only worries about updating the pending field, otherwise there is nothing to update.
    permission_classes =[IsCurrentUser] 
    def patch(self, request, **kwargs):
        #pk here references the connections pk
        # gets current user connection object.
        userlink = get_object_or_404(ProfileLink, profile_id=request.user.id, friend_id=kwargs["connections_pk"])
        serializer1 = ProfileLinkSerializer(userlink, data={'pending': False}, partial=True)
        serializer1.is_valid(raise_exception=True)
        serializer1.save()
        # gets same object but from the friends perspective.
        friendlink = get_object_or_404(ProfileLink, profile_id=kwargs["connections_pk"], friend_id=request.user.id)
        serializer2 = ProfileLinkSerializer(friendlink, data={'pending': False}, partial=True)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()
        return Response(status=status.HTTP_200_OK)
    def delete(self, request, **kwargs):
        userlink = get_object_or_404(ProfileLink, profile_id=request.user.id, friend_id=kwargs["connections_pk"])
        friendlink = get_object_or_404(ProfileLink, profile_id=kwargs["connections_pk"], friend_id=request.user.id)
        userlink.delete()
        friendlink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get(self, request, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs["connections_pk"])
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)




class RoomProfileLinkList(APIView):
    permission_classes =[IsCurrentUser]
    # Creates and adds a Room to the current user.
    def post(self, request, pk):
        # Checkes to see if data is coming through in right format
        roomserializer = RoomSerializer(data = request.data)
        roomserializer.is_valid(raise_exception=True)
        # Gets Current users Profile if exists, Creates room, and adds it to user profile
        profile = get_object_or_404(Profile, id=request.user.id)
        profile.rooms.create(name=roomserializer.data["name"])
        profileserializer = ProfileSerializer(profile)
        return Response(profileserializer.data, status=status.HTTP_201_CREATED)
    def get(self, request, pk):
        queryset = Room.objects.filter(profile=request.user.id)
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)
class RoomProfileLinkDetail(APIView):
   #Adds users to an existing room.
    permission_classes =[IsCurrentUser]
    def put(self, request, **kwargs):
        # Checks to see if data is coming through in right format
        serailizer = RoomProfileLinkSerializer(data=request.data)
        serailizer.is_valid(raise_exception=True)
        
        #Access instance of ProfileLink table where current user and profile id line up.
        profilelink = get_object_or_404(ProfileLink, profile_id=request.user.id, friend_id=request.data['profile_id'])
        profilelinkserial = ProfileLinkSerializer(profilelink)
        if profilelinkserial.data["pending"]:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 
        else:
            try:
                # Gets Current users Profile if exists
                userprofile = get_object_or_404(Profile, id=request.user.id)
                #check to see if Current user is associated with the user and room
                # If not, exception is raised.
                userprofile.connections.get(id=request.data["profile_id"])
                userprofile.rooms.get(id=kwargs["room_pk"])
            # If all is good, then save.
                serailizer.save()
                return Response(status=status.HTTP_200_OK)  
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, **kwargs):
        instance = get_object_or_404(ProfileRoomLink, room_id=kwargs["room_pk"], profile_id=request.user.id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
##########################################################################################
                            #Not Sure About Placement#
    def get(self, request, **kwargs):
        userprofile = get_object_or_404(Profile, id=request.user.id)
        
       # try:
            #check to see if room is associated with user. If not it will throw exception.
        userprofile.rooms.get(id=kwargs["room_pk"])
        roomqueryset = Room.objects.get(id=kwargs["room_pk"])
        print(roomqueryset.profile_set.all())
        print(roomqueryset.message_set.all().reverse())
        serializer = RoomSerializer(roomqueryset)
            
      
        return Response(ProfileSerializer(roomqueryset.profile_set.all(), many=True).data)
            # return Response(seri)
        # except:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)




    
class MessageViewSet(CreateModelMixin,GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = DefaultPagination

    def create(self, request):
        print(request.data)
        userprofile = get_object_or_404(Profile, id=request.user.id)
        try:
            #check to see if room is associated with user. If not it will throw exception.
            userprofile.rooms.get(id=request.data["room_id"])
            #creates instance and saves it.
            serializer = MessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

   
        



    
       


        
       

        



    

        

        




    


        












