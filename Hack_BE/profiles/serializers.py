from rest_framework import generics, permissions
from rest_framework import serializers
from accounts.models import CustomUser
from policy.models import Policy
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .models import UserProfile

#마이페이지 접근시 권한 체크 (사용자 확인용)
class MyPageSerializer(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        user = request.user

        #내 맞춤프로필 정보

        #관심 정책 목록 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ["user"]

class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "region","age","martial_status","annual_income",
            "education","employment_status","major_field","specialty",
        ]