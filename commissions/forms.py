from django import forms
from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ('title', 'author', 'description', 'status',)
        widgets = {
            'author': forms.Select(attrs={
                "style": "pointer-events: none; background-color : #CCCCCC",
                "tabindex": "-1",
            })
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('commission', 'role', 'manpower_required', 'status',)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('job',)
