from django import forms
from .models import CallbackRequest
from django.core.validators import RegexValidator, EmailValidator
import re

class CallbackRequestForm(forms.ModelForm):
    """
    فرم درخواست تماس
    """
    class Meta:
        model = CallbackRequest
        fields = ['full_name', 'email', 'phone', 'accept_communication', 'accept_kvkk']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lütfen adınızı ve soyadınızı giriniz',
                'id': 'fullName'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ornek@email.com',
                'id': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(5XX) XXX XX XX',
                'id': 'phone'
            }),
            'accept_communication': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'acceptCommunication'
            }),
            'accept_kvkk': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'acceptKVKK'
            }),
        }
        labels = {
            'full_name': 'Ad Soyad',
            'email': 'E-posta',
            'phone': 'Telefon Numarası',
            'accept_communication': 'İletişim İzni',
            'accept_kvkk': 'KVKK Onayı',
        }

    def clean_phone(self):
        """
        اعتبارسنجی شماره تلفن
        """
        phone = self.cleaned_data.get('phone')
        if phone:
            # حذف کاراکترهای غیرعددی
            phone_clean = re.sub(r'[^\d+]', '', phone)
            
            # شماره تلفن ترکیه باید با 0 یا +90 شروع شود و 10-11 رقم باشد
            if not re.match(r'^(\+90|0)?[0-9]{10,11}$', phone_clean):
                raise forms.ValidationError('Geçerli bir Türkiye telefon numarası giriniz.')
            
            # اگر شماره با 0 شروع شده بود، +90 اضافه کنیم
            if phone_clean.startswith('0'):
                phone_clean = '+9' + phone_clean
            
            return phone_clean
        return phone

    def clean_email(self):
        """
        اعتبارسنجی ایمیل
        """
        email = self.cleaned_data.get('email')
        if email:
            # اعتبارسنجی پیشرفته ایمیل
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise forms.ValidationError('Geçerli bir e-posta adresi giriniz.')
            
            # جلوگیری از ایمیل‌های یکبار مصرف (اختیاری)
            disposable_domains = ['tempmail.com', 'throwaway.com', 'mailinator.com']
            domain = email.split('@')[1]
            if domain.lower() in disposable_domains:
                raise forms.ValidationError('Geçici e-posta adresleri kabul edilmemektedir.')
        
        return email

    def clean(self):
        """
        اعتبارسنجی کلی فرم
        """
        cleaned_data = super().clean()
        accept_communication = cleaned_data.get('accept_communication')
        accept_kvkk = cleaned_data.get('accept_kvkk')

        if not accept_communication:
            self.add_error('accept_communication', 'İletişim izni vermelisiniz.')
        
        if not accept_kvkk:
            self.add_error('accept_kvkk', 'KVKK onayı vermelisiniz.')

        return cleaned_data