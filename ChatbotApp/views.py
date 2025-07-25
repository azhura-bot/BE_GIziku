import google.generativeai as genai
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import ChatSession, ChatMessage

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_gemini(request):
    user = request.user
    message = request.data.get('message')
    session_id = request.data.get('session_id')

    if not message:
        return Response({'error': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Ambil atau buat session
    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id, user=user)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Session not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        session = ChatSession.objects.create(
            user=user,
            title=f'Obrolan {ChatSession.objects.filter(user=user).count() + 1}'
        )

    # Simpan pesan user
    ChatMessage.objects.create(
        session=session,
        role='user',
        content=message
    )

    try:
        gemini_response = model.generate_content(message)
        reply = gemini_response.text.strip()

        # Simpan balasan Gemini
        ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=reply
        )

        return Response({
            'session_id': session.id,
            'reply': reply
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
