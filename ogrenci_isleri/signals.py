from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment, Registration

@receiver(post_save, sender=Payment)
def payment_status_change(sender, instance, created, **kwargs):
    """وقتی وضعیت پرداخت تغییر کرد"""
    if not created and instance.islem_durumu == 'basarili':
        # ارسال ایمیل تایید نهایی پرداخت
        subject = f'Ödeme Tamamlandı - {instance.referans_no}'
        message = f'Sayın {instance.ad_soyad},\n\nÖdemeniz başarıyla tamamlanmıştır.\nReferans No: {instance.referans_no}\nTutar: {instance.odeme_tutari or "Belirtilmemiş"} TL\n\nTeşekkür ederiz.'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=True,
        )

@receiver(post_save, sender=Registration)
def registration_status_change(sender, instance, created, **kwargs):
    """وقتی وضعیت ثبت‌نام تغییر کرد"""
    if not created and instance.kayit_durumu == 'onaylandi':
        # ارسال ایمیل تایید نهایی ثبت‌نام
        subject = f'Kayıt Onaylandı - {instance.kayit_no}'
        message = f'Sayın {instance.ad_soyad},\n\nKayıt başvurunuz onaylanmıştır.\nKayıt No: {instance.kayit_no}\nÖğrenci No: {instance.ogrenci_no}\n\nArtık öğrenci portalını kullanabilirsiniz.\n\nTeşekkür ederiz.'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=True,
        )