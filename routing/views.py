from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
import os
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import get_user_model
from users.models import UserPermissionCust, Permission

User = get_user_model()

path_ = os.getcwd()




arr = [
    'home',
    'about',
    'incident',
    'dashboard',
    'action-assemblyman',
    'sidebar',
    'create-project',
    'view-projects',
    'constituents',
    'incident',
    'request',
    'send-email',
    'view-admins',
    'get_permissions',
    'action-mp',
    'add-admin',
    'accounts',
    'assessment',
    'summary-action-plan',
    'summary-assessment'
]



class WebPageView(APIView):
    permission_classes = ()
    renderer_classes = [TemplateHTMLRenderer]
    def post(self, request, id):
        call_ = request.data['page_name']
        print(call_ in arr)
        user = User.objects.get(system_id_for_user=id)

        all_permissions = Permission.objects.all()

        try:
            permission = UserPermissionCust.objects.filter(user__system_id_for_user=id)
        except Exception as e:
            permission = "null"

        if call_ in arr:

            
            try:
                
                data = {
                    'id':id,
                    'user':user,
                    "permission":permission,
                    "all_permissions":all_permissions
                }
                
                return Response(data, template_name=f"routing/{call_}.html")

            except Exception as e:
                print(e)
                data = {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Sorry, something went wrong."
                }
                
                return Response(data, status.HTTP_400_BAD_REQUEST)
        else:
            
          
            data ={
                "status":status.HTTP_400_BAD_REQUEST,
                "page":"Page not found"
            }
            return Response(data, template_name="")


class SideBarView(APIView):
    permission_classes = ()
    renderer_classes = [TemplateHTMLRenderer]
    def post(self, request, id):
        call_ = request.data['page_name']
        print(call_ in arr)
        user = User.objects.get(system_id_for_user=id)

        if call_ in arr:
            try:
                
                data = {
                    "id":id,
                    "user":user,
                    "is_constituent":user.is_constituent,
                    "is_mp":user.is_mp,
                    "is_assemblyman":user.is_assembly_man,
                    "is_subadmin": user.is_subadmin
                }
                
                return Response(data, template_name=f"routing/{call_}.html")

            except Exception as e:
                print(e)
                data = {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Sorry, something went wrong."
                }
                
                return Response(data, status.HTTP_400_BAD_REQUEST)
        else:
            
          
            data ={
                "status":status.HTTP_400_BAD_REQUEST,
                "page":"Page not found"
            }
            return Response(data, template_name="")



        
