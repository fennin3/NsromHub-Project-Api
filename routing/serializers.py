from rest_framework import serializers

class Home(serializers.Serializer):
    page_name = serializers.CharField(max_length=200)