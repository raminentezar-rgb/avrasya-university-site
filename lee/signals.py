from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import LeeDuyuru

@receiver(post_save, sender=Duyuru)
def sync_duyuru_to_lee(sender, instance, created, **kwargs):
    """
    وقتی یک اطلاعیه جدید در سیستم اصلی ایجاد می‌شود،
    به صورت اتوماتیک در LEE نیز کپی می‌شود.
    """
    if created:
        # بررسی کنید که آیا این اطلاعیه مربوط به دانشکده LEE است
        # (مثلاً بر اساس فیلد fakulte یا bolumler)
        # این منطق را بر اساس نیاز خود تنظیم کنید
        
        # ایجاد اطلاعیه LEE
        LeeDuyuru.objects.create(
            ana_duyuru=instance,
            baslik=instance.baslik,
            icerik=instance.icerik,
            ozet=instance.ozet,
            yayin_tarihi=instance.yayin_tarihi,
            yayinda=instance.yayinda
        )