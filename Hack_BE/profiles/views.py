from rest_framework import generics,status, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileEnrollSerializer, ProfileReadSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer


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



# class MyPageView(generics.RetrieveAPIView):
#     serializer_class = CustomUserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         # JWT 인증된 사용자 반환
        # return self.request.user







