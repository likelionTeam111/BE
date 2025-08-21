from django.urls import path
from . import views
from .views import EnrollView,MyPageView

app_name = 'profiles'
urlpatterns = [
    path("mypage/",MyPageView.as_view(),name="profile-mypage"),
    path("enroll/",EnrollView.as_view(),name="profile-enroll"),

]