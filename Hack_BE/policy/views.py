from .models import *
from .serializers import *

from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# # chat봇 관련
from uuid import uuid4
from .langchain import ai_chat
    
class Chat_view(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data["message"].strip()
        thread_id = serializer.validated_data.get("thread_id") or str(uuid4())
                    # request.COOKIES.get("thread_id") or \
                    # getattr(getattr(request, "session", None), "session_key", None) or \
                    
        answer = ai_chat(message, thread_id)

        resp_serializer = ChatResponseSerializer({
            "answer": answer,
            "thread_id": thread_id
        })

        return Response(resp_serializer.data, status=status.HTTP_200_OK)
    
class Detail_chat_view(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        policy_id = kwargs.get("policy_id")
        policy = get_object_or_404(Policy, id=policy_id)
        
        provided_thread_id = serializer.validated_data.get("thread_id")
        is_first_turn = not bool(provided_thread_id)
        thread_id = serializer.validated_data.get("thread_id") or str(uuid4())
        
        message = ""
        if is_first_turn:
            about = policy.plcyNm
            message += f"{about}에 관한 챗봇이야 \n"
        message += (serializer.validated_data.get("message") or "").strip()
        
        answer = ai_chat(message, thread_id)

        resp_serializer = ChatResponseSerializer({
            "answer": answer,
            "thread_id": thread_id,
        })
        
        return Response(resp_serializer.data, status=status.HTTP_200_OK)
    
class Policy_list_view(generics.ListAPIView):
    # 참고용
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    pagination_class = PageNumberPagination

class Policy_info_view(generics.RetrieveAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicyInfoSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

class Favorite_policy_view(generics.GenericAPIView):
    #관심정책
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        policy_id = kwargs.get("policy_id")
        policy = get_object_or_404(Policy, id=policy_id)
        serializer = FavoriteSerializer(data={})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, policy=policy)
            return Response(status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        policy_id = kwargs.get("policy_id")
        policy = get_object_or_404(Policy, id=policy_id)
        favorite = get_object_or_404(Favorite_policy, user = request.user, policy = policy)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Favorite_policy_list_view(generics.ListAPIView):
    # 마이페이지
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteListSerializer
    pagination_class = None
    
    def get_queryset(self):
        return Policy.objects.filter(
            id__in=Favorite_policy.objects.filter(user=self.request.user).values_list('policy_id', flat=True)
        )