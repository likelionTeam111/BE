from django.urls import path
from .views import *

app_name = 'policy'
urlpatterns = [
    path('', Policy_list.as_view()),
]