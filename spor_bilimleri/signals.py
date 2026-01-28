# spor_bilimleri/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import SporBilimleriDuyuru

@receiver(post_save, sender=Duyuru)
def create_spor_bilimleri_duyuru(sender, instance, created, **kwargs):
    """
    وقتی یک اطلاعیه جدید در سیستم اصلی ایجاد شد،
    اگر مربوط به دانشکده Spor Bilimleri باشد، به صورت خودکار
    در اپ spor_bilimleri نیز ایجاد شود
    """
    if instance.fakulte == 'SPOR' and instance.yayinda:
        try:
            # چک کن که آیا از قبل وجود دارد یا نه
            spor_bilimleri_duyuru, created = SporBilimleriDuyuru.objects.get_or_create(
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
                spor_bilimleri_duyuru.baslik = instance.baslik
                spor_bilimleri_duyuru.icerik = instance.icerik
                spor_bilimleri_duyuru.ozet = instance.ozet
                spor_bilimleri_duyuru.yayin_tarihi = instance.yayin_tarihi
                spor_bilimleri_duyuru.yayinda = instance.yayinda
                spor_bilimleri_duyuru.save()
                
        except Exception as e:
            print(f"Spor Bilimleri duyuru hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_spor_bilimleri_duyuru(sender, instance, **kwargs):
    """
    وقتی اطلاعیه اصلی آپدیت شد، اطلاعیه مربوطه در اپ دانشکده نیز آپدیت شود
    """
    if instance.fakulte == 'SPOR' and hasattr(instance, 'spor_bilimleri_duyuru'):
        try:
            spor_bilimleri_duyuru = instance.spor_bilimleri_duyuru
            spor_bilimleri_duyuru.baslik = instance.baslik
            spor_bilimleri_duyuru.icerik = instance.icerik
            spor_bilimleri_duyuru.ozet = instance.ozet
            spor_bilimleri_duyuru.yayin_tarihi = instance.yayin_tarihi
            spor_bilimleri_duyuru.yayinda = instance.yayinda
            spor_bilimleri_duyuru.save()
        except Exception as e:
            print(f"Spor Bilimleri güncelleme hatası: {e}")