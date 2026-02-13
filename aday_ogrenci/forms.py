from django import forms
from .models import AdayIletisim

class AdayIletisimForm(forms.ModelForm):
    class Meta:
        model = AdayIletisim
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız Soyadınız'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta adresiniz'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefon numaranız'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Mesajınız...',
                'rows': 4
            }),
        }