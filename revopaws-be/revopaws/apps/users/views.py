from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer, DoctorRegisterSerializer, DoctorLoginSerializer, UserUpdateSerializer, DoctorProfileUpdateSerializer, ChangePasswordSerializer
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import update_session_auth_hash
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# login user biasa
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            
            # Generate token
            refresh = RefreshToken.for_user(user)
            
            # Serialize user data
            user_serializer = UserSerializer(user)
            
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'user': user_serializer.data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_200_OK)
            
        return Response({
            'status': 'error',
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# register user biasa
class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate token
            refresh = RefreshToken.for_user(user)
            
            # Serialize user data
            user_serializer = UserSerializer(user)
            
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'user': user_serializer.data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# register doctor
class DoctorRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DoctorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({
                'status': 'success',
                'message': 'Registration successful. Please wait for admin verification.',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'verification_status': 'pending'
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# login doctor
class DoctorLoginView(APIView):
    permission_classes = [AllowAny]
    

    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            
            # Generate token
            refresh = RefreshToken.for_user(user)
            
            # Get doctor profile
            doctor = user.doctor_profile
            
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'doctor_profile': {
                            'name': doctor.name,
                            'specialization': doctor.specialization,
                            'verification_status': doctor.verification_status
                        }
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_200_OK)
            
        return Response({
            'status': 'error',
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# update profile user
class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get(self, request):
        if request.user.role != 'user':
            raise PermissionDenied("Only regular users can access this endpoint")
        
        serializer = UserSerializer(request.user)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def put(self, request):
        if request.user.role != 'user':
            raise PermissionDenied("Only regular users can access this endpoint")
        
        # Handle form-data untuk upload file
        if request.content_type.startswith('multipart'):
            profile_data = {
                'profile': {
                    'profile_picture': request.FILES.get('profile_picture')
                }
            }
            serializer = UserUpdateSerializer(request.user, data=profile_data, partial=True)
        else:
            # Handle JSON data untuk update normal
            serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
            
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Profile updated successfully',
                'data': UserSerializer(user).data
            })
        return Response({
            'status': 'error',
            'message': 'Update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.user.role != 'user':
            raise PermissionDenied("Only regular users can access this endpoint")
        
        request.user.delete()
        return Response({
            'status': 'success',
            'message': 'Account deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

# update profile doctor
class DoctorProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can access this endpoint")
        
        doctor = request.user.doctor_profile
        return Response({
            'status': 'success',
            'data': {
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'doctor_profile': DoctorProfileUpdateSerializer(doctor).data
                }
            }
        })

    def put(self, request):
        if request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can access this endpoint")
        
        doctor = request.user.doctor_profile
        serializer = DoctorProfileUpdateSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            doctor = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Profile updated successfully',
                'data': {
                    'user': {
                        'id': request.user.id,
                        'username': request.user.username,
                        'email': request.user.email,
                        'doctor_profile': DoctorProfileUpdateSerializer(doctor).data
                    }
                }
            })
        return Response({
            'status': 'error',
            'message': 'Update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can access this endpoint")
        
        request.user.delete()
        return Response({
            'status': 'success',
            'message': 'Account deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                return Response({
                    'status': 'success',
                    'message': 'Password updated successfully'
                })
            return Response({
                'status': 'error',
                'message': 'Incorrect old password'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)