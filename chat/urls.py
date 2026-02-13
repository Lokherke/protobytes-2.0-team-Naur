from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.chat_message, name='chat_message'),
    path('history/<str:session_id>/', views.get_chat_history, name='get_chat_history'),
    path('clear/', views.clear_chat, name='clear_chat'),
]
