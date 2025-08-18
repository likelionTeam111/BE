from rest_framework import generics, permissions
from rest_framework import serializers
from accounts.models import CustomUser
from policy.models import Policy
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *

#마이페이지 접근시 권한 체크 (사용자 확인용)
class MyPageSerializer(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        user = request.user

        #내 맞춤프로필 정보

        #관심 정책 목록 


class ProfileSerializer(serializers.ModelSerializer):
    marry_display = serializers.SerializerMethodField()
    graduate_display = serializers.SerializerMethodField()
    employment_display = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'age', 'region', 'marry', 'marry_display', 
            'min_income', 'max_income', 'graduate', 'graduate_display', 
            'employment', 'employment_display', 'goal'
            ]
    
    def get_marry_display(self,obj):return obj.get_marry_display()
    def get_graduate_display(self, obj):return obj.get_graduate_display()
    def get_employment_display(self, obj):return obj.get_employment_display()