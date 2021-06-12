from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Country, Region, Constituency, Town, Area
from .models import ForumMessage
from users.serializers import ListAllConstituencySerializer
from mp_operations.serializers import UserSerializer

User = get_user_model()

class ProfileEditConstituentSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["profile_picture"]


class CountryCustomisedForEmma(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields=['id','name']



class RegionCustomisedForEmma(serializers.ModelSerializer):
    class Meta:
        model=Region
        fields=['id','name']


class ConstituencyCustomisedForEmma(serializers.ModelSerializer):
    class Meta:
        model=Constituency
        fields=['id','name']


class TownCustomisedForEmma(serializers.ModelSerializer):
    class Meta:
        model=Town
        fields=['id','name']     



class AreaCustomisedForEmma(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields=['id','name']


class ForumMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    current_mp  = UserSerializer()
    constituency = ListAllConstituencySerializer()
    class Meta:
        model=ForumMessage
        fields= "__all__"




