from django.urls import path
from .views import MyPageView
from .views import EnrollView
from . import views

app_name = 'profiles'
urlpatterns = [
    path("mypage/",MyPageView.as_view(),name="mypage"),
    path("enroll/",EnrollView.as_view(),name="enroll")

]