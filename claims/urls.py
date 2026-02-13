from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_damage, name='analyze_damage'),
    path('submit/', views.submit_claim, name='submit_claim'),
    path('status/<int:claim_id>/', views.get_claim_status, name='get_claim_status'),
    path('damage-types/', views.get_damage_types, name='get_damage_types'),
    path('rejection-reasons/', views.get_rejection_reasons, name='get_rejection_reasons'),
]
