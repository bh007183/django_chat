from dataclasses import fields
from djoser.serializers import UserCreateSerializer as BaseUserCreate

class UserCreateSerializer(BaseUserCreate):
    class Meta(BaseUserCreate.Meta):
        fields = ['id', 'password', 'email', 'first_name', 'last_name']