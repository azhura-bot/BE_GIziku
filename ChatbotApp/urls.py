from django.urls import path
from .views import chat_with_gemini

urlpatterns = [
    path('chatbot/', chat_with_gemini, name='chat_with_gemini'),
]
