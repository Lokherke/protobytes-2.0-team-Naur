from django.contrib import admin
from .models import InsurancePolicy, PolicyClause


class PolicyClauseInline(admin.TabularInline):
    model = PolicyClause
    extra = 1


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ['name', 'policy_type', 'provider', 'created_at']
    list_filter = ['policy_type', 'provider']
    search_fields = ['name', 'provider']
    inlines = [PolicyClauseInline]


@admin.register(PolicyClause)
class PolicyClauseAdmin(admin.ModelAdmin):
    list_display = ['clause_number', 'title', 'policy', 'is_covered']
    list_filter = ['is_covered', 'policy']
    search_fields = ['title', 'description']
