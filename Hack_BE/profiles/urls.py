from django.urls import path
from .views import EnrollView, MyPageView, Recommend_view, Profile_view


app_name = 'profiles'
urlpatterns = [
    path("mypage/",MyPageView.as_view(),name="profile-mypage"),
    path("enroll/",EnrollView.as_view(),name="profile-enroll"),
    path("enroll/",EnrollView.as_view(),name="profile-enroll"),
    path("recommend/", Recommend_view.as_view()),
    path("<int:id>/", Profile_view.as_view()),
]