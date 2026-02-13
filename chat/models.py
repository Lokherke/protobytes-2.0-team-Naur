from django.db import models
from core.models import InsurancePolicy


class DamageClaim(models.Model):
    """Model for insurance claims"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('eligible', 'Eligible for Claim'),
        ('not_eligible', 'Not Eligible'),
        ('needs_info', 'Needs More Information'),
    ]
    
    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('motorcycle', 'Motorcycle'),
        ('truck', 'Truck'),
        ('bus', 'Bus'),
        ('other', 'Other'),
    ]
    
    # User information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Vehicle information
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default='car')
    vehicle_number = models.CharField(max_length=50)
    insurance_policy_number = models.CharField(max_length=100, blank=True)
    
    # Policy reference
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Damage information
    damage_description = models.TextField()
    damage_image = models.ImageField(upload_to='claims/damage_images/')
    detected_damage_type = models.CharField(max_length=100, blank=True)
    damage_severity = models.CharField(max_length=20, blank=True)
    
    # AI Analysis
    ai_analysis = models.JSONField(default=dict, blank=True)
    matched_clauses = models.JSONField(default=list, blank=True)
    
    # Claim status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    eligibility_reason = models.TextField(blank=True)
    estimated_coverage = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Claim #{self.id} - {self.full_name} - {self.vehicle_number}"


class DamageType(models.Model):
    """Model for predefined damage types"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    common_causes = models.JSONField(default=list)
    typically_covered = models.BooleanField(default=True)
    required_documents = models.JSONField(default=list)
    
    def __str__(self):
        return self.name
