from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer

from policy.models import Favorite_policy, Policy
from policy.serializers import FavoriteListSerializer
from .models import Profile, Major, Special
from accounts.models import CustomUser


class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        # user = CustomUser.objects.first()  # 테스트용
        user = request.user
        
        try:
            profile = user.profile
            profile_data = ProfileSerializer(profile).data
        except Profile.DoesNotExist:
            profile_data = None

        return Response(
            {
                "profile": profile_data,
                
            },
            status=status.HTTP_200_OK
        )


class EnrollView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # user = CustomUser.objects.first()  # 테스트용

        user = request.user
        profile, _ = Profile.objects.update_or_create(
            user=user,
            defaults={
                "age":None,
                "region":"",
                "marry_code":None,
                "max_income":None,
                "min_income":None,
                "graduate_code":None,
                "employment_code":None,
                "goal":"",
            }
        )
                                                
        # ManyToMany 초기화
        profile.majors.clear()
        profile.special.clear()

        # serializer에 데이터 그대로 넘김
        serializer = ProfileSerializer(profile, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()  # LabelManyField가 자동으로 M2M 처리
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

