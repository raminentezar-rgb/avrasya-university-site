# fen_edebiyat/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import FenEdebiyatDuyuru, FenEdebiyatDosya
import os
from django.core.files import File

@receiver(post_save, sender=Duyuru)
def create_fen_edebiyat_duyuru(sender, instance, created, **kwargs):
    """
    وقتی یک اطلاعیه جدید در سیستم اصلی ایجاد شد،
    اگر مربوط به دانشکده Fen Edebiyat باشد، به صورت خودکار
    در اپ fen_edebiyat نیز ایجاد شود
    """
    if instance.fakulte == 'FEF' and instance.yayinda:
        try:
            # چک کن که آیا از قبل وجود دارد یا نه
            fen_edebiyat_duyuru, created = FenEdebiyatDuyuru.objects.get_or_create(
                ana_duyuru=instance,
                defaults={
                    'baslik': instance.baslik,
                    'icerik': instance.icerik,
                    'ozet': instance.ozet,
                    'yayin_tarihi': instance.yayin_tarihi,
                    'yayinda': instance.yayinda,
                    'kategori': 'genel'
                }
            )
            
            if not created:
                # اگر از قبل وجود داشت، اطلاعات را آپدیت کن
                fen_edebiyat_duyuru.baslik = instance.baslik
                fen_edebiyat_duyuru.icerik = instance.icerik
                fen_edebiyat_duyuru.ozet = instance.ozet
                fen_edebiyat_duyuru.yayin_tarihi = instance.yayin_tarihi
                fen_edebiyat_duyuru.yayinda = instance.yayinda
                fen_edebiyat_duyuru.save()
            
            # فایل‌های ضمیمه را کپی کن
            copy_attached_files(instance, fen_edebiyat_duyuru)
                
        except Exception as e:
            print(f"Hata oluştu: {e}")

def copy_attached_files(ana_duyuru, fen_duyuru):
    """کپی کردن فایل‌های ضمیمه از اطلاعیه اصلی به اطلاعیه دانشکده"""
    try:
        # حذف فایل‌های قدیمی
        fen_duyuru.dosyalar.all().delete()
        
        # کپی فایل‌های جدید
        for ana_dosya in ana_duyuru.dosyalar.all():
            FenEdebiyatDosya.objects.create(
                duyuru=fen_duyuru,
                dosya=ana_dosya.dosya,
                dosya_adi=ana_dosya.dosya_adi,
                tur=ana_dosya.tur,
                aciklama=ana_dosya.aciklama
            )
    except Exception as e:
        print(f"Dosya kopyalama hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_fen_edebiyat_duyuru(sender, instance, **kwargs):
    """
    وقتی اطلاعیه اصلی آپدیت شد، اطلاعیه مربوطه در اپ دانشکده نیز آپدیت شود
    """
    if instance.fakulte == 'FEF' and hasattr(instance, 'fen_edebiyat_duyuru'):
        try:
            fen_edebiyat_duyuru = instance.fen_edebiyat_duyuru
            fen_edebiyat_duyuru.baslik = instance.baslik
            fen_edebiyat_duyuru.icerik = instance.icerik
            fen_edebiyat_duyuru.ozet = instance.ozet
            fen_edebiyat_duyuru.yayin_tarihi = instance.yayin_tarihi
            fen_edebiyat_duyuru.yayinda = instance.yayinda
            fen_edebiyat_duyuru.save()
            
            # فایل‌ها را نیز آپدیت کن
            copy_attached_files(instance, fen_edebiyat_duyuru)
            
        except Exception as e:
            print(f"Güncelleme hatası: {e}")