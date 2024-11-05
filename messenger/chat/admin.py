from django.contrib import admin
from .models import Message, CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'user_id', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'user_id', 'first_name', 'last_name')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fieldsets = [f for f in fieldsets if f[0] != 'Permissions']
        return fieldsets

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'timestamp', 'content_preview')
    search_fields = ('sender__username', 'recipient__username', 'content')
    list_filter = ('timestamp',)

    def content_preview(self, obj):
        return obj.get_content()[:50]
    content_preview.short_description = 'Message Preview'