from django.http import JsonResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import speech_recognition as sr
import pyttsx3
import os

# Text-to-Speech (TTS) View
class TextToSpeechView(APIView):
    def post(self, request, *args, **kwargs):
        text = request.data.get('text')
        if not text:
            return Response({"error": "No text provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Set up pyttsx3 engine
        engine = pyttsx3.init()
        audio_file_path = "tts_output.mp3"  # Output file path
        engine.save_to_file(text, audio_file_path)  # Save speech to file
        engine.runAndWait()
        
        # Send the generated audio file to the browser
        if os.path.exists(audio_file_path):
            return FileResponse(open(audio_file_path, 'rb'), content_type='audio/mpeg')
        else:
            return Response({"error": "Failed to generate speech."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Speech-to-Text (STT) View
class SpeechToTextView(APIView):
    def post(self, request, *args, **kwargs):
        recognizer = sr.Recognizer()
        audio_file = request.FILES.get('audio')
        
        if not audio_file:
            return Response({"error": "No audio file provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return Response({"text": text}, status=status.HTTP_200_OK)
            except sr.UnknownValueError:
                return Response({"error": "Could not understand the audio."}, status=status.HTTP_400_BAD_REQUEST)
            except sr.RequestError:
                return Response({"error": "Speech recognition service error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
