from rest_framework import serializers

class SpeechSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=200)
    audio = serializers.FileField(required=False)
