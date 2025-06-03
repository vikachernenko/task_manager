from django import forms
from .models import Task, Criteria


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'priority']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'priority': forms.Select(choices=Task.PRIORITY_CHOICES),
        }


class CriteriaForm(forms.ModelForm):
    class Meta:
        model = Criteria
        fields = ['title', 'status', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=Criteria.STATUS_CHOICES),
            'priority': forms.Select(attrs={'class': 'form-select'}, choices=Criteria.PRIORITY_CHOICES),
        }
