# muhendislik_mimarlik/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import MuhendislikMimarlikDuyuru

@receiver(post_save, sender=Duyuru)
def create_muhendislik_mimarlik_duyuru(sender, instance, created, **kwargs):
    """
    وقتی یک اطلاعیه جدید در سیستم اصلی ایجاد شد،
    اگر مربوط به دانشکده Mühendislik Mimarlık باشد، به صورت خودکار
    در اپ muhendislik_mimarlik نیز ایجاد شود
    """
    if instance.fakulte == 'MMF' and instance.yayinda:
        try:
            # چک کن که آیا از قبل وجود دارد یا نه
            muhendislik_mimarlik_duyuru, created = MuhendislikMimarlikDuyuru.objects.get_or_create(
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
                muhendislik_mimarlik_duyuru.baslik = instance.baslik
                muhendislik_mimarlik_duyuru.icerik = instance.icerik
                muhendislik_mimarlik_duyuru.ozet = instance.ozet
                muhendislik_mimarlik_duyuru.yayin_tarihi = instance.yayin_tarihi
                muhendislik_mimarlik_duyuru.yayinda = instance.yayinda
                muhendislik_mimarlik_duyuru.save()
                
        except Exception as e:
            print(f"Mühendislik Mimarlık duyuru hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_muhendislik_mimarlik_duyuru(sender, instance, **kwargs):
    """
    وقتی اطلاعیه اصلی آپدیت شد، اطلاعیه مربوطه در اپ دانشکده نیز آپدیت شود
    """
    if instance.fakulte == 'MMF' and hasattr(instance, 'muhendislik_mimarlik_duyuru'):
        try:
            muhendislik_mimarlik_duyuru = instance.muhendislik_mimarlik_duyuru
            muhendislik_mimarlik_duyuru.baslik = instance.baslik
            muhendislik_mimarlik_duyuru.icerik = instance.icerik
            muhendislik_mimarlik_duyuru.ozet = instance.ozet
            muhendislik_mimarlik_duyuru.yayin_tarihi = instance.yayin_tarihi
            muhendislik_mimarlik_duyuru.yayinda = instance.yayinda
            muhendislik_mimarlik_duyuru.save()
        except Exception as e:
            print(f"Mühendislik Mimarlık güncelleme hatası: {e}")