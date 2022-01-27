from dataclasses import fields
from rest_framework import serializers
from .models import Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields=['callsign', 'online', 'connections', 'user_id']

    def update(self, instance, validated_data):
        validated_data.pop('user_id', None)  # prevent myfield from being updated
        return super().update(instance, validated_data)

  
        