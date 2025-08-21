from rest_framework import generics,status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Profile
from .serializers import ProfileSerializer, RecommendSerializer
from .recommend import recommend_by_onboarding

# class EnrollView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self,request):
#         user = request.user
#         #get_or_create - 현재 유저 프로필 정보가 없다면 생성, 있으면 업데이트 
#         profile, created = Profile.objects.get_or_create(user=user)
#         serializer = ProfileSerializer(profile,data=request.data,partial=False)

#         if serializer.is_valid():
#             serializer.save()

#             return Response(
#                 serializer.data, 
#                 status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrollView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # get_or_create로 프로필 인스턴스 가져오기
        profile, created = Profile.objects.get_or_create(user=user)
        
        # 시리얼라이저에 인스턴스(profile)와 요청 데이터(request.data) 전달
        # partial=True로 설정하면 부분 업데이트 가능
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            # serializer.save()가 create() 또는 update() 메서드를 호출
            serializer.save()
            
            # 성공 응답
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        
        # 유효성 검사 실패 응답
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Profile_view(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
    lookup_url_kwarg = 'id'

class Recommend_view(generics.ListAPIView):
    serializer_class = RecommendSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        user = self.request.user
        qs = recommend_by_onboarding(user)
        return qs
        






