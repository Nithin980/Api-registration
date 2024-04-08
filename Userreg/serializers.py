from rest_framework import serializers
from .models import UserProfile, Referral
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'referral_code']

class ReferralSerializer(serializers.ModelSerializer):
    referred_user = UserProfileSerializer()
    class Meta:
        model = Referral
        fields = ['referred_user', 'registration_timestamp']
