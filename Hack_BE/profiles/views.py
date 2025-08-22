from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Profile
from .serializers import ProfileSerializer, RecommendSerializer, EnrollSerializer
from django.shortcuts import get_object_or_404
from .recommend import recommend_by_onboarding

class Profile_view(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related('user')
    
    def get_object(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)
        
        
class Enroll_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if Profile.objects.filter(user=request.user).exists():
            return Response({"detail": "Profile already exists"}, status=status.HTTP_409_CONFLICT) 
        serializer = EnrollSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user) 
            return Response(serializer.data, status = status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = EnrollSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    
# class MyPageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self,request):
#         # user = CustomUser.objects.first()  # 테스트용
#         user = request.user
        
#         try:
#             profile = user.profile
#             profile_data = ProfileSerializer(profile).data
#         except Profile.DoesNotExist:
#             profile_data = None

#         return Response(
#             {
#                 "profile": profile_data,
#             },
#             status=status.HTTP_200_OK
#         )


# class EnrollView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         # user = CustomUser.objects.first()  # 테스트용

#         user = request.user
#         profile, _ = Profile.objects.update_or_create(
#             user=user,
#             defaults={
#                 "age":None,
#                 "region":"",
#                 "marry_code":None,
#                 "max_income":None,
#                 "min_income":None,
#                 "graduate_code":None,
#                 "employment_code":None,
#                 "goal":"",
#             }
#         )
                                                
#         # ManyToMany 초기화
#         profile.major_code.clear()
#         profile.special_code.clear()

#         # serializer에 데이터 그대로 넘김
#         serializer = ProfileSerializer(profile, data=request.data, partial=False)
#         if serializer.is_valid():
#             serializer.save()  # LabelManyField가 자동으로 M2M 처리
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Recommend_view(generics.ListAPIView):
    serializer_class = RecommendSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        user = self.request.user
        qs = recommend_by_onboarding(user)
        return qs

