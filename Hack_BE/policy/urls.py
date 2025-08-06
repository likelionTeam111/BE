from django.urls import path
from .views import load_policies

app_name = 'load_policies'
urlpatterns = [ 
    path('',load_policies),
]