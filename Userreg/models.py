from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=20, blank=True, null=True)

class Referral(models.Model):
    referrer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referred_by')
    registration_timestamp = models.DateTimeField(auto_now_add=True)
