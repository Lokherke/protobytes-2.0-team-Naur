from django.shortcuts import render
from django.http import JsonResponse
from .models import InsurancePolicy


def home(request):
    """Render the main landing page"""
    return render(request, 'core/home.html')


def about(request):
    """Render the about page"""
    return render(request, 'core/about.html')


def api_policies(request):
    """API endpoint to get all policies"""
    policies = InsurancePolicy.objects.all()
    data = []
    for policy in policies:
        data.append({
            'id': policy.id,
            'name': policy.name,
            'policy_type': policy.get_policy_type_display(),
            'provider': policy.provider,
            'description': policy.description,
        })
    return JsonResponse({'policies': data})
