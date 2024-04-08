from django.urls import path
from .views import user_registration, user_details, referrals

urlpatterns = [
    path('register/', user_registration),
    path('details/', user_details),
    path('referrals/', referrals),
]
