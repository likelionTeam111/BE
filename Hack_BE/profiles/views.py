from django.shortcuts import render
from rest_framework import generics, permissions
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from .models import UserProfile
from .serializers import UserProfileSerializer, EnrollSerializer


class MyPageView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # JWT 인증된 사용자 반환
        return self.request.user

class EnrollView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        userprofile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = EnrollSerializer(instance=userprofile, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        #return Response(UserProfileSerializer(userprofile).data, status=status.HTTP_200_OK)
    



