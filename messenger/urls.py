from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from .views import *

app_name = 'messenger'

urlpatterns = [
    path('message/create/', MessageCreateView.as_view()),
    path('message/all/', MessageListView.as_view()),
    path('message/user/<int:pk>', MessageListByUserView.as_view()),
    path('message/user/<str:username>', MessageListByUserView.as_view()),
    path('message/<int:pk>', MessageDetailedView.as_view()),
    path('user/list/', UserListView.as_view()),
]
