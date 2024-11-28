from rest_framework import serializers
from userprofile.models import UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class MyTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = f"{user.first_name} {user.last_name}" 
        token["permissions"] = {
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser
        }
        
        return token

class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    class Meta:
        model = UserProfile
        fields = ['username','email','username','first_name','last_name','rooms','password','password_confirmation',]
        extra_kwargs = { 
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        if check_password(validated_data['password_confirmation'],validated_data['password']):
            validated_data.pop('password_confirmation')
            return super().create(validated_data)
        else:
            raise serializers.ValidationError('Password does not match.')

    def update(self, instance, validated_data):
        if validated_data['password'] != validated_data['password_confirmation']:
            raise serializers.ValidationError('Password does not match.')
        validated_data.pop('password_confirmation')
        return super().update(instance, validated_data)
    