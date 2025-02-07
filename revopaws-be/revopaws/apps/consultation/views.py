from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Consultation, DoctorReview, ConsultationRoom
from .serializers import ConsultationSerializer, DoctorReviewSerializer
from apps.users.models import Doctor
from django.utils import timezone
import uuid

class ConsultationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'user':
            consultations = Consultation.objects.filter(user=request.user)
        elif request.user.role == 'doctor':
            consultations = Consultation.objects.filter(doctor=request.user.doctor_profile)
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid user role'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ConsultationSerializer(consultations, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def post(self, request):
        if request.user.role != 'user':
            return Response({
                'status': 'error',
                'message': 'Only users can create consultations'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'message': 'Consultation created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ConsultationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        consultation = get_object_or_404(Consultation, pk=pk)
        
        # Cek user punya akses ke konsultasi ini
        if not (request.user == consultation.user or 
                (request.user.role == 'doctor' and request.user.doctor_profile == consultation.doctor)):

            return Response({
                'status': 'error',
                'message': 'You do not have permission to view this consultation'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ConsultationSerializer(consultation)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

class DoctorReviewCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, consultation_id):
        if request.user.role != 'user':
            return Response({
                'status': 'error',
                'message': 'Only users can create reviews'
            }, status=status.HTTP_403_FORBIDDEN)

        consultation = get_object_or_404(Consultation, id=consultation_id, user=request.user)
        
        serializer = DoctorReviewSerializer(
            data=request.data,
            context={'consultation': consultation}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Review submitted successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ConsultationBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'user':
            return Response({
                'status': 'error',
                'message': 'Only users can book consultations'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            # Create consultation
            consultation = serializer.save(
                user=request.user,
                status='pending',
                payment_status='pending'
            )
            
            # Create room
            room_id = f"room_{uuid.uuid4().hex[:10]}"
            ConsultationRoom.objects.create(
                consultation=consultation,
                room_id=room_id,
                status='waiting'
            )

            return Response({
                'status': 'success',
                'message': 'Consultation booked successfully. Please proceed with payment.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ConsultationPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, id=consultation_id, user=request.user)
        
        if consultation.payment_status == 'paid':
            return Response({
                'status': 'error',
                'message': 'Consultation is already paid'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Nanti disini tambahin payment gateway
        # Sekarang mah tandain paid dulu aja
        consultation.payment_status = 'paid'
        consultation.status = 'paid'
        consultation.save()

        return Response({
            'status': 'success',
            'message': 'Payment successful',
            'data': ConsultationSerializer(consultation).data
        })

class ConsultationStartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, consultation_id):
        if request.user.role == 'user':
            consultation = get_object_or_404(Consultation, id=consultation_id, user=request.user)
        else:
            consultation = get_object_or_404(Consultation, id=consultation_id, doctor__user=request.user)

        if consultation.payment_status != 'paid':
            return Response({
                'status': 'error',
                'message': 'Consultation is not paid yet'
            }, status=status.HTTP_400_BAD_REQUEST)

        if consultation.status == 'ongoing':
            return Response({
                'status': 'error',
                'message': 'Consultation is already ongoing'
            }, status=status.HTTP_400_BAD_REQUEST)

        consultation.status = 'ongoing'
        consultation.save()

        room = consultation.room
        room.status = 'active'
        room.doctor_joined_at = timezone.now()
        room.save()

        return Response({
            'status': 'success',
            'message': 'Consultation started',
            'data': ConsultationSerializer(consultation).data
        })

class ConsultationEndView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, consultation_id):
        if request.user.role == 'user':
            consultation = get_object_or_404(Consultation, id=consultation_id, user=request.user)
        else:
            return Response({
                'status': 'error',
                'message': 'Only users can end consultations'
            }, status=status.HTTP_403_FORBIDDEN)

        if consultation.status != 'ongoing':
            return Response({
                'status': 'error',
                'message': 'Consultation is not ongoing'
            }, status=status.HTTP_400_BAD_REQUEST)

        consultation.status = 'completed'
        consultation.completed_at = timezone.now()
        consultation.save()

        room = consultation.room
        if room:
            room.status = 'closed'
            room.closed_at = timezone.now()
            room.save()

        return Response({
            'status': 'success',
            'message': 'Consultation ended successfully',
            'data': ConsultationSerializer(consultation).data
        })
