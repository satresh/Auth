from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .permissions import IsAdminUser, IsManagerUser, IsRegularUser,IsManagerOrRegularUser
from .models import User

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({'message': 'Hello Admin'})

class ManagerOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsManagerUser]

    def get(self, request):
        return Response({'message': 'Hello Manager'})

class UserOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsRegularUser]

    def get(self, request):
        return Response({'message': 'Hello User'})

class manager(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrRegularUser]
    def get(self, request):
        return Response({'message': 'Hello manager.. Viewing managers and users'})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.role == "admin":
                user.is_superuser = True
                user.is_staff = True
                user.save()
            elif user.role == "manager":
                user.is_staff = True
                user.save()
            # Serialize the user data to return only needed fields
            user_data = UserSerializer(user).data

            return Response({
                'user': user_data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            
            # Serialize the user data
            user_data = UserSerializer(user).data
            
            return Response({
                'user': user_data,
                'refresh': str(refresh),
                'access': access,
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class UpdateUserRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        email = request.GET.get('email', 'default')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        new_role = request.data.get('role')
        
        if new_role not in ['user', 'manager', 'admin']:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.role = new_role
        if new_role == "manager":
            user.is_staff = True
        user.save()
        return Response({"message": f"User role updated to {new_role}"}, status=status.HTTP_200_OK)