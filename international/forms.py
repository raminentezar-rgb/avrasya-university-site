from django import forms
from .models import InternationalApplication

class InternationalApplicationForm(forms.ModelForm):
    class Meta:
        model = InternationalApplication
        fields = [
            'first_name', 'last_name', 'birth_date', 'gender', 'email', 'phone',
            'country', 'city', 'address',
            'program', 'semester', 'education_level', 'english_level',
            'passport_copy', 'diploma_certificate', 'academic_transcript', 'passport_photo',
            'newsletter_subscription'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
