from django.db import models


class InsurancePolicy(models.Model):
    """Model for insurance policies"""
    POLICY_TYPES = [
        ('vehicle', 'Vehicle Insurance'),
        ('health', 'Health Insurance'),
        ('property', 'Property Insurance'),
        ('life', 'Life Insurance'),
    ]
    
    name = models.CharField(max_length=200)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    provider = models.CharField(max_length=200)
    description = models.TextField()
    coverage_details = models.JSONField(default=dict)
    exclusions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.provider}"


class PolicyClause(models.Model):
    """Model for individual policy clauses"""
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name='clauses')
    clause_number = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_covered = models.BooleanField(default=True)
    conditions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.clause_number}: {self.title}"
