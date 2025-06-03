from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Criteria(models.Model):
    title = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('to do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(default=timezone.now)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    criterion = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='medium')

    def time_remaining(self):
        if self.deadline:
            remaining = self.deadline - timezone.now()
            if remaining.days < 0:
                return "Просрочено"
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            return f"{hours}ч {minutes}м"
        return "Нет срока"
