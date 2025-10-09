from rest_framework import serializers
from .models import UploadedFile, CommonBook

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'

class CommonBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonBook
        fields = '__all__'
