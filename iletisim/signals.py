# iletisim/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import IletisimDuyuru

@receiver(post_save, sender=Duyuru)
def create_iletisim_duyuru(sender, instance, created, **kwargs):
    """
    وقتی یک اطلاعیه جدید در سیستم اصلی ایجاد شد،
    اگر مربوط به بخش ارتباطات باشد، به صورت خودکار
    در اپ iletisim نیز ایجاد شود
    """
    if instance.fakulte == 'ILTF' and instance.yayinda:  # یا فیلد مناسب دیگر
        try:
            # چک کن که آیا از قبل وجود دارد یا نه
            iletisim_duyuru, created = IletisimDuyuru.objects.get_or_create(
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
                iletisim_duyuru.baslik = instance.baslik
                iletisim_duyuru.icerik = instance.icerik
                iletisim_duyuru.ozet = instance.ozet
                iletisim_duyuru.yayin_tarihi = instance.yayin_tarihi
                iletisim_duyuru.yayinda = instance.yayinda
                iletisim_duyuru.save()
                
        except Exception as e:
            print(f"İletişim duyuru hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_iletisim_duyuru(sender, instance, **kwargs):
    """
    وقتی اطلاعیه اصلی آپدیت شد، اطلاعیه مربوطه در اپ ارتباطات نیز آپدیت شود
    """
    if instance.fakulte == 'ILETISIM' and hasattr(instance, 'iletisim_duyuru'):
        try:
            iletisim_duyuru = instance.iletisim_duyuru
            iletisim_duyuru.baslik = instance.baslik
            iletisim_duyuru.icerik = instance.icerik
            iletisim_duyuru.ozet = instance.ozet
            iletisim_duyuru.yayin_tarihi = instance.yayin_tarihi
            iletisim_duyuru.yayinda = instance.yayinda
            iletisim_duyuru.save()
        except Exception as e:
            print(f"İletişim güncelleme hatası: {e}")