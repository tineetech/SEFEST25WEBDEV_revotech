from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile, Doctor

# login user biasa
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        # Memastikan user yang login adalah user biasa
        if user.role != 'user':
            raise serializers.ValidationError('This login is only for regular users')

        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'phone_number', 'address', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile']
        read_only_fields = ['role']

# register user biasa
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation', 'profile']

    def validate(self, data):
        # Validasi password match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                'password_confirmation': "Password fields didn't match."
            })
        
        # Validasi email unik
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'Email already exists'
            })
        
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('password_confirmation')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='user'
        )

        UserProfile.objects.filter(user=user).update(**profile_data)

        return user

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'str_number', 'specialization', 'chat_fee']

class DoctorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    doctor_profile = DoctorProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation', 'doctor_profile']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                'password_confirmation': "Password fields didn't match."
            })
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'Email already exists'
            })
        
        return data

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor_profile')
        validated_data.pop('password_confirmation')
        
        # Create user with doctor role
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='doctor'
        )

        # Create doctor profile with pending status
        Doctor.objects.create(
            user=user,
            verification_status='pending',
            **doctor_data
        )

        return user

class DoctorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        # Memastikan user adalah dokter
        if user.role != 'doctor':
            raise serializers.ValidationError('This login is only for doctors')

        # Memastikan dokter sudah terverifikasi
        try:
            doctor = user.doctor_profile
            if doctor.verification_status != 'approved':
                raise serializers.ValidationError('Your account is not verified yet')
        except Doctor.DoesNotExist:
            raise serializers.ValidationError('Doctor profile not found')

        return user