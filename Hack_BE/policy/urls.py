from django.urls import path
from .views import *

app_name = 'policy'
urlpatterns = [
    path('', Policy_list.as_view()),
    path("chat/", ChatView.as_view(), name="chat"),
    path("<int:id>/brief/", Brief_policy_info.as_view(), name="brief_info"),
    path("<int:id>/detail/", Detail_policy_info.as_view(), name="detail_info"),
    path("favorite/<int:policy_id>/post/", Favorite_policy_View.as_view(), name="favorite_post"),
    path("favorite/<int:policy_id>/delete/", Favorite_policy_View.as_view(), name="favorite_delete"),
    path("favorite/list/", Favorite_policy_list_View.as_view(), name="favorite_list"),
]