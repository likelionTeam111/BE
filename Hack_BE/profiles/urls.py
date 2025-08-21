from django.urls import path
from .views import EnrollView, Recommend_view, Profile_view

app_name = 'profiles'
urlpatterns = [
    path("enroll/",EnrollView.as_view(),name="profile-enroll"),
    path("recommend/", Recommend_view.as_view()),
    path("<int:id>/", Profile_view.as_view())
]