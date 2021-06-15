
# from constituent_operations.serializers import SendMessageSerializer
from constituent_operations.models import IncidentReport, Message, RequestForm
from rest_framework.response import Response
from rest_framework.views import APIView
from mp_operations.models import ActionPlanAreaSummaryForMp, Project, User
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import CreateProjectSerializer, ListConstituentsSerializer, ListProjectSerializer, \
    MPRetrieveAllSubAdminSerializer, RNRetrieveIncidentReportSerializer, RNRetrieveMessageSerializer, \
    RetrieveActionPlanSummaryEachAreaForMPSerializer, SearchConstituentsSerialiser, SearchProjectsSerialiser, \
    SendEmailSerializer, SendEmailToConstSerializer, SendMessageToConstituentSerializer, \
    RNRetrieveRequestFormSerializer, UserSerializer, PermissionSerializer, CreatePostSerializer
from users.models import Constituency, Constituent, Country, Town, Area, SubAdminPermission, Region, MpProfile, OTPCode, Permission, UserPermissionCust
from rest_framework import status
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from users.serializers import ConstituentRegisterSerializer, countryCode
from io import  BytesIO
from django.core.files.base import ContentFile
import requests
from users.utils import generate_OTP, generate_userID, send_sms, sending_mail
from constituent_operations.models import Assessment, ConductAssessment, ConductsForAssessment, ActionPlanToAssemblyMan
from django.db.models import Count, Sum, Q
from constituent_operations.serializers import  RetrieveMessageSerializer
from users.serializers import ListAllAreaSerializer



class CreateProjectView(CreateAPIView):
    serializer_class = CreateProjectSerializer
    permission_classes = ()
    lookup_field = 'id'
    lookup_url_kwarg = "id"
    
    def create(self, request):
        print("------------------------------------")
        print(request.data)
        user_id = request.data['user_id']

        try:
            user = User.objects.get(system_id_for_user=user_id)
        except Exception:
            pass

        project = Project.objects.create(
            mp = user,
            name = request.data['name'],
            place = request.data['place'],
            media = request.data['media'],
            description = request.data['description']
        )
        print("------------------------------------")

        project.save()

   
        return Response(
            {
                "status":status.HTTP_200_OK,
                "message":"Project has been created successfully."
            }
        )


class ListProjectView(ListAPIView):
    serializer_class = ListProjectSerializer
    queryset=Project.objects.all()
    permission_classes = ()


    def list(self, request, id):
        projects = Project.objects.filter(mp__system_id_for_user=id)

        len(projects)

        data = ListProjectSerializer(projects, many=True).data
        data = {
            'projects':data
        }
        return Response(data, status=status.HTTP_200_OK)

# customized for data tabke search
class CustomListProjectView(APIView):
    serializer_class = ListProjectSerializer
    queryset=Project.objects.all()
    permission_classes = ()


    def post(self, request, id):
        projects = Project.objects.filter(mp__system_id_for_user=id, is_post=False)

        len(projects)

        data = ListProjectSerializer(projects, many=True).data

        data = {
            'data':data
        }
        return Response(data, status=status.HTTP_200_OK)

# customised for data table search
class ListConstituentsForMpView(APIView):
    serializer_class = ListConstituentsSerializer
    queryset=Project.objects.all()
    permission_classes = ()


    def post(self, request, id):
        user = User.objects.get(system_id_for_user=id)
        constituency = user.active_constituency

        data = ListConstituentsSerializer(constituency.members, many=True).data

        data = {
            'data':data
        }
        return Response(data,status=status.HTTP_200_OK)


class SendEmailView(APIView):
    permission_classes = ()

    def post(self, request):
        
        try:
            data = SendEmailSerializer(data=request.data)

            data.is_valid(raise_exception=True)

            user_id = data['user_id'].value
            subject = data['subject'].value
            message = data['message'].value
            attached_file = data['attached_file']

            mp = User.objects.get(system_id_for_user=user_id)

            constituency = mp.active_constituency

            emails = []

            
            for user in constituency.members.all():
                emails.append(user.email)



            print(emails)

            mail = EmailMessage(
                subject,
                message,
                'rennintech.com',
                emails
            )

            

            if request.data['attached_file']:
                attached_file=request.data['attached_file']
                mail.attach(attached_file.name, attached_file.read(), attached_file.content_type)
            
            mail.send()
            data = {
                "message":"Email has been sent successfully"
            }
        except Exception as e:
            
            data = {
                "message":f"Sorry something went wrong, try again. {e}"
            }

        return Response(data, status=status.HTTP_200_OK)

        
class ProjectsSearchEngineView(ListAPIView):
    permission_classes = ()
    def list(self, request, id, query):
        projects = Project.objects.filter(mp__system_id_for_user=id, name__icontains=query)       
        data = SearchProjectsSerialiser(projects, many=True)
        return Response({
            "results":data.data},
            status=status.HTTP_200_OK
        )

class ConstituentsSearchEngineView(ListAPIView):
    permission_classes = ()
    def list(self, request, constituency, query):
        constituency = Constituency.objects.get(id=constituency)
        constituents = constituency.members.all()

        data = []
        for i in constituents:
            if query.lower() in i.full_name.lower():
                data.append(i)
        
        data = SearchConstituentsSerialiser(data, many=True)

        return Response({
            "results":data.data},
            status=status.HTTP_200_OK
        )


class RetrieveIncidentReportView(APIView):
    permission_classes=()
    def get(self, request, id):
        incident_reports = IncidentReport.objects.filter(receiver__system_id_for_user=id)
        data = RNRetrieveIncidentReportSerializer(incident_reports,many=True)

        # data.is_valid(raise_exception=True)
        
        data = {
            "data":data.data
        }

        return Response(data)
    

class RetrieveMessageView(APIView):
    permission_classes=()
    def get(self, request, id):
        incident_reports = Message.objects.filter(receiver__system_id_for_user=id)
        data = RNRetrieveMessageSerializer(incident_reports,many=True)

        # data.is_valid(raise_exception=True)
        
        data = {
            "data":data.data
        }

        return Response(data)
        

class RetrieveRequestNotificationsView(APIView):
    permission_classes=()
    def get(self, request, id):

        incident_reports = IncidentReport.objects.filter(receiver__system_id_for_user=id)
        incident_reports = RNRetrieveIncidentReportSerializer(incident_reports,many=True)


        messages = Message.objects.filter(receiver__system_id_for_user=id)
        messages = RNRetrieveMessageSerializer(messages,many=True)

        requestform = RequestForm.objects.filter(receiver__system_id_for_user=id)
        requestform = RNRetrieveRequestFormSerializer(requestform,many=True)


        data = {
            "messages":messages.data,
            "incident_reports":incident_reports.data,
            "request_form":requestform.data,
            "status":status.HTTP_200_OK

        }

        return Response(data)



class RetrieveAllSubAdminsView(APIView):
    permission_classes=()
    def post(self, request, id):
        try:
            mp = User.objects.get(system_id_for_user=id)
            sub_admins = mp.sub_admins.all()

            data = MPRetrieveAllSubAdminSerializer(sub_admins,many=True)

            print(data.data)
            data = {
                "status":status.HTTP_200_OK,
                "data":data.data
            }
        except Exception as e:
            print(e)
            data = {
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message":"Sorry, something went wrong."
            }
            
        return Response(data, status=status.HTTP_200_OK)


class SendMessageToContView(APIView):
    permission_classes = ()

    def post(self, request):
        try:
            data = SendMessageToConstituentSerializer(data=request.data)

            data.is_valid(raise_exception=True)

            receiver = data['receiver_id'].value
            sender = data['sender_id'].value

            receiver = User.objects.get(system_id_for_user=receiver)
            sender = User.objects.get(system_id_for_user=sender)

            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                message=data['message'].value,
                attached_file = data['attached_file'].value
            )

            message.save()

            data = {
                "status":status.HTTP_200_OK,
                "message":"Message has been sent successfully."
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            data = {
                "status":status.status.HTTP_400_BAD_REQUEST,
                "message":"Message was not sent successfully."
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class SendEmailToConstView(APIView):
    permission_classes=()

    def post(self, request):
        try:
            data = SendEmailToConstSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            sender = data['sender_id'].value
            receiver = data['receiver_id'].value
            subject = data['subject'].value
            message = data['message'].value
            

            sender = User.objects.get(system_id_for_user=sender)
            receiver = User.objects.get(system_id_for_user=receiver)



            mail = EmailMessage(
                f"{subject} - Email from {sender.full_name} (MP)",
                message,
                'rennintech.com',
                [receiver.email]
            )


            if request.data["attached_file"]:
                
                attached_file = request.data["attached_file"]

                mail.attach(attached_file.name, attached_file.read(), attached_file.content_type)
            else:
                print("--------------------------------------")
                print("NOT Adding file")
                print(request.data)
            
            mail.send()

            data = {
                "status":status.HTTP_200_OK,
                "message":f"Email has been sent to {receiver.full_name}"
            }

            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            data = {
                "status":status.HTTP_400_BAD_REQUEST,
                "message":f"Email was not sent {receiver.full_name}"
            }

            return Response(data, status.HTTP_400_BAD_REQUEST)    

class RetrieveActionPlanSummaryEachAreaForMPView(APIView):
    permission_classes=()

    def get(self, request, id, date):
        user = User.objects.get(system_id_for_user=id)


        action_plans = ActionPlanAreaSummaryForMp.objects.filter(date__year=date, area=user.active_area, constituency=user.active_constituency)

        print(action_plans)

        data = RetrieveActionPlanSummaryEachAreaForMPSerializer(action_plans, many=True)

        

        data = {
            "status":status.HTTP_200_OK,
            "data":data.data
        }

        return Response(data, status.HTTP_200_OK)

# Unconsumed endpoints.....................................
class MakeSubAdminView(APIView):
    permission_classes = ()
    def post(self, request, id, subadmin_id):
        print(id)
        print(subadmin_id)
    
        try:
            mp = User.objects.get(system_id_for_user=id)
            const = Constituent.objects.get(user__system_id_for_user=subadmin_id)

            const.is_subadmin=True
            const.user.is_subadmin=True
            const.user.subadmin_for=mp.user.active_constituency
            const.subadmin_for=mp

            const.save()

            permissions = SubAdminPermission.objects.create(
                sub_admin=const,
                sub_admin_for=mp.mp_profile
            )

            data = {
                "status":status.HTTP_200_OK,
                "message":f"{const.user.full_name} is now your sub-admin."
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            data = {
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message":"Sorry something went wrong, try again."
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UnmakeSubAdmin(APIView):
    permission_classes = ()

    def post(self, request, id, subadmin_id):
        const = Constituent.objects.get(user__system_id_for_user=subadmin_id)
        mp = MpProfile.objects.get(user__system_id_for_user=id)

        sub = SubAdminPermission.objects.get(
            sub_admin=const,
            sub_admin_for=mp
        )
        sub.delete()

        const.is_subadmin=False
        const.user.is_subadmin=False

        const.subadmin_for = None
        const.save()

        data = {
            "status":status.HTTP_200_OK,
            "message":f"{const.user.full_name} is no more your subadmin."
        }

        return Response(data, status.HTTP_200_OK)

# customize email content to allow email verifivation
class CreateUserAccountForOtherView(CreateAPIView):
    queryset=User.objects.all()
    serializer_class = ConstituentRegisterSerializer
    permission_classes=()

    def create(self, request, id, type_):
        country = get_object_or_404(Country, id=request.data['country'])
        region = get_object_or_404(Region, id=request.data['region'])
        constituency = get_object_or_404(Constituency, id=request.data['constituency'])
        town = get_object_or_404(Town, id=request.data['town'])
        area = get_object_or_404(Area, id=request.data['area'])
        mp = User.objects.get(system_id_for_user=id)

    

        CD = countryCode[country.name]
        system_id_for_user =""

        while True:
            nums = generate_userID()
            system_id_for_user = str(CD)+str(nums)
            user = User.objects.filter(system_id_for_user=system_id_for_user)

            if user.exists():
                pass
            else:
                system_id_for_user = system_id_for_user
                break

        
        email = request.data['email']
        contact = request.data['contact']
        if User.objects.filter(email=email).exists():
            return Response({
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message":"Email already exist"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif User.objects.filter(contact=contact).exists():
            return Response({
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message":"Contact already exist"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif len(str(request.data['date_of_birth'])) < 1 or request.data['date_of_birth']=="null":
            return Response({
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message":"Date of birth is required."
            })
        elif len(str(request.data['voters_id'])) < 1 or request.data['voters_id']=="null":
            return Response({
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message":"Voter's ID is required."
            })
        
        else:
        
        # Creating User and Constituency Profile
            try:
                otp_code = generate_OTP()

                otp = OTPCode.objects.create(code_for=request.data['email'],code=otp_code)
                otp.save()
                sending_mail(f"Hello {request.data['full_name']}\nThis is your verification code: {otp_code}","NsromaHub Account email verification", request.data['email'])


                if type_.lower() == 'subadmin':
                    user = User.objects.create(
                    email=request.data['email'],
                    # username=validated_data['username'],
                    full_name=request.data['full_name'],
                    date_of_birth=request.data['date_of_birth'],
                    contact=request.data['contact'],
                    country=country,
                    # is_superuser=request.data['is_superuser'],
                    is_constituent = True,
                    system_id_for_user=system_id_for_user,
                    is_active=True,
                    active_constituency=constituency,
                    is_subadmin=True,
                    subadmin_for=mp.active_constituency
                    )

                    user.set_password(request.data['password'])
                    user.save()

                    user.constituency.add(constituency)
                    user.region.add(region)


                    constituent = Constituent(
                        user = user,
                        voters_id = request.data['voters_id'],
                        is_subadmin = True,
                        subadmin_for = mp
                    )

                    constituent.save()

                    constituent.town.add(town)
                    constituent.area.add(area)

                    constituent.save()

                    permissions = SubAdminPermission.objects.create(
                        sub_admin = constituent,
                        sub_admin_for=mp.mp_profile
                    )

                    permissions.save()

                    return Response({
                    "status":status.HTTP_201_CREATED,
                    "message":"SubAdmin Account registration is successful",
                    "email":user.email
                    }, status=status.HTTP_201_CREATED)

                elif type_.lower() == 'security':
                    user = User.objects.create(
                    email=request.data['email'],
                    # username=validated_data['username'],
                    full_name=request.data['full_name'],
                    date_of_birth=request.data['date_of_birth'],
                    contact=request.data['contact'],
                    country=country,
                    # is_superuser=request.data['is_superuser'],
                    is_constituent = True,
                    system_id_for_user=system_id_for_user,
                    is_active=True,
                    active_constituency=constituency,
                    is_security_person =True
                    )

                    user.set_password(request.data['password'])
                    user.save()

                    user.constituency.add(constituency)
                    user.region.add(region)


                    constituent = Constituent(
                        user = user,
                        voters_id = request.data['voters_id'],
                    )

                    constituent.save()

                    constituent.town.add(town)
                    constituent.area.add(area)

                    constituent.save()

                    return Response({
                    "status":status.HTTP_201_CREATED,
                    "message":"Account registration is successful",
                    "email":user.email
                    }, status=status.HTTP_201_CREATED)

                
                elif type_.lower() == 'assemblyman':
                    user = User.objects.create(
                    email=request.data['email'],
                    # username=validated_data['username'],
                    full_name=request.data['full_name'],
                    date_of_birth=request.data['date_of_birth'],
                    contact=request.data['contact'],
                    country=country,
                    # is_superuser=request.data['is_superuser'],
                    is_constituent = True,
                    system_id_for_user=system_id_for_user,
                    is_active=True,
                    active_constituency=constituency,
                    is_assembly_man =True
                    )


                    user.set_password(request.data['password'])
                    user.save()

                    user.constituency.add(constituency)
                    user.region.add(region)


                    constituent = Constituent(
                        user = user,
                        voters_id = request.data['voters_id'],
                    )

                    constituent.save()

                    constituent.town.add(town)
                    constituent.area.add(area)

                    constituent.save()

                    return Response({
                    "status":status.HTTP_201_CREATED,
                    "message":"Assembly Man Account registration is successful",
                    "email":user.email
                    }, status=status.HTTP_201_CREATED)


                elif type_.lower() == 'medical_center':
                    user = User.objects.create(
                    email=request.data['email'],
                    # username=validated_data['username'],
                    full_name=request.data['full_name'],
                    date_of_birth=request.data['date_of_birth'],
                    contact=request.data['contact'],
                    country=country,
                    # is_superuser=request.data['is_superuser'],
                    is_constituent = True,
                    system_id_for_user=system_id_for_user,
                    is_active=True,
                    active_constituency=constituency,
                    is_medical_center =True
                    )


                    user.set_password(request.data['password'])
                    user.save()

                    user.constituency.add(constituency)
                    user.region.add(region)


                    constituent = Constituent(
                        user = user,
                        voters_id = request.data['voters_id'],
                    )

                    constituent.save()

                    constituent.town.add(town)
                    constituent.area.add(area)

                    constituent.save()

                    return Response({
                    "status":status.HTTP_201_CREATED,
                    "message":"Medical Center Account registration is successful",
                    "email":user.email
                    }, status=status.HTTP_201_CREATED)

                
                else:
                    user = User.objects.create(
                    email=request.data['email'],
                    # username=validated_data['username'],
                    full_name=request.data['full_name'],
                    date_of_birth=request.data['date_of_birth'],
                    contact=request.data['contact'],
                    country=country,
                    # is_superuser=request.data['is_superuser'],
                    is_constituent = True,
                    system_id_for_user=system_id_for_user,
                    is_active=True,
                    active_constituency=constituency,
                    )

                

                    user.set_password(request.data['password'])
                    user.save()

                    user.constituency.add(constituency)
                    user.region.add(region)


                    constituent = Constituent(
                        user = user,
                        voters_id = request.data['voters_id'],
                    )

                    constituent.save()

                    constituent.town.add(town)
                    constituent.area.add(area)

                    constituent.save()

                    return Response({
                    "status":status.HTTP_201_CREATED,
                    "message":"Account registration is successful",
                    "email":user.email
                    }, status=status.HTTP_201_CREATED)
                    
                    


            except Exception as e:
                print(e)

                return Response({
                    "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message":"Something went wrong, check your internet connection and try again.",
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetPermissionsForSubAdmin(APIView):
    permission_classes=()

    def post(self, request, subadmin_id):
        data = PermissionSerializer(request.data).data
        perm_name = data['perm_name']
        perm_value = data['perm_value']

        print("----------------------------")
        print(request.data)
        print("----------------------------")
        user = User.objects.get(system_id_for_user=subadmin_id)


        try:

            perm = UserPermissionCust.objects.get(user=user, permission_name=perm_name)

        

            print(perm.permission_value)
            perm.permission_value = perm_value

            perm.save()

            print(perm.permission_value)

        except Exception as e:
            perm = UserPermissionCust.objects.create(user=user, permission_name=perm_name, permission_value=perm_value)

            perm.save()

        

        data = {
            "status":status.HTTP_200_OK,
            "message":f"{perm_name} status changed to {perm_value}"
        }
        return Response (data,status=status.HTTP_200_OK)

        
class RetrievePermissionsOfSubAdmin(APIView):
    permission_classes=()          


class AllUsersInACountry(APIView):
    permission_classes = ()

    def get(self, request, country):
        users = User.objects.filter(country=country)
        data = UserSerializer(users, many=True)
        return Response ({
            "status":status.HTTP_200_OK,
            "data":data.data
        }, status=status.HTTP_200_OK)


class ShareAsPostView(APIView):
    permission_classes=()

    def post(self, request, id):
        user = User.objects.get(system_id_for_user=id)


        area = request.data['area']

        image = requests.get(request.data['image']).content

        title = f"{area} Action Plan Summary"

        comment = request.data['comment']

        image = ContentFile(image)

        project = Project.objects.create(
            mp = user,
            name = title,
            description = comment,
            place = area,
            is_post=True
        )

        project.media.save("shared_data.jpg", image)

        project.save()


        data = {
            "status":status.HTTP_200_OK,
            "message":f"{area} Action Plan Summary has been shared."
        }

        return Response(data,status=status.HTTP_200_OK)

class ShareAllAtOnce(APIView):
    permission_classes=()

    def post(self, request, id, date):
        user = User.objects.get(system_id_for_user=id)

        action_plans = ActionPlanAreaSummaryForMp.objects.filter(date__year=date, area=user.active_area, constituency=user.active_constituency)
        data = RetrieveActionPlanSummaryEachAreaForMPSerializer(action_plans, many=True)


        print("**********************************")
        print(data.data)


        for action_plan in data.data:
            area = action_plan['area']['name']

            image = requests.get(str(action_plan['image'])).content

            title = f"{area} Action Plan Summary"

            # comment = request.data['comment']

            image = ContentFile(image)

            project = Project.objects.create(
                mp = user,
                name = title,
                # description = ,
                place = area,
                is_post=True
            )

            project.media.save("shared_data.jpg", image)

            project.save()


        data = {
            "status":status.HTTP_200_OK,
            "message":f"Action Plan Summaries has been shared."
        }

        return Response(data,status=status.HTTP_200_OK)


class RetrieveAssessmentView(APIView):
    permission_classes=()

    def get(self, request, id, year):
        user = User.objects.get(system_id_for_user=id)
        const = user.active_constituency
        # project_names

        options_ = ['Good','Excellent', "Very Good", 'Average', 'Poor']

        data_projects = []

        projects = Project.objects.filter(mp=user, date_posted__year=year, is_post=False)
        conds = ConductsForAssessment.objects.all()
        

        for project in projects:
            assessments = Assessment.objects.filter(constituency=const, date__year=year, project=project).values('assessment').annotate(total_num=Count('assessment'))
            print(assessments)

            ass_names = []
            ass_value = []

            
            for i in assessments:
                ass_names.append(i['assessment'])
                ass_value.append(i['total_num'])

            for k in options_:
                if k not in ass_names:
                    ass_names.append(k)
                    ass_value.append(0)

        

            data_projects.append({
                "id":project.id,
                "project_title":f"{project.name} at {project.place} on {project.date_posted.strftime('%d %b, %Y')}",
                "assessement_names":ass_names,
                "assessment_values":ass_value
            })




        
        data_conduct=[]

        for i in conds:
            
            cond_ass = ConductAssessment.objects.filter(constituency=const, conduct=i.title).values('assessment').annotate(total_num=Count('assessment'))

            cond_names =[]
            cond_value=[]
            for j in cond_ass:    
                cond_names.append(j['assessment'])
                cond_value.append(j['total_num'])

            
            for k in options_:
                if k not in cond_names:
                    cond_names.append(k)
                    cond_value.append(0)


            data_conduct.append(
                {
                "id":i.id,
                "conduct":i.title,
                "assessment_names":cond_names,
                "assessment_value":cond_value
                }
            )

            
        

        
        return Response({
            "status":status.HTTP_200_OK,
            "projects_assessment":data_projects,
            "conduct_assessment": data_conduct
        })

class CreatePostView(APIView):
    permission_classes=()

    def post(self, request):
        data = CreatePostSerializer(request.data)

        print('----')

        print(data)
        image = None

        caption = data.data['caption']
        try:
            if request.data['media']:
                image = request.data['media']
        except Exception as e:
            print(e)
        id = data.data['user_id']
        try:
            user = User.objects.get(system_id_for_user=id)


            post = Project.objects.create(
            mp=user,
            description=caption,
            media = image,
            is_post=True
            )

            post.save()

            data= {
            "status":status.HTTP_200_OK,
            "message":"You post has been created."
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response()

class RetrieveActionPlanOverview(APIView):
    permission_classes=()

    def get(self, request, id, year):
        user = User.objects.get(system_id_for_user=id)
        const = user.active_constituency

        action_plan = ActionPlanToAssemblyMan.objects.filter(constituency=const, date__year=year).values("problem_title").annotate(total_rating=Sum('total_rating'))
        print(action_plan)
        problem_title=[]
        total_rating=[]
        for i in action_plan:
            problem_title.append(i['problem_title'])
            total_rating.append(i['total_rating'])

    
        return Response({
            "status":status.HTTP_200_OK,
            "data":{
                "problem_titles":problem_title,
                "total_ratings":total_rating
                
            }
        }, status=status.HTTP_200_OK)


class RetrieveMessages(APIView):
    permission_classes = ()
    def get(self, request, id, consti):
        try:
            mp = User.objects.get(system_id_for_user=id)
            consti = User.objects.get(system_id_for_user=consti)

            # const = mp.active_constituency

            messages = Message.objects.filter(Q(sender=mp) & Q(receiver=consti) | Q(sender=consti) & Q(receiver=mp))

            
            data = RetrieveMessageSerializer(messages, many=True)
            # data.is_valid(raise_exception=True)

            data = {
                "status":status.HTTP_200_OK,
                "this":len(data.data),
                "messages":data.data
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            return Response()


class SetRequestFormRead(APIView):
    permission_classes=()
    def post(self, request, id):
        rf = RequestForm.objects.get(id=id)

        rf.read = True
        rf.save()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"marked as read"
        }
        )



class SetIncidentReportRead(APIView):
    permission_classes=()
    def post(self, request, id):
        rf = IncidentReport.objects.get(id=id)

        rf.read = True
        rf.save()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"marked as read"
        }
        )


class GetProjectDetail(APIView):
    permission_classes=()
    def get(self, request, id):
        try:
            project= Project.objects.get(id=id)

            data = ListProjectSerializer(project)

            return Response(
                {
                    "status":status.HTTP_200_OK,
                    "data":data.data
                }
            )
        except Exception:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Sorry something went wrong."
                }
            )

class GetAreasForMP(APIView):
    permission_classes=()

    def get(self, request, id):
        areas = []
        try:
            mp  = User.objects.get(system_id_for_user=id)
            const = mp.active_constituency
            towns  = const.towns.all()

            for town in towns:
                areas = areas + list(town.areas.all())


            areas  = ListAllAreaSerializer(areas, many=True).data
        
            return Response(
                {
                "status":status.HTTP_200_OK,
                "areas": areas      
                },
                status=status.HTTP_200_OK
            )   
        except Exception as e:
            print(e)
            return Response(
                {
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "Sorry something went wrong."      
                },
                status=status.HTTP_400_BAD_REQUEST
            )   
            

class SendEmailToAreaView(APIView):
    permission_classes = ()
    def post(self, request, areaid):
        
        try:
            data = SendEmailSerializer(data=request.data)

            data.is_valid(raise_exception=True)

            # user_id = data['user_id'].value///////////////////////
            subject = data['subject'].value
            message = data['message'].value
            attached_file = data['attached_file']

            area = Area.objects.get(id=areaid)



            emails = [user.user.email for user in area.members.all()]

            print(emails)

            mail = EmailMessage(
                subject,
                message,
                'rennintech.com',
                emails
            )

            

            if request.data['attached_file']:
                attached_file=request.data['attached_file']
                mail.attach(attached_file.name, attached_file.read(), attached_file.content_type)
            
            mail.send()
            data = {
                "message":"Email has been sent successfully"
            }
        except Exception as e:
            
            data = {
                "message":f"Sorry something went wrong, try again. {e}"
            }

        return Response(data, status=status.HTTP_200_OK)
