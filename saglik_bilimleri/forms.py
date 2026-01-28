# saglik_bilimleri/forms.py
from django import forms
from .models import SaglikBilimleriDuyuru

class SaglikBilimleriDuyuruForm(forms.ModelForm):
    class Meta:
        model = SaglikBilimleriDuyuru
        fields = ['baslik', 'icerik', 'ozet', 'kategori', 'dosya', 'onemli', 'yayinda', 'sira']