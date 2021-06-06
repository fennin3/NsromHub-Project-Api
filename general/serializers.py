from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Country, Region, Constituency, Town, Area

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




