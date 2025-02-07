from rest_framework import serializers
from .models import Consultation, DoctorReview, ConsultationRoom
from apps.users.serializers import UserSerializer, DoctorProfileSerializer
from apps.users.models import Doctor
from apps.chatrealtime.models import ChatRealtime

class ConsultationRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationRoom
        fields = ['room_id', 'status', 'doctor_joined_at', 'closed_at', 'created_at']
        read_only_fields = fields

class ConsultationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    doctor = DoctorProfileSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    room = ConsultationRoomSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'user', 'doctor', 'doctor_id',
            'consultation_type', 'consultation_date',
            'status', 'payment_status', 'room',
            'created_at', 'completed_at'
        ]
        read_only_fields = ['status', 'payment_status', 'completed_at']

    def validate_doctor_id(self, value):
        try:
            doctor = Doctor.objects.get(id=value)
            if doctor.verification_status != 'approved':
                raise serializers.ValidationError("This doctor is not available for consultation")
            
            # Cek apakah dokter sedang dalam konsultasi lain
            active_consultation = Consultation.objects.filter(
                doctor=doctor,
                status='ongoing'
            ).exists()
            
            if active_consultation:
                raise serializers.ValidationError("Doctor is currently in another consultation")
                
            return value
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Invalid doctor ID")

class ChatRealtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRealtime
        fields = ['chat_id', 'message', 'message_type', 'timestamp', 'is_read']
        read_only_fields = ['chat_id', 'timestamp']

    def create(self, validated_data):
        consultation = self.context['consultation']
        if consultation.status != 'ongoing':
            raise serializers.ValidationError("Consultation is not active")
        return ChatRealtime.objects.create(**validated_data)

class DoctorReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    doctor = DoctorProfileSerializer(read_only=True)

    class Meta:
        model = DoctorReview
        fields = ['id', 'user', 'doctor', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'doctor']

    def create(self, validated_data):
        consultation = self.context['consultation']
        validated_data['consultation'] = consultation
        validated_data['user'] = consultation.user
        validated_data['doctor'] = consultation.doctor
        return super().create(validated_data)

    def validate(self, data):
        consultation = self.context['consultation']
        if consultation.status != 'completed':
            raise serializers.ValidationError("Can't review uncompleted consultation")
        if hasattr(consultation, 'review'):
            raise serializers.ValidationError("This consultation has already been reviewed")
        return data