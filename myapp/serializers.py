from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password', 'date_of_birth', 'mobile_number', 'address', 'pancard_number']

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
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Must include both email and password.')
        
        data['user'] = user
        return data


