from django.core.exceptions import ValidationError
from django.db.models import fields
from django.shortcuts import get_object_or_404
from users.models import Area, Constituency, Constituent, Country, MpProfile, OTPCode, Region, Town
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from .utils import generate_OTP, generate_userID, sending_mail

countryCode = {
    "Ghana":"GH",
    "TOGO":"TG"
}
 


User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER



class ConstituentRegisterSerializer(serializers.ModelSerializer):
    voters_id       = serializers.CharField(write_only=True)
    town            = serializers.CharField(write_only=True)
    country         = serializers.IntegerField(write_only=True)
    region          = serializers.IntegerField(write_only=True)
    constituency    = serializers.IntegerField(write_only=True)
    town    = serializers.IntegerField(write_only=True)
    area    = serializers.IntegerField(write_only=True)
    class Meta:
        model = User
        # exclude = ['user_permissions', 'groups','is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'system_id_for_user', 'is_mp', 'is_constituent','first_name', 'last_name']
        fields = ['email', 'full_name', 'profile_picture', 'date_of_birth','is_superuser', 'voters_id', 'town', 'area', 'contact', 'country','region', 'town', 'constituency', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    

    
    # def create(self, validated_data):

    #     country = get_object_or_404(Country, id=validated_data['country'])
    #     region = get_object_or_404(Region, id=validated_data['region'])
    #     constituency = get_object_or_404(Constituency, id= validated_data['constituency'])


    #     # Generating A valid user ID
    #     CD = countryCode[country.name]
    #     system_id_for_user =""
    #     while True:
    #         nums = generate_userID()
    #         system_id_for_user = str(CD)+str(nums)
    #         user = User.objects.filter(system_id_for_user=system_id_for_user)

    #         if user.exists():
    #             pass
    #         else:
    #             system_id_for_user = system_id_for_user
    #             break

    #     email = validated_data['email']
    #     contact = validated_data['contact']
    #     if User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError("Email already exist")
    #     elif User.objects.filter(contact=contact).exists():
    #         raise serializers.ValidationError("Contact already exist")
    #     else:
        
    #     # Creating User and Constituency Profile
    #         user = User.objects.create(
    #         email=validated_data['email'],
    #         # username=validated_data['username'],
    #         full_name=validated_data['full_name'],
    #         date_of_birth=validated_data['date_of_birth'],
    #         contact=validated_data['contact'],
    #         country=country,
            
    #         is_constituent = True,
    #         system_id_for_user=system_id_for_user,
    #         is_active=False
    #         )

    #         user.set_password(validated_data['password'])
    #         user.save()

    #         user.constituency.add(constituency)
    #         user.region.add(region)


    #         constituent = Constituent(
    #             user = user,
    #             voters_id = validated_data['voters_id'],
    #             town = validated_data['town']
    #         )
    #         otp_code = generate_OTP()

    #         otp = OTPCode.objects.create(code_for=validated_data['email'],code=otp_code)
    #         otp.save()

    #         sending_mail(f"Hello {validated_data['full_name']}\nThis is your verification code: {otp_code}","NsromaHub Account email verification", validated_data['email'])
    #         constituent.save()




    #         return user


class MPRegisterSerializer(serializers.ModelSerializer):
    mp_id = serializers.CharField(write_only=True)
    country = serializers.IntegerField(write_only=True)
    region = serializers.IntegerField(write_only=True)
    constituency = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = User
        # exclude = ['user_permissions', 'groups','is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'system_id_for_user', 'is_mp', 'is_constituent','first_name', 'last_name']
        fields = ['email', 'full_name','profile_picture', 'date_of_birth', 'mp_id', 'contact', 'country','region', 'constituency', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    

    
    # def create(self, validated_data):

    #     country = get_object_or_404(Country, id=validated_data['country'])
    #     region = get_object_or_404(Region, id=validated_data['region'])
    #     constituency = get_object_or_404(Constituency, id= validated_data['constituency'])

    #     # Generating A valid user ID
    #     CD = countryCode[country.name]
    #     system_id_for_user =""
    #     while True:
    #         nums = generate_userID()
    #         system_id_for_user = str(CD)+str(nums)
    #         user = User.objects.filter(system_id_for_user=system_id_for_user)

    #         if user.exists():
    #             pass
    #         else:
    #             system_id_for_user = system_id_for_user
    #             break
        
    #     # Creating User and MP Profile
    #     user = User.objects.create(
    #     email=validated_data['email'],
    #     # username=validated_data['username'],
    #     full_name=validated_data['full_name'],
    #     date_of_birth=validated_data['date_of_birth'],
    #     contact=validated_data['contact'],
    #     country=country,
    #     is_mp = True,
    #     system_id_for_user=system_id_for_user,
    #     is_active=False
    #     )

    #     user.set_password(validated_data['password'])
    #     user.save()

    #     user.constituency.add(constituency)
    #     user.region.add(region)


    #     mp = MpProfile(
    #         user = user,
    #         mp_id = validated_data['mp_id'],  
    #     )

    #     mp.save()
    #     print(validated_data)
        
    #     return user




class UserLoginSerializer(serializers.Serializer):

    email_or_contact = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model= User
        fields=['id']

    def validate(self, data):
        email_or_contact = data.get("email_or_contact", None)
        password = data.get("password", None)

        if "@" in email_or_contact and "." in email_or_contact:

            user = authenticate(email=email_or_contact, password=password)
        else:
            user = User.objects.get(contact=email_or_contact)
            user = authenticate(email=user.email, password=password)


        if user is None:
            raise serializers.ValidationError(
                'A user with this email/phone and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email_or_contact':email_or_contact,
            'username':user.username,
            'token': jwt_token
        }


class ConstituentSecondaryRegistration(serializers.ModelSerializer):
    system_id_for_user         = serializers.CharField(write_only=True)
    region          = serializers.IntegerField(write_only=True)
    constituency    = serializers.IntegerField(write_only=True)
    town    = serializers.IntegerField(write_only=True)
    area    = serializers.IntegerField(write_only=True)

    class Meta:
        model=User
        fields = ['system_id_for_user','region','constituency', 'town', 'area']
        lookup_field = 'id'

class ListAllAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields="__all__"

class ListAllTownsSerializer(serializers.ModelSerializer):
    areas = ListAllAreaSerializer(many=True, read_only=True)
    class Meta:
        model=Town
        fields = "__all__"

class ListAllConstituencySerializer(serializers.ModelSerializer):
    towns = ListAllTownsSerializer(many=True, read_only=True)
    class Meta:
        model=Constituency
        fields = "__all__"


class ListAllRegionsSerializer(serializers.ModelSerializer):
    constituencies = ListAllConstituencySerializer(many=True, read_only=True)
    class Meta:
        model=Region
        fields = "__all__"


class ListAllCountriesSerializer(serializers.ModelSerializer):
    regions=ListAllRegionsSerializer(many=True, read_only=True)
    class Meta:
        model=Country
        fields = "__all__"


class OTPVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=7)

class GetOTPSMSSerializer(serializers.Serializer):
    system_id_for_user = serializers.CharField(max_length=15)


class OTPVerificationSMSSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=7)
