from django.contrib import admin
from .models import Message, Group

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'created_by', 'created_at', 'likes', 'group']
    
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_id', 'group_name', 'created_at', 'members']
    

