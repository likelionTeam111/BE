from django.urls import path
from .views import *

app_name = 'policy'
urlpatterns = [
    path('', Policy_list_view.as_view()),
    path("chat/", Chat_view.as_view(), name="chat"),
    path("chat/<int:policy_id>/", Detail_chat_view.as_view(), name="detail_chat"),
    path("info/<int:id>/", Policy_info_view.as_view(), name="policy_info"),
    path("search/", Policy_search_view.as_view(), name="search"),
    path("favorite/<int:policy_id>/post/", Favorite_policy_view.as_view(), name="favorite_post"),
    path("favorite/<int:policy_id>/delete/", Favorite_policy_view.as_view(), name="favorite_delete"),
    path("favorite/list/", Favorite_policy_list_view.as_view(), name="favorite_list"),
]