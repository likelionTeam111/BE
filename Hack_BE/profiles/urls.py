from django.urls import path
from . import views
from .views import EnrollView,MyPageView

app_name = 'profiles'
urlpatterns = [
    path("profiles/mypage/",MyPageView.as_view(),name="profile-mypage"),
    path("profiles/enroll/",EnrollView.as_view(),name="profile-enroll"),

]