from django.urls import path
from .views import *
from .services import load_policies

app_name = 'policy'
urlpatterns = [
    path('', Policy_list.as_view()),
    path('load/',load_policies),
]