from django.db import models
from django.db.models.fields import CharField
from django.shortcuts import get_object_or_404
from users.models import Constituency, Constituent, Country, MpProfile, Region
from rest_framework import fields, serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from .utils import generate_userID

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
    class Meta:
        model = User
        # exclude = ['user_permissions', 'groups','is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'system_id_for_user', 'is_mp', 'is_constituent','first_name', 'last_name']
        fields = ['username', 'email', 'full_name', 'date_of_birth', 'voters_id', 'town', 'contact', 'country','region', 'town', 'constituency', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    

    
    def create(self, validated_data):

        country = get_object_or_404(Country, id=validated_data['country'])
        region = get_object_or_404(Region, id=validated_data['region'])
        constituency = get_object_or_404(Constituency, id= validated_data['constituency'])


        # Generating A valid user ID
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
        
        # Creating User and Constituency Profile
        user = User.objects.create(
        email=validated_data['email'],
        username=validated_data['username'],
        full_name=validated_data['full_name'],
        date_of_birth=validated_data['date_of_birth'],
        contact=validated_data['contact'],
        country=country,
        
        is_constituent = True,
        system_id_for_user=system_id_for_user
        )

        user.set_password(validated_data['password'])
        user.save()

        user.constituency.add(constituency)
        user.region.add(region)

        print(validated_data)

        constituent = Constituent(
             user = user,
            voters_id = validated_data['voters_id'],
            town = validated_data['town']
        )

        constituent.save()
        print(validated_data)
        return user


class MPRegisterSerializer(serializers.ModelSerializer):
    mp_id = serializers.CharField(write_only=True)
    country = serializers.IntegerField(write_only=True)
    region = serializers.IntegerField(write_only=True)
    constituency = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = User
        # exclude = ['user_permissions', 'groups','is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'system_id_for_user', 'is_mp', 'is_constituent','first_name', 'last_name']
        fields = ['username', 'email', 'full_name', 'date_of_birth', 'mp_id', 'contact', 'country','region', 'constituency', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    

    
    def create(self, validated_data):

        country = get_object_or_404(Country, id=validated_data['country'])
        region = get_object_or_404(Region, id=validated_data['region'])
        constituency = get_object_or_404(Constituency, id= validated_data['constituency'])

        # Generating A valid user ID
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
        
        # Creating User and MP Profile
        user = User.objects.create(
        email=validated_data['email'],
        username=validated_data['username'],
        full_name=validated_data['full_name'],
        date_of_birth=validated_data['date_of_birth'],
        contact=validated_data['contact'],
        country=country,
        is_mp = True,
        system_id_for_user=system_id_for_user
        )

        user.set_password(validated_data['password'])
        user.save()

        user.constituency.add(constituency)
        user.region.add(region)


        mp = MpProfile(
             user = user,
            mp_id = validated_data['mp_id'],  
        )

        mp.save()
        print(validated_data)
        return user




class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password is not found.'
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
            'username':user.username,
            'token': jwt_token
        }


class ConstituentSecondaryRegistration(serializers.ModelSerializer):
    system_id_for_user         = serializers.CharField(write_only=True)
    region          = serializers.IntegerField(write_only=True)
    constituency    = serializers.IntegerField(write_only=True)

    class Meta:
        model=User
        fields = ['system_id_for_user','region','constituency']
        lookup_field = 'id'

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     region = get_object_or_404(Region, id=validated_data.region)
    #     constituency = get_object_or_404(Constituency, id= validated_data.constituency)

    #     user = get_object_or_404(User, system_id_for_user=validated_data.system_id_for_user)
        
    #     if user.constituency.count() > 1:
    #         data = {"message":"You can not belong to more than 2 constituencies"}
    #         return data
    #     else:
    #         user.region.add(region)
    #         user.constituency.add(constituency)

    #         user.save()

    #         return user
