from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SendMessageViaMicroServiceSerializer
from django.contrib.auth import  get_user_model
from constituent_operations.models import Message
from rest_framework.response import Response
from rest_framework import  status

User = get_user_model()


class SendMessageViaMicroServiceView(APIView):
    permission_classes=()

    def post(self, request):
        data = SendMessageViaMicroServiceSerializer(request.data).data

        sender = data['sender']
        receiver = data['receiver']
        message = data['message']
        attached_file= data['attached_file']


        sender = User.objects.get(system_id_for_user=sender)
        receiver=User.objects.get(system_id_for_user=receiver)


        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            message=message,
            attached_file=attached_file,
            )


        message.save()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Message has been sent"
        }, 
        status=status.HTTP_200_OK
        )