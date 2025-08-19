from django.urls import path
from . import views
from .views import EnrollView

app_name = 'profiles'
urlpatterns = [
    path("profiles/enroll/",EnrollView.as_view(),name="profile-enroll"),

]