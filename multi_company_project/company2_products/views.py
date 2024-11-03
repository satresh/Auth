from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from products.models import UserProfile

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list(request):
    print("Using database:", 'company2' if request.user.userprofile.company == 'company2' else 'company2')
    
    try:
        user_company = request.user.userprofile.company
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found."}, status=400)

    if user_company == 'company2':
        if request.method == 'GET':
            products = Product.objects.using('company2').all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                product_instance = serializer.save()  # Create the Product instance without saving
                print(">>>>>>")
                product_instance.save(using='company2')  # Save to 'company2' database
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
    return Response({"error": "Unauthorized"}, status=403)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    user_company = request.user.userprofile.company
    if user_company == 'company2':
        product = get_object_or_404(Product.objects.using('company2'), pk=pk)
        if request.method == 'GET':
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save(using='company2')
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == 'DELETE':
            product.delete(using='company2')
            return Response(status=204)
    return Response({"error": "Unauthorized"}, status=403)
