from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.

from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


# embedding 관련
from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class Policy_list(generics.ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    pagination_class = PageNumberPagination

model = SentenceTransformer('jhgan/ko-sbert-sts')
class SimilarPolicySearch(APIView):
    def get(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response({"error": "검색어(q)를 입력하세요."}, status=400)

        try:
            # 1. 사용자 질문 임베딩
            query_embedding = model.encode(query)

            # 2. pgvector 유사도 검색
            results = Policy.objects.annotate(
                similarity=CosineDistance("embedding", query_embedding)
            ).order_by("similarity")[:5]

            # 3. 직렬화
            serializer = PolicySerializer(results, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
