from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class CallbackRequest(models.Model):
    """
    مدل درخواست تماس برای فرم Sizi Arayalım
    """
    full_name = models.CharField(
        max_length=200, 
        verbose_name="Ad Soyad"
    )
    email = models.EmailField(
        max_length=254, 
        verbose_name="E-posta"
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[0-9\-\+\s\(\)]{10,20}$',
                message='Geçerli bir telefon numarası giriniz.'
            )
        ],
        verbose_name="Telefon Numarası"
    )
    accept_communication = models.BooleanField(
        default=False,
        verbose_name="İletişim İzni"
    )
    accept_kvkk = models.BooleanField(
        default=False,
        verbose_name="KVKK Onayı"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Başvuru Tarihi"
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name="İşlendi mi?"
    )
    notes = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Notlar"
    )
    ip_address = models.GenericIPAddressField(
        blank=True, 
        null=True,
        verbose_name="IP Adresi"
    )
    user_agent = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Tarayıcı Bilgisi"
    )

    class Meta:
        verbose_name = "Geri Arama Talebi"
        verbose_name_plural = "Geri Arama Talepleri"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.phone} ({self.created_at.strftime('%d.%m.%Y')})"

    def save(self, *args, **kwargs):
        # چک‌باکس‌ها باید True باشند
        if not self.accept_communication or not self.accept_kvkk:
            raise ValueError("İletişim izni ve KVKK onayı zorunludur.")
        super().save(*args, **kwargs)