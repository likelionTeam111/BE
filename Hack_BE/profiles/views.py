from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileEnrollSerializer, ProfileReadSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer

from policy.models import Favorite_policy, Policy
from policy.serializers import FavoriteListSerializer


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

    def post(self,request):
        user = request.user
        #get_or_create - 현재 유저 프로필 정보가 없다면 생성, 있으면 업데이트 
        profile, created = Profile.objects.get_or_create(user=user)
        serializer = ProfileSerializer(profile,data=request.data,partial=False)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









