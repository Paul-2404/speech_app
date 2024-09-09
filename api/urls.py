from django.urls import path
from .views import TextToSpeechView, SpeechToTextView

urlpatterns = [
    path('text-to-speech/', TextToSpeechView.as_view(), name='text-to-speech'),
    path('speech-to-text/', SpeechToTextView.as_view(), name='speech-to-text'),
]
