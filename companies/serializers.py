from rest_framework import serializers
from .models import Company, Email

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email']

class CompanySerializer(serializers.ModelSerializer):
    emails = EmailSerializer(many=True, read_only=True)  # Nested serializer to show related emails

    class Meta:
        model = Company
        fields = ['id', 'name', 'url', 'is_active', 'country', 'city', 'emails']
