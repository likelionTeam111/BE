from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Profile
from .serializers import ProfileSerializer, EnrollSerializer
from policy.serializers import PolicyListSerializer
from policy.models import Policy
from .recommend import recommend_by_onboarding

class Profile_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        print(profile)
        if profile is None:
            return Response({})
        return Response(ProfileSerializer(profile).data)
        
        
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

class Recommend_view(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PolicyListSerializer
    pagination_class = None
    def get_queryset(self):
        user = self.request.user
        category = self.kwargs.get("category")
        qs = recommend_by_onboarding(user, category)
        return qs[:5]

class Recommend_all_view(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PolicyListSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        categories = ["일자리", "주거", "교육", "복지문화", "참여권리"]

        out = []
        for cat in categories:
            qs = recommend_by_onboarding(user, cat)[:5]
            data = self.get_serializer(qs, many=True).data
            out.extend(data)

        return Response(out)