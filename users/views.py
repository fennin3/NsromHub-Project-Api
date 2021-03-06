from rest_framework import permissions
from users.models import Constituency, Region
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ConstituentRegisterSerializer, ConstituentSecondaryRegistration, MPRegisterSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView
from . import serializers
from rest_framework import status
from rest_framework.response import Response


User = get_user_model()

class ConstituentCreateApiView(CreateAPIView):
    serializer_class = ConstituentRegisterSerializer
    permission_classes=()
    


class MPCreateApiView(CreateAPIView):
    serializer_class = MPRegisterSerializer
    permission_classes=()


    

class UserLoginView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        u_name = serializer.data['username']
        user_ = User.objects.get(username=u_name)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            'id':user_.id,
            'email':user_.email,
            'username':user_.username,
            'full_name':user_.full_name,
            'is_constituent':user_.is_constituent,
            'is_mp':user_.is_mp,
            'contact':user_.contact,
            'date_of_birth':user_.date_of_birth,
            'system_id_for_user':user_.system_id_for_user



            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class SecondaryRegistration(UpdateAPIView):
    serializer_class = ConstituentSecondaryRegistration
    lookup_field = 'id'
    lookup_url_kwarg = "id"

    permission_classes= (permissions.AllowAny,)

    def update(self, request, *args, **kwargs):
        system_id_for_user = request.data['system_id_for_user']
        user = get_object_or_404(User, system_id_for_user=system_id_for_user)
        data = ""
        if user.constituency.count()>1:
            data = {
                "message":"You can not belong to more that 2 constituencies."
            }
        else:
            region = get_object_or_404(Region, id=request.data['region'])
            constituency = get_object_or_404(Constituency, id=request.data['constituency'])
            try:
                user.region.add(region)
                user.constituency.add(constituency)
            except:
                pass
            data = {
                "data":f"You are now a member of {constituency.name}."
            }
        
        return Response(data)