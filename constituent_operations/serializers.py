from warnings import simplefilter
from django.db import models

from django.db.models import fields
from django.db.models.fields import files
from users.models import Constituency, Region
from constituent_operations.models import Message, ProblemsForActionPlan, User, ConductsForAssessment
from rest_framework import serializers
from mp_operations.models import Comment, Project
from mp_operations.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SendMessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.CharField(max_length=15)
    class Meta:
        model=Message
        fields=["sender_id","message","attached_file"]


class CommentSerializer(serializers.ModelSerializer):
    comment_from = UserSerializer()
    class Meta:
        model=Comment 
        fields="__all__"

class ListProjectsOfMPs(serializers.ModelSerializer):
    mp = UserSerializer(read_only=True)
    
    comments = CommentSerializer(many=True)
    class Meta:
        model=Project
        fields='__all__'


class RNSendIncidentReportSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=15)
    # receiver = serializers.IntegerField()
    subject = serializers.CharField(max_length=20000)
    message = serializers.CharField(max_length=1000000)
    attached_file = serializers.FileField(required=False, allow_null=True)

class RNSendRequestFormSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=15)
    # receiver = serializers.IntegerField()
    subject = serializers.CharField(max_length=20000)
    message = serializers.CharField(max_length=1000000)
    attached_file = serializers.FileField(required=False, allow_null=True)


class RetrieveConstituentConstituenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Constituency
        fields = "__all__"


class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model=Constituency
        fields="__all__"

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Region
        fields="__all__"


class GetUserInfoSerializer(serializers.ModelSerializer):
    constituency = ConstituencySerializer(many=True)
    region = RegionSerializer(many=True)
    active_constituency = ConstituencySerializer()
    class Meta:
        model=User
        fields = ['id','is_mp','is_constituent','is_security_person','is_assembly_man','is_medical_center','is_subadmin', 'full_name','profile_picture', 'email', 'contact', 'date_of_birth', 'system_id_for_user', 'country', 'region', 'constituency', "active_constituency", "active_town", "active_area", "subadmin_for"]


class CommentOnPostSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=15)
    project_id = serializers.IntegerField()
    comment_body = serializers.CharField(max_length=500)

 
class RetrieveMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    class Meta:
        model=Message
        fields = "__all__"


class ActionPlanSerializer(serializers.Serializer):
    data = serializers.DictField(
        child=serializers.CharField(max_length=100)
    )


class AssessmentSerializer(serializers.Serializer):
    data = serializers.DictField(
        child=serializers.CharField(max_length=100)
    )

class ApproveActionPlanSerializer(serializers.Serializer):
    problem_titles = serializers.ListField(child=serializers.CharField(max_length=100))
    stats = serializers.ListField(child=serializers.IntegerField())
    comment = serializers.CharField(max_length=20000)


class ProblemForActionPlanSerializer(serializers.ModelSerializer):
     class Meta:
         model=ProblemsForActionPlan
         fields=['title']    


class ConductForAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConductsForAssessment
        fields="__all__"


class AssessmentSerializer(serializers.Serializer):
    projects_assessment=serializers.DictField(
        child=serializers.CharField(max_length=100)
        )

    conduct_assessment=serializers.DictField(
        child=serializers.CharField(max_length=100)
    )
