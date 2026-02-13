from django.contrib import admin
from .models import DamageClaim, DamageType


@admin.register(DamageClaim)
class DamageClaimAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'vehicle_number', 'detected_damage_type', 'status', 'created_at']
    list_filter = ['status', 'vehicle_type', 'detected_damage_type']
    search_fields = ['full_name', 'email', 'vehicle_number', 'insurance_policy_number']
    readonly_fields = ['created_at', 'updated_at', 'ai_analysis', 'matched_clauses']


@admin.register(DamageType)
class DamageTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'typically_covered']
    list_filter = ['typically_covered']
    search_fields = ['name', 'description']
