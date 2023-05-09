from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for register user
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password', 'date_of_birth', 'mobile_number', 'address', 'pancard_number']

    # function to create a user using MyUser Model.
    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            date_of_birth=validated_data.get('date_of_birth'),
            mobile_number=validated_data.get('mobile_number'),
            address=validated_data.get('address'),
            pancard_number=validated_data.get('pancard_number')
        )
        return user



class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class for Login User
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password) #using the authenticate() method from django.contrib.auth
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Must include both email and password.')
        
        data['user'] = user
        return data


class MyUserSerializer(serializers.ModelSerializer):
    """
    Serializer class for User Model - defined to GET all the users present in the database.
    """
    class Meta:
        model = MyUser
        fields = ['id', 'name', 'email', 'date_of_birth', 'mobile_number', 'address', 'pancard_number']

