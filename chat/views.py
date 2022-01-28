from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Profile, ProfileLink
from .serializers import ProfileSerializer, ProfileLinkSerializer
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin

# Create your views here.

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

class ProfileLinkViewSet(DestroyModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = ProfileLink.objects.all()
    serializer_class = ProfileLinkSerializer











