from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_extra_fields import fields



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'}, validators=[validate_password])
    confirm_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'first_name': {'required' : True},
            'last_name': {'required' : True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password fields didn't match"})
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user)
        return user

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField(source='user.pk')
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    user = UserSerializer()
    profile_picture = fields.Base64ImageField()
    online = serializers.BooleanField(read_only=True)
    last_online = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Profile
        fields = ['pk', 'user', 'username','first_name', 'last_name', 'profile_picture', 'online', 'last_online']
    
    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        instance.user.first_name = user.get('first_name', instance.user.first_name)
        instance.user.last_name = user.get('last_name', instance.user.last_name)
        instance.user.email = user.get('email', instance.user.email)
        instance.user.username = user.get('username', instance.user.username)
        instance.user.save()
        instance.profile_picture = validated_data.get('profile_picture', instance.image)
        instance.save()
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)