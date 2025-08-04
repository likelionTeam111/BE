from django.urls import path

from .views import Policy

app_name = 'policy'
urlpatterns = [ 
    path('',Policy),
]