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
        # user = CustomUser.objects.first()  # 테스트용: 첫 번째 유저

        # 기존 프로필이 있다면 모든 필드 초기화
        profile, created = Profile.objects.get_or_create(user=user)

        # M2M 필드 초기화
        profile.majors.clear()
        profile.special.clear()

        data = request.data.copy()  # 요청 데이터 복사

        # majors_code와 special_code는 실제 객체로 변환
        majors_codes = data.pop("majors_code", [])
        special_codes = data.pop("special_code", [])

        try:
            if majors_codes:
                majors_objs = Major.objects.filter(code__in=majors_codes)
                profile.majors.set(majors_objs)

            if special_codes:
                special_objs = Special.objects.filter(code__in=special_codes)
                profile.special.set(special_objs)

            # 나머지 필드 업데이트
            serializer = ProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"detail": f"서버 에러: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )









