from rest_framework.response import Response
from superadmin_operations.models import GeneralOperationsSwitch
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class SwitchActionPlanOnOrOffView(APIView):
    permission_classes=()
    def post(self, request, id):
        try:
            user = User.objects.get(system_id_for_user=id)

            if user.is_superuser or user.is_staff:
                actionplan_switch = GeneralOperationsSwitch.objects.all().first()
                print(actionplan_switch)

                if actionplan_switch.open_action_plan:
                    actionplan_switch.open_action_plan = False
                    actionplan_switch.save()
                    data = {
                        "status":status.HTTP_200_OK,
                        "message":"Action plan has been closed."
                    }

                    return Response(data, status.HTTP_200_OK)
                else:
                    actionplan_switch.open_action_plan = True
                    actionplan_switch.save()

                    data = {
                        "status":status.HTTP_200_OK,
                        "message":"Action plan has been opened."
                    }
                    return Response(data, status.HTTP_200_OK)

            else:
                data = {
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message":"Sorry, You are not a superadmin."
                    }
                return Response(data, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            data = {
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Sorry, something went wrong."
                }
            return Response(data, status.HTTP_400_BAD_REQUEST)

class RetrieveActionPlanSwitchStatus(APIView):
    permission_classes=()
    def get(self, request):
        try:
            action_plan_switch = GeneralOperationsSwitch.objects.all().first()

            action_plan_status = action_plan_switch.open_action_plan

            data = {
                "status": status.HTTP_200_OK,
                "message":"Successful",
                "action_plan_status":action_plan_status
            }

            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            print(e)

            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message":"Sorry, something went wrong." 
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)


class RetrieveForumSwitchStatus(APIView):
    permission_classes=()
    def get(self, request):
        try:
            forumswitch = GeneralOperationsSwitch.objects.all().first()

            forum = forumswitch.open_forum

            data = {
                "status": status.HTTP_200_OK,
                "message":"Successful",
                "forum_status":forum
            }

            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            print(e)

            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message":"Sorry, something went wrong." 
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)



class RetrieveAssessmentSwitchStatus(APIView):
    permission_classes=()
    def get(self, request):
        try:
            assessmentswitch = GeneralOperationsSwitch.objects.all().first()

            assessment = assessmentswitch.open_assessment

            data = {
                "status": status.HTTP_200_OK,
                "message":"Successful",
                "assessment_status":assessment
            }

            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            print(e)

            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message":"Sorry, something went wrong." 
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)



