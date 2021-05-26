from rest_framework import  serializers
from .models import you_url


class you_serial(serializers.Serializer):

    url = serializers.CharField(max_length=200,required=True)
    pixel =  serializers.CharField(max_length=10)


class igtv_serial(serializers.Serializer):
    url = serializers.CharField(max_length=200, required=True)
