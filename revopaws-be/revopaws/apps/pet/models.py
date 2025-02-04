from django.db import models
from django.conf import settings

class Pet(models.Model):
    PET_TYPE_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('reptile', 'Reptile'),
        ('other', 'Other'),
    ]

    pet_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets'
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES)
    breed = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class PetMedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    visit_date = models.DateTimeField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Medical Record for {self.pet.name} on {self.visit_date}"
