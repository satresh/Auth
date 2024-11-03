from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import RegisterForm
from .models import UserProfile
from django.shortcuts import get_object_or_404
from company1_products.models import Product as Company1Product  # Adjust the import as necessary
from company2_products.models import Product as Company2Product  # Adjust the import as necessary
from company1_products.serializers import ProductSerializer as Company1ProductSerializer  # Correct import
from company2_products.serializers import ProductSerializer as Company2ProductSerializer  # Correct import

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    form = RegisterForm(request.data)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        UserProfile.objects.create(user=user, company=form.cleaned_data['company'])  # Create a UserProfile
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def user_products(request):
    # Get the user's company
    user_company = request.user.userprofile.company  # Assuming user has a user profile linked to User
    if request.method == 'GET':

        if user_company == 'company1':
            products = Company1Product.objects.using('company1').all()
            serializer = Company1ProductSerializer(products, many=True)  # Use the correct serializer
        elif user_company == 'company2':
            products = Company2Product.objects.using('company2').all()
            serializer = Company2ProductSerializer(products, many=True)  # Use the correct serializer
        else:
            return Response({"error": "No products available for the user"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the products
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
            if user_company == 'company1':
                serializer = Company1ProductSerializer(data=request.data)
                if serializer.is_valid():
                    product_instance = serializer.save()  # Create the Product instance without saving
                    print(">>>>>>")
                    product_instance.save(using='company1')  # Save to 'company1' database
                    return Response(serializer.data, status=201)
            elif user_company == 'company2':
                serializer = Company2ProductSerializer(data=request.data)
                if serializer.is_valid():
                    product_instance = serializer.save()  # Create the Product instance without saving
                    print(">>>>>>")
                    product_instance.save(using='company2')  # Save to 'company1' database
                    return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_product(request, pk):
    user_company = request.user.userprofile.company
    if user_company == 'company1':
        product = get_object_or_404(Company1Product.objects.using('company1'), pk=pk)
        if request.method == 'GET':
            serializer = Company1ProductSerializer(product)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = Company1ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save(using='company1')
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            product.delete(using='company1')
            return Response(status=204)
        
    if user_company == 'company2':
        product = get_object_or_404(Company2Product.objects.using('company2'), pk=pk)
        if request.method == 'GET':
            serializer = Company2ProductSerializer(product)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = Company2ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save(using='company2')
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            product.delete(using='company2')
            return Response(status=204)
    return Response({"error": "Unauthorized"}, status=403)
