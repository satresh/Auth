from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework.response import Response
from rest_framework import status
from .models import UserCred
from .serializer import UserSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

# class Home(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_token(request):
    print(request)
    # Extract the token from the Authorization header
    content = {
        'status': 'request was permitted'
    }
    return Response(content)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    print("Inside refresh")
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Use SimpleJWT to create a new access token from the refresh token
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_custom_user(request):
    serializer = UserSerializer(data=request.data)
    print("inside Serial", request.data)
    
    if serializer.is_valid():
        user = serializer.save()

        return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)  # Success
    else:
        print("serializers error", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Failure


'''
{
"user_name":"deqyv",
"user_pass":"123123"
}
'''

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('user_name')
    password = request.data.get('user_pass')

    try:
        user = UserCred.objects.get(user_name=username)

        # Check the provided password against the stored hashed password
        if check_password(password, user.user_pass):
            # Create JWT token
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            user_profile_url = request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
            user = UserSerializer(user).data
            # Return user details along with the token
            user.update({'img-path': user_profile_url})

            return Response({
                'user': user,
                'token': token
            }, status=status.HTTP_200_OK)  # Success
        else:
            return Response({'error': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)  # Invalid password
    except UserCred.DoesNotExist:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)  # User not found

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    # The user is already authenticated, so we can access the user details from request.user
    user = request.user
    
    # Structure the user details to return
    user_details = {
        'id': user.id,
        'user_name': user.user_name,
        'user_email': user.user_email,
        'user_phone_no': user.user_phone_no,
    }

    # Return the user details as a response
    return Response(user_details, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_details(request):
    user = request.user  # Get the authenticated user
    
    # Extract the data from the request
    data = request.data
    
    # Update fields if provided in the request
    if 'user_name' in data:
        user.user_name = data['user_name']
    
    if 'user_email' in data:
        user.user_email = data['user_email']

    if 'user_phone_no' in data:
        user.user_phone_no = data['user_phone_no']
    
    # You can add password update logic as well if necessary
    if 'user_pass' in data:
        user.set_password(data['user_pass'])  # Hashes and sets the password
    
    # Save the updated user details
    user.save()

    # Structure the updated user details to return
    updated_user_details = {
        'id': user.id,
        'user_name': user.user_name,
        'user_email': user.user_email,
        'user_phone_no': user.user_phone_no,
    }

    # Return the updated user details as a response
    return Response(updated_user_details, status=status.HTTP_200_OK)
