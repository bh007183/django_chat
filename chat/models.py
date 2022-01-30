
from django.db import models
from chat_app import settings

# Create your models here.

class Profile(models.Model):
    callsign = models.CharField(max_length=100)
    online = models.BooleanField(default=False)
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, db_column='user_id', on_delete=models.CASCADE)
    connections = models.ManyToManyField('Profile', through='ProfileLink', through_fields=('profile_id', 'friend_id'), blank=True)
    rooms = models.ManyToManyField('Room', through='ProfileRoomLink', through_fields=('profile_id', 'room_id'), blank=True)
    

class ProfileLink(models.Model):
    friend_id = models.ForeignKey('Profile', db_column='friend_id', related_name='friend_id',blank=True, null=True, on_delete=models.SET_NULL)
    profile_id= models.ForeignKey('Profile', db_column='profile_id', related_name='profile_id', blank=True, null=True, on_delete=models.SET_NULL)
    pending = models.BooleanField(default=True)


class Room(models.Model):
    name = models.CharField(max_length=100)
    
    

class ProfileRoomLink(models.Model):
    profile_id= models.ForeignKey('Profile', db_column='profile_id', blank=True, null=True, on_delete=models.SET_NULL)
    room_id = models.ForeignKey('Room', db_column='room_id', blank=True, null=True, on_delete=models.SET_NULL)


class Message(models.Model):
    message = models.TextField()
    room_id = models.ForeignKey(Room, db_column='room_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, db_column='user_id', on_delete=models.CASCADE)
    


