from rest_framework import serializers
from .models import ParentInquiry

class ParentInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentInquiry
        fields = '__all__'
