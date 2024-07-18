from django.test import TestCase
"""
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from assets.models import Asset, Tag, AssetTag
from django.contrib.auth import get_user_model

User = get_user_model()

class AssetTagTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com
            password='adminpass'
        )
        self.client.force_authenticate(user=self.admin_user)

        self.asset = Asset.objects.create(
            name='Laptop',
            assetType='Electronics',
            description='A high-end laptop',
            serialNumber='ABC12345',
            category_id=1,
            assignedDepartment_id=1,
            status=True
        )
        self.tag = Tag.objects.create(name='IT Equipment')
        self.asset_tag_url = reverse('asset-tag-list')

    def test_create_asset_tag(self):
        payload = {
            'asset': self.asset.id,
            'tag': self.tag.id
        }
        response = self.client.post(self.asset_tag_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert
        Equal(AssetTag.objects.count(), 1)

    def test_list_asset_tags(self):
        AssetTag.objects.create(asset=self.asset, tag=self.tag)
        response = self.client.get(self.asset_tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_asset_tag(self):
        asset_tag = AssetTag.objects.create(asset=self.asset, tag=self.tag)
        new_tag = Tag.objects.create(name='Office Equipment')
        payload = {
            'asset': self.asset.id,
            'tag': new_tag.id
        }
        url = reverse('asset-tag-detail', args=[asset_tag.id])
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code
, status.HTTP_200_OK)
        asset_tag.refresh_from_db()
        self.assertEqual(asset_tag.tag.id, new_tag.id)

    def test_delete_asset_tag(self):
        asset_tag = AssetTag.objects.create(asset=self.asset, tag=self.tag)
        url = reverse('asset-tag-detail', args=[asset_tag.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AssetTag.objects.count(), 0)

"""
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
