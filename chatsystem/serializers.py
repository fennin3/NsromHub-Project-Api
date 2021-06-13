from rest_framework import  serializers
from constituent_operations.models import Message


class SendMessageViaMicroServiceSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(max_length=15)
    receiver = serializers.CharField(max_length=15)
    class Meta:
        model=Message
        fields=["sender","receiver","message","attached_file"]