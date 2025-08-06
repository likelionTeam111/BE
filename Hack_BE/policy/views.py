from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.

from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class Policy_list(generics.ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    pagination_class = PageNumberPagination

