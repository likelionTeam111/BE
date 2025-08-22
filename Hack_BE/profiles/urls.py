from django.urls import path
from .views import Recommend_view, Profile_view


app_name = 'profiles'
urlpatterns = [
    path("mypage/",Profile_view.as_view(),name="profile-mypage"),
    # path("enroll/",EnrollView.as_view(),name="profile-enroll"),
    path("recommend/", Recommend_view.as_view()),
]