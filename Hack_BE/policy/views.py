from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.

from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

# chat봇 관련
import json
from uuid import uuid4

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .langchain import ai_chat
    
@method_decorator(csrf_exempt, name="dispatch")  # 운영에선 제거하고 CSRF 헤더/쿠키 사용 권장
class Chat(View):

    def post(self, request):
        # JSON 파싱
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({"error": "invalid json"}, status=400)

        # message
        message = payload.get("message").strip()
        if not message:
            return JsonResponse({"error": "message is required"}, status=400)

        # thread_id
        thread_id = (
            payload.get("thread_id")
            or getattr(getattr(request, "session", None), "session_key", None)
            or str(uuid4())
        )

        answer = ai_chat(message, thread_id)
        resp = JsonResponse(
            {"answer": answer, "thread_id": thread_id},
            json_dumps_params={"ensure_ascii": False},
        )
        # 선택: thread_id를 쿠키로 내려 프론트가 재사용하게
        if "thread_id" not in payload:
            resp.set_cookie("thread_id", thread_id, samesite="Lax")
        return resp
        
class Policy_list(generics.ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    pagination_class = PageNumberPagination