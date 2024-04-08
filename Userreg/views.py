from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, Referral
from .serializers import UserProfileSerializer, ReferralSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['POST'])
def user_registration(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    referral_code = request.data.get('referral_code')

    if name and email and password:
        # Create User
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        # Create UserProfile
        user_profile = UserProfile.objects.create(user=user, referral_code=referral_code)

        return Response({'user_id': user.id, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Name, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user_profile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def referrals(request):
    user_profile = UserProfile.objects.get(user=request.user)
    referred_users = Referral.objects.filter(referrer=user_profile)
    page = request.GET.get('page', 1)
    paginator = Paginator(referred_users, 20)
    try:
        referrals_page = paginator.page(page)
    except PageNotAnInteger:
        referrals_page = paginator.page(1)
    except EmptyPage:
        referrals_page = paginator.page(paginator.num_pages)

    serializer = ReferralSerializer(referrals_page, many=True)
    return Response(serializer.data)
