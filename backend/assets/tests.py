from django.test import TestCase
from rest_framework import test
from rest_framework.views import APIView
from assets.viewsets import LoginView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from assets.models import CustomUser, Category, Tag, Asset
from django.contrib.auth.password_validation import validate_password

# Create your tests here.
class Test(APIView):
    """
    Tests
    """
    def post(self,request):
        try:
            # self.testRegister
            # self.
            serializer = self.testPasswordReset(data=request.data)
           
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as err:
             return Response(err,status=status.HTTP_400_BAD_REQUEST)

    class testLogin(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)
        access = serializers.CharField(read_only=True)
        refresh = serializers.CharField(read_only=True)

        username ="bongoyedaniel"
        password = 'myPassword' 

        def validate(self, attrs):
            #=====test data
            attrs['username'] = "bongoyedaniel"
            attrs['password'] = 'myPassword' 

            username = attrs['username']
            password =attrs['password']

            if not username or not password:
                raise serializers.ValidationError("Username and password are required")

            try:
                user = CustomUser.objects.get(username=username)
                if not user.check_password(password):
                    raise serializers.ValidationError("Incorrect password")
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("User does not exist")

            refresh = RefreshToken.for_user(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)

            return attrs

    class testRegister(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
        password2 = serializers.CharField(write_only=True, required=True)

        class Meta:
            model = CustomUser
            fields = ['username', 'password', 'password2', 'email', 'firstName', 'lastName']
            extra_kwargs = {
                'username': {'required': True},
                'email': {'required': True},
                'firstName': {'required': True},
                'lastName': {'required': True},
            }

        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            return attrs

        def create(self, validated_data):
            user = CustomUser.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['firstName'],
                last_name=validated_data['lastName']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

    class testPasswordReset(serializers.Serializer):
        oldPassword = serializers.CharField(write_only=True)
        newPassword = serializers.CharField(write_only=True)
        newPasswordConfirm = serializers.CharField(write_only=True)

        oldPassword  ="myPPassword"
        newPassword = "myPassword"
        newPasswordConfirm = "mPassword"

        def validate(self, data):
            # test data
            data['oldPassword']  = "myPPassword"
            data['newPassword'] = "myPassword"
            data['newPasswordConfirm'] = "myNewPassword"
 
            if data['newPassword'] != data['newPasswordConfirm']:
                raise serializers.ValidationError("New passwords do not match")
            return data

        def validate_old_password(self, value):
            user = self.context['request'].user
            if not user.check_password(value):
                raise serializers.ValidationError("Old password is incorrect")
            return value

        def validate_new_password(self, value):
            validate_password(value)
            return value