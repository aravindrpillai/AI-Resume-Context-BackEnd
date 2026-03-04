from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Patient(models.Model):
    
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("U", "Prefer not to say"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # Physical attributes
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(130)])
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(30), MaxValueValidator(300)])
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(700)])

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "patients"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["first_name", "last_name"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.pk})"

    @property
    def bmi(self):
        if self.height_cm and self.weight_kg:
            height_m = float(self.height_cm) / 100
            return round(float(self.weight_kg) / (height_m ** 2), 2)
        return None

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class PatientConversation(models.Model):
   
    SPECIALITY_CHOICES = [
        ("cardiology", "Cardiology"),
        ("dermatology", "Dermatology"),
        ("endocrinology", "Endocrinology"),
        ("gastroenterology", "Gastroenterology"),
        ("general_practice", "General Practice"),
        ("neurology", "Neurology"),
        ("oncology", "Oncology"),
        ("ophthalmology", "Ophthalmology"),
        ("orthopaedics", "Orthopaedics"),
        ("paediatrics", "Paediatrics"),
        ("psychiatry", "Psychiatry"),
        ("pulmonology", "Pulmonology"),
        ("rheumatology", "Rheumatology"),
        ("urology", "Urology"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("escalated", "Escalated to Clinician"),
    ]

    # Relationship
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="conversations",
    )

    # Session context
    speciality = models.CharField(
        max_length=50,
        choices=SPECIALITY_CHOICES,
        help_text="Medical speciality the patient is seeking",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    # Patient input
    symptom_description = models.TextField(
        help_text="Patient's description of their problem in their own words",
    )

    # AI output
    ai_diagnosis_notes = models.TextField(
        blank=True,
        null=True,
        help_text="AI-generated diagnostic notes and recommendations",
    )
    ai_suggested_tests = models.JSONField(
        blank=True,
        null=True,
        help_text="Structured list of suggested diagnostic tests",
    )
    ai_urgency_level = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ("low", "Low — Routine appointment"),
            ("medium", "Medium — See a doctor soon"),
            ("high", "High — Urgent care needed"),
            ("emergency", "Emergency — Call 999 / ER immediately"),
        ],
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "patient_conversations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["patient", "speciality"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return (
            f"Conversation #{self.pk} — {self.patient.full_name} "
            f"[{self.get_speciality_display()}] ({self.get_status_display()})"
        )
