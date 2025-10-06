
# In feedback/admin.py

from django.contrib import admin
from .models import UserStory

@admin.register(UserStory)
class UserStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'pet', 'created_date')
    list_filter = ('user', 'pet')
    search_fields = ('title', 'content', 'user__username')