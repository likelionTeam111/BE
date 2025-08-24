from django.urls import path
from .views import Recommend_view, Profile_view, Enroll_view


app_name = 'profiles'
urlpatterns = [
    path("mypage/",Profile_view.as_view(),name="profile-mypage"),
    path("enroll/",Enroll_view.as_view(),name="profile-enroll"),
    path("update/",Enroll_view.as_view(),name="profile-update"),
    path("recommend/<str:category>/", Recommend_view.as_view()),
]