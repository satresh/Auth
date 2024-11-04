# from rest_framework import serializers
# from .models import UserCred
# from django.contrib.auth.hashers import make_password

# class UserSerializer(serializers.ModelSerializer):
#     user_pass = serializers.CharField(write_only=True)

#     class Meta:
#         model = UserCred
#         fields = ['user_name', 'user_email', 'user_phone_no', 'user_pass', 'profile_picture']

#     def create(self, validated_data):
#         validated_data['user_pass'] = make_password(validated_data['user_pass'])
#         return super().create(validated_data)


from rest_framework import serializers
from .models import UserCred
from django.contrib.auth.hashers import make_password
from .models import UserCredManager

class UserSerializer(serializers.ModelSerializer):
    user_pass = serializers.CharField(write_only=True)

    class Meta:
        model = UserCred
        fields = ['user_name', 'user_email', 'user_phone_no', 'user_pass', 'profile_picture']
        extra_kwargs = {'user_pass': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data['user_pass'] = make_password(validated_data['user_pass'])
        return super().create(validated_data)