from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import LeeDuyuru

@receiver(post_save, sender=Duyuru)
def sync_duyuru_to_lee(sender, instance, created, **kwargs):
    if kwargs.get('raw'):
        return
    """
    وقتی یک اطلاعیه در سیستم اصلی ایجاد یا ویرایش می‌شود،
    تنها در صورتی که مربوط به دانشکده/انستیتو LEE باشد در اپ LEE همگام‌سازی می‌شود.
    """
    if instance.fakulte == 'LEE' and instance.yayinda:
        lee_duyuru, created = LeeDuyuru.objects.get_or_create(
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
            lee_duyuru.baslik = instance.baslik
            lee_duyuru.icerik = instance.icerik
            lee_duyuru.ozet = instance.ozet
            lee_duyuru.yayin_tarihi = instance.yayin_tarihi
            lee_duyuru.yayinda = instance.yayinda
            lee_duyuru.save()
    else:
        # اگر اطلاعیه به دانشکده دیگری تعلق دارد یا غیرفعال است، از LEE حذف شود
        LeeDuyuru.objects.filter(ana_duyuru=instance).delete()