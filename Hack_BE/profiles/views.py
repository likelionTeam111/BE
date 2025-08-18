from django.shortcuts import render
from rest_framework import generics, permissions
from accounts.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 



# class MyPageView(generics.RetrieveAPIView):
#     serializer_class = CustomUserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         # JWT 인증된 사용자 반환
        # return self.request.user




