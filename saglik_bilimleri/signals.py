# saglik_bilimleri/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import SaglikBilimleriDuyuru, SaglikBilimleriDosya

@receiver(post_save, sender=Duyuru)
def create_saglik_bilimleri_duyuru(sender, instance, created, **kwargs):
    """
    وقتی یک اطلاعیه جدید در سیستم اصلی ایجاد شد،
    اگر مربوط به دانشکده Sağlık Bilimleri باشد، به صورت خودکار
    در اپ saglik_bilimleri نیز ایجاد شود
    """
    if instance.fakulte == 'SBF' and instance.yayinda:
        try:
            # چک کن که آیا از قبل وجود دارد یا نه
            saglik_bilimleri_duyuru, created = SaglikBilimleriDuyuru.objects.get_or_create(
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
                saglik_bilimleri_duyuru.baslik = instance.baslik
                saglik_bilimleri_duyuru.icerik = instance.icerik
                saglik_bilimleri_duyuru.ozet = instance.ozet
                saglik_bilimleri_duyuru.yayin_tarihi = instance.yayin_tarihi
                saglik_bilimleri_duyuru.yayinda = instance.yayinda
                saglik_bilimleri_duyuru.save()
            
            # فایل‌های ضمیمه را کپی کن
            copy_attached_files(instance, saglik_bilimleri_duyuru)
                
        except Exception as e:
            print(f"Sağlık Bilimleri duyuru oluşturma hatası: {e}")

def copy_attached_files(ana_duyuru, saglik_duyuru):
    """کپی کردن فایل‌های ضمیمه از اطلاعیه اصلی به اطلاعیه دانشکده"""
    try:
        # حذف فایل‌های قدیمی
        saglik_duyuru.dosyalar.all().delete()
        
        # کپی فایل‌های جدید
        for ana_dosya in ana_duyuru.dosyalar.all():
            SaglikBilimleriDosya.objects.create(
                duyuru=saglik_duyuru,
                dosya=ana_dosya.dosya,
                dosya_adi=ana_dosya.dosya_adi,
                tur=ana_dosya.tur,
                aciklama=ana_dosya.aciklama
            )
    except Exception as e:
        print(f"Dosya kopyalama hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_saglik_bilimleri_duyuru(sender, instance, **kwargs):
    """
    وقتی اطلاعیه اصلی آپدیت شد، اطلاعیه مربوطه در اپ دانشکده نیز آپدیت شود
    """
    if instance.fakulte == 'SBF' and hasattr(instance, 'saglik_bilimleri_duyuru'):
        try:
            saglik_bilimleri_duyuru = instance.saglik_bilimleri_duyuru
            saglik_bilimleri_duyuru.baslik = instance.baslik
            saglik_bilimleri_duyuru.icerik = instance.icerik
            saglik_bilimleri_duyuru.ozet = instance.ozet
            saglik_bilimleri_duyuru.yayin_tarihi = instance.yayin_tarihi
            saglik_bilimleri_duyuru.yayinda = instance.yayinda
            saglik_bilimleri_duyuru.save()
            
            # فایل‌ها را نیز آپدیت کن
            copy_attached_files(instance, saglik_bilimleri_duyuru)
            
        except Exception as e:
            print(f"Sağlık Bilimleri güncelleme hatası: {e}")