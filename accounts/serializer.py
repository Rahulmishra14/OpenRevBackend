# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    affiliation = serializers.CharField(source='profile.affiliation', allow_blank=True)
    homepage = serializers.URLField(source='profile.homepage', allow_blank=True)
    scholar = serializers.URLField(source='profile.scholar', allow_blank=True)
    github = serializers.URLField(source='profile.github', allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name', 
                  'affiliation', 'homepage', 'scholar', 'github']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
