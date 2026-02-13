import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import DamageClaim, DamageType
from core.models import InsurancePolicy, PolicyClause

# Configuration for simulated AI Analysis
DAMAGE_METADATA = {
    'bumper_damage': {'name': 'Bumper Damage', 'covered': True, 'base_cost': 12000},
    'windshield_damage': {'name': 'Windshield Damage', 'covered': True, 'base_cost': 15000},
    'wheel_damage': {'name': 'Wheel/Rim Damage', 'covered': False, 'base_cost': 8000},
    'door_damage': {'name': 'Door Damage', 'covered': True, 'base_cost': 18000},
}

@csrf_exempt
@require_http_methods(["POST"])
def analyze_damage(request):
    """
    Analyzes uploaded image, matches it with database Policy Clauses,
    and returns a repair estimate in NPR.
    """
    try:
        image = request.FILES.get('image')
        if not image:
            return JsonResponse({'success': False, 'error': 'No image provided'}, status=400)

        # 1. SIMULATE AI DETECTION
        # In production, replace this with: model.predict(image)
        detected_key = random.choice(list(DAMAGE_METADATA.keys()))
        meta = DAMAGE_METADATA[detected_key]
        severity = random.choice(['minor', 'moderate', 'severe'])
        confidence = random.randint(85, 99)

        # 2. DYNAMIC CLAUSE MATCHING
        # We query the Core app models to find real clauses matching the damage
        relevant_clauses = PolicyClause.objects.filter(
            title__icontains=detected_key.replace('_', ' ')
        ).values('clause_number', 'title', 'description', 'is_covered')

        # 3. CALCULATION LOGIC
        severity_multiplier = {'minor': 0.5, 'moderate': 1.0, 'severe': 2.5}
        estimated_total = meta['base_cost'] * severity_multiplier[severity]

        return JsonResponse({
            'success': True,
            'analysis': {
                'damage_type': meta['name'],
                'severity': severity,
                'confidence': f"{confidence}%",
                'is_covered': meta['covered']
            },
            'estimate': {
                'amount': estimated_total,
                'currency': 'NPR',
                'note': 'Estimated based on standard Nepal workshop rates.'
            },
            'clauses': list(relevant_clauses),
            'documents_needed': [
                'Bluebook (Original)', 
                'Driving License', 
                'Photos of spot'
            ]
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def submit_claim(request):
    """Saves the final claim to the database."""
    try:
        data = json.loads(request.body)
        claim = DamageClaim.objects.create(
            full_name=data.get('full_name'),
            vehicle_number=data.get('vehicle_number'),
            email=data.get('email'),
            phone=data.get('phone'),
            damage_description=data.get('damage_description'),
            status='pending'
        )
        return JsonResponse({'success': True, 'claim_id': claim.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_damage_types(request):
    """Returns list for frontend dropdowns."""
    types = DamageType.objects.all().values('name', 'typically_covered')
    return JsonResponse({'damage_types': list(types)})