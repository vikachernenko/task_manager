from django.contrib import admin
from .models import Criteria, Task


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('title',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'criterion', 'user', 'deadline', 'created_at')
    list_filter = ('criterion', 'user', 'deadline')
    search_fields = ('title', 'description')
