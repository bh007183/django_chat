from dataclasses import fields
from rest_framework import serializers
from .models import Profile, ProfileLink, Room, ProfileRoomLink
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields=['callsign', 'online', 'connections','rooms', 'user_id']

    def update(self, instance, validated_data):
        print(instance)
        validated_data.pop('user_id', None)  # prevent myfield from being updated
        return super().update(instance, validated_data)

        

class ProfileLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLink
        fields = ['friend_id', 'profile_id', "pending"]

class RoomSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer
   
    class Meta: 
        model = Room
        fields = ["id", "name"]

class RoomProfileLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileRoomLink
        fields = ["id", "profile_id", "room_id"]





  
        