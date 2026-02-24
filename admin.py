from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'due_date', 'completed', 'user')
    list_filter = ('status', 'completed', 'due_date')
    search_fields = ('title', 'description')