from constituent_operations.models import IncidentReport, Message, RequestForm
from rest_framework import serializers
from .models import ActionPlanAreaSummaryForMp, Project, Comment
from django.contrib.auth import get_user_model
from users.models import Constituent, SubAdminPermission, Town, Area
from users.serializers import ListAllAreaSerializer, ListAllConstituencySerializer




User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','is_active','is_mp','is_constituent','is_security_person','is_assembly_man','is_medical_center', 'is_subadmin','full_name','profile_picture', 'email', 'contact', 'date_of_birth', 'system_id_for_user', 'country', 'region', 'constituency', "subadmin_for"]

class SubAdminPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubAdminPermission
        exclude = ['sub_admin']

class PermissionSerializer(serializers.Serializer):
    perm_name = serializers.CharField(max_length=20)
    perm_value = serializers.BooleanField()

class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model=Town
        fields="__all__"

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields="__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"


class CreateProjectSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=15, write_only=True)
    # comments = CommentSerializer(many=True)
    class Meta:
        model=Project
        exclude = ['mp','comments']


    


class ListProjectSerializer(serializers.ModelSerializer):
    mp = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True)
    
    class Meta:
        model=Project
        fields="__all__"
        lookup_field = 'id'

class ConstituentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituent
        fields = "__all__"

class ListConstituentsSerializer(serializers.ModelSerializer):
    more_info = ConstituentInfoSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id','is_mp','is_constituent','is_security_person','is_medical_center', 'full_name', 'email', 'contact', 'date_of_birth', 'system_id_for_user','profile_picture', 'country', 'region', 'constituency', 'more_info']
        lookup_field = 'id'


class SendEmailSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=15)
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField(max_length=1000)
    attached_file = serializers.FileField(required = False, allow_null = True)



class SearchProjectsSerialiser(serializers.ModelSerializer):
    mp = UserSerializer(read_only=True)
    class Meta:
        model=Project
        fields = "__all__"
        # lookup_field = 'id'


class SearchConstituentsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','is_mp','is_constituent','is_security_person','is_medical_center', 'full_name', 'email', 'contact', 'date_of_birth', 'system_id_for_user', 'country', 'region', 'constituency']


class RNRetrieveIncidentReportSerializer(serializers.ModelSerializer):
    sender=UserSerializer()
    receiver=UserSerializer()
    class Meta:
        model = IncidentReport
        fields="__all__"

class RNRetrieveRequestFormSerializer(serializers.ModelSerializer):
    sender=UserSerializer()
    receiver=UserSerializer()
    class Meta:
        model = RequestForm
        fields="__all__"


class RNRetrieveMessageSerializer(serializers.ModelSerializer):
    sender=UserSerializer()
    receiver=UserSerializer()
    class Meta:
        model = Message
        fields="__all__"


class MPRetrieveAllSubAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    permissions = SubAdminPermissionSerializer()
    town = TownSerializer(read_only=True, many=True)
    area = AreaSerializer(read_only=True, many=True)
    class Meta:
        model = Constituent
        fields = ['voters_id','town','area','is_subadmin', 'user', 'permissions']

class SendMessageToConstituentSerializer(serializers.ModelSerializer):
    sender_id = serializers.CharField(max_length=15)
    receiver_id = serializers.CharField(max_length=15)
    class Meta:
        model=Message
        fields=["sender_id", "receiver_id","message","attached_file"]

class SendEmailToConstSerializer(serializers.Serializer):
    sender_id = serializers.CharField(max_length=15)
    receiver_id = serializers.CharField(max_length=15)
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField(max_length=1000)
    attached_file = serializers.FileField(required = False, allow_null = True)


class RetrieveActionPlanSummaryEachAreaForMPSerializer(serializers.ModelSerializer):
    area = ListAllAreaSerializer(read_only=True)
    constituency = ListAllConstituencySerializer(read_only=True)

    class Meta:
        model=ActionPlanAreaSummaryForMp
        fields="__all__"


class CreatePostSerializer(serializers.Serializer):

    user_id = serializers.CharField(max_length=15)
    media = serializers.FileField()
    caption = serializers.CharField(max_length=5000)

