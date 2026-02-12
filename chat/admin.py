from django.contrib import admin
from .models import ChatSession, ChatMessage
from .models import DamageClaim, DamageType



class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['timestamp']


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'message_count']
    inlines = [ChatMessageInline]
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp']
    list_filter = ['message_type']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'

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
