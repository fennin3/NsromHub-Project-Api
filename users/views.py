from constituent_operations.serializers import ConstituencySerializer
from users.utils import generate_OTP, generate_userID, send_sms, sending_mail
from rest_framework import permissions
from users.models import Area, Constituency, Constituent, Country, MpProfile, OTPCode, Region, Town, Permission, UserPermissionCust
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import ConstituentRegisterSerializer, ConstituentSecondaryRegistration, GetOTPSMSSerializer, ListAllAreaSerializer, ListAllCountriesSerializer, ListAllTownsSerializer, MPRegisterSerializer, OTPVerificationEmailSerializer, OTPVerificationSMSSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from . import serializers
from rest_framework import status
from rest_framework.response import Response
from .serializers import countryCode


User = get_user_model()

class ConstituentCreateApiView(CreateAPIView):
    queryset=User.objects.all()
    serializer_class = ConstituentRegisterSerializer
    permission_classes=()

    def create(self, request):
        country = get_object_or_404(Country, id=request.data['country'])
        region = get_object_or_404(Region, id=request.data['region'])
        constituency = get_object_or_404(Constituency, id=request.data['constituency'])
        town = get_object_or_404(Town, id=request.data['town'])
        area = get_object_or_404(Area, id=request.data['area'])
    

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
                is_active=False,
                active_constituency=constituency
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

                permissions = Permission.objects.all()

                for perm in permissions:
                    user_perm = UserPermissionCust.objects.create(
                        user=user,
                        permission_name=perm.name
                    )

                    user_perm.save()

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

    
class MPCreateApiView(CreateAPIView):
    serializer_class = MPRegisterSerializer
    permission_classes=()

    def create(self, request, id):
        country = get_object_or_404(Country, id=request.data['country'])
        region = get_object_or_404(Region, id=request.data['region'])
        constituency = get_object_or_404(Constituency, id= request.data['constituency'])

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
        elif len(str(request.data['mp_id'])) < 1 or request.data['mp_id']=="null":
            return Response({
                "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message":"MP's ID is required."
            })
        
        else:
        
        # Creating User and MP Profile
            user = User.objects.create(
            email=request.data['email'],
            # username=validated_data['username'],
            full_name=request.data['full_name'],
            date_of_birth=request.data['date_of_birth'],
            contact=request.data['contact'],
            country=country,
            is_mp = True,
            system_id_for_user=system_id_for_user,
            is_active=False,
            active_constituency=constituency
            )

            user.set_password(request.data['password'])
            user.save()

            user.constituency.add(constituency)
            user.region.add(region)


            mp = MpProfile(
                user = user,
                mp_id = request.data['mp_id'],  
            )

            mp.save()
            try:
                const = Constituent.objects.get(user__system_id_for_user = id)
                const.user.is_subadmin = True
                const.user.subadmin_for = mp.user.active_constituency
                const.subadmin_for = user
                const.is_subadmin = True

                const.save()
            except Exception as e:
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"User is an MP"
                })

            
            return Response({
                "status":status.HTTP_201_CREATED,
                "message":"Account registration is successful. We will get in touch to get your account verified.",
                "email": user.email
                }, status=status.HTTP_201_CREATED)
   

class UserLoginView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        emailorcontact = serializer.data['email_or_contact']
        if "@" in emailorcontact and "." in emailorcontact:
            user_ = User.objects.get(email=emailorcontact)
        else:
            user_ = User.objects.get(contact=emailorcontact)

        ac = ConstituencySerializer(user_.active_constituency)
        ar = ListAllAreaSerializer(user_.active_area)
        at = ListAllTownsSerializer(user_.active_town)
        sub = ConstituencySerializer(user_.subadmin_for)
        # ac.is_valid(raise_exception=True)

        print(f"______________________{ac.data}")
        response = {
            'success' : 'True',
            'status' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            'id':user_.id,
            'email':user_.email,
            # 'username':user_.username,
            'full_name':user_.full_name,
            'is_constituent':user_.is_constituent,
            'is_mp':user_.is_mp,
            "is_security_person":user_.is_security_person,
            "is_medical_center":user_.is_medical_center,
            "is_assembly_man":user_.is_assembly_man,
            "is_subadmin":user_.is_subadmin,
            'contact':user_.contact,
            'date_of_birth':user_.date_of_birth,
            'system_id_for_user':user_.system_id_for_user,
            'active_constituency':ac.data,
            'active_town':at.data,
            'active_area':ar.data,
            "email_verified":user_.email_verified,
            "subadmin_for":sub.data

            }
        status_code = status.HTTP_200_OK
        if user_.email_verified:
            return Response(response, status=status_code)
        else:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"You have to verify your account.",
                    "email_verified":user_.email_verified,
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class SecondaryRegistration(UpdateAPIView):

    serializer_class = ConstituentSecondaryRegistration

    permission_classes= ()

    def update(self, request):
        try:
            system_id_for_user = request.data['system_id_for_user']
            user = User.objects.get(system_id_for_user=system_id_for_user)
            data = ""
            constituency = Constituency.objects.get(id=request.data['constituency'])
            consts = user.constituency.all()

            ids = []

            for i in consts:
                ids.append(i.id)

            

                 
            
            if request.data['constituency']  in ids:
                data = {
                "status":status.HTTP_400_BAD_REQUEST,
                "message":f"You are already a member of {constituency.name}."
                }
                return Response(
                    data, status.HTTP_400_BAD_REQUEST
                )
            elif user.constituency.count()>1:
                data = {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"You can not belong to more that 2 constituencies."
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                region = get_object_or_404(Region, id=request.data['region'])
                constituency = get_object_or_404(Constituency, id=request.data['constituency'])
                area = get_object_or_404(Area, id=request.data['area'])
                town = get_object_or_404(Town, id=request.data['town'])
                try:
                    user.region.add(region)
                    user.constituency.add(constituency)
                    const = Constituent.objects.get(user=user)
                    const.town.add(town)
                    const.area.add(area)
                    data = {
                    "status":status.HTTP_200_OK,
                    
                    "message":f"You are now a member of {constituency.name}."
                    }
                except Exception as e:
                    print(e)
                    data = {
                    "status":status.HTTP_400_BAD_REQUEST,
                    
                    "message":"Sorry, something went wrong."
                }
                
            
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            data = {
                    "status":status.HTTP_400_BAD_REQUEST,
                    
                    "message":f"Sorry, something went wrong."
                }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)




class RetrieveAllCountriesView(ListAPIView):
    serializer_class = ListAllCountriesSerializer
    permission_classes=[AllowAny]
    queryset = Country.objects.all()


class OTPEmailVerificationView(APIView):
    permission_classes =()
    def post(self, request):
        data = OTPVerificationEmailSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        email = data['email']
        otp_code = data['code']
        try:
            user = User.objects.get(email=email.value)
            code = OTPCode.objects.get(code_for=email.value, code=otp_code.value)   
            code.delete()
            user.is_active = True
            user.email_verified = True
            user.save() 
            
            data = {
                "status":status.HTTP_202_ACCEPTED,
                "message":"email has been verified"
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            data = {
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Sorry something went wrong, try again"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class OTPPhoneVerificationView(APIView):
    permission_classes =()
    def post(self, request):
        data = OTPVerificationSMSSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user_id = data['user_id']
        otp_code = data['code']
        try:
            user = User.objects.get(system_id_for_user=user_id.value)
            code = OTPCode.objects.get(code_for=user_id.value, code=otp_code.value)   
            code.delete()
            user.phone_verified = True
            user.save() 
            data = {
                "message":"Phone has been verified"
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            data = {
                "message":"Sorry something went wrong, try again"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class GetOTPSMSView(APIView):
    permission_classes =()
    def post(self, request):
        data = GetOTPSMSSerializer(data=request.data)  
        data.is_valid(raise_exception=True)

        user_id = data['system_id_for_user']
        
        otp_code = generate_OTP()

        send_sms(f"Your NsromaHub phone number verification code is {otp_code}")

        otp = OTPCode.objects.create(
           code_for= user_id.value,
           code=otp_code
        )

        otp.save()
        data = {
            "message":"SMS has been sent to the phone number"
        }
        return Response(data, status=status.HTTP_200_OK)



          