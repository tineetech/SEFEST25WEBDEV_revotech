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
    profile = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation', 'profile']

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
        validated_data.pop('password_confirmation')
        profile_data = validated_data.pop('profile', {})
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='user'
        )

        if profile_data:
            UserProfile.objects.filter(user=user).update(**profile_data)

        return user

# register doctor
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

# untuk update profile
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = UserProfile
        fields = ['birthday', 'phone_number', 'address', 'profile_picture']

    def update(self, instance, validated_data):
        # Jangan update profile_picture jika tidak ada dalam data
        if 'profile_picture' not in validated_data:
            validated_data.pop('profile_picture', None)
        
        return super().update(instance, validated_data)

# untuk update profile
class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileUpdateSerializer()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'profile']
        read_only_fields = ['role']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Update user data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update profile data
        if profile_data:
            profile = instance.profile
            # Jangan update profile_picture jika menggunakan JSON
            if not profile_data.get('profile_picture'):
                profile_data.pop('profile_picture', None)
            
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

# untuk update profile doctor
class DoctorProfileUpdateSerializer(serializers.ModelSerializer):
    photo_profile = serializers.ImageField(required=False)
    
    class Meta:
        model = Doctor
        fields = ['name', 'photo_profile', 'str_number', 'specialization', 'chat_fee', 'video_fee']
        read_only_fields = ['verification_status']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Untuk change password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirmation']:
            raise serializers.ValidationError({
                'new_password_confirmation': "Password fields didn't match."
            })
        return data