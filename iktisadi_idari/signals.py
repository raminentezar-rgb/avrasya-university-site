# iktisadi_idari/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import IktisadiIdariDuyuru, IktisadiIdariDosya
import os
from django.core.files import File

@receiver(post_save, sender=Duyuru)
def create_iktisadi_idari_duyuru(sender, instance, created, **kwargs):
    """
    وقتی یک اطلاعیه جدید در سیستم اصلی ایجاد شد،
    اگر مربوط به دانشکده İktisadi İdari باشد، به صورت خودکار
    در اپ iktisadi_idari نیز ایجاد شود
    """
    if instance.fakulte == 'IIBF' and instance.yayinda:
        try:
            # چک کن که آیا از قبل وجود دارد یا نه
            iktisadi_idari_duyuru, created = IktisadiIdariDuyuru.objects.get_or_create(
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
                iktisadi_idari_duyuru.baslik = instance.baslik
                iktisadi_idari_duyuru.icerik = instance.icerik
                iktisadi_idari_duyuru.ozet = instance.ozet
                iktisadi_idari_duyuru.yayin_tarihi = instance.yayin_tarihi
                iktisadi_idari_duyuru.yayinda = instance.yayinda
                iktisadi_idari_duyuru.save()
            
            # فایل‌های ضمیمه را کپی کن
            copy_attached_files(instance, iktisadi_idari_duyuru)
                
        except Exception as e:
            print(f"Hata oluştu: {e}")

def copy_attached_files(ana_duyuru, iktisadi_duyuru):
    """کپی کردن فایل‌های ضمیمه از اطلاعیه اصلی به اطلاعیه دانشکده"""
    try:
        # حذف فایل‌های قدیمی
        iktisadi_duyuru.dosyalar.all().delete()
        
        # کپی فایل‌های جدید
        for ana_dosya in ana_duyuru.dosyalar.all():
            IktisadiIdariDosya.objects.create(
                duyuru=iktisadi_duyuru,
                dosya=ana_dosya.dosya,
                dosya_adi=ana_dosya.dosya_adi,
                tur=ana_dosya.tur,
                aciklama=ana_dosya.aciklama
            )
    except Exception as e:
        print(f"Dosya kopyalama hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_iktisadi_idari_duyuru(sender, instance, **kwargs):
    """
    وقتی اطلاعیه اصلی آپدیت شد، اطلاعیه مربوطه در اپ دانشکده نیز آپدیت شود
    """
    if instance.fakulte == 'IIBF' and hasattr(instance, 'iktisadi_idari_duyuru'):
        try:
            iktisadi_idari_duyuru = instance.iktisadi_idari_duyuru
            iktisadi_idari_duyuru.baslik = instance.baslik
            iktisadi_idari_duyuru.icerik = instance.icerik
            iktisadi_idari_duyuru.ozet = instance.ozet
            iktisadi_idari_duyuru.yayin_tarihi = instance.yayin_tarihi
            iktisadi_idari_duyuru.yayinda = instance.yayinda
            iktisadi_idari_duyuru.save()
            
            # فایل‌ها را نیز آپدیت کن
            copy_attached_files(instance, iktisadi_idari_duyuru)
            
        except Exception as e:
            print(f"Güncelleme hatası: {e}")