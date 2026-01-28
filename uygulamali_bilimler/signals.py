# uygulamali_bilimler/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import UygulamaliBilimlerDuyuru, UygulamaliBilimlerDosya

@receiver(post_save, sender=Duyuru)
def create_uygulamali_bilimler_duyuru(sender, instance, created, **kwargs):
    if instance.fakulte == 'UBY' and instance.yayinda:  # Burada fakulte değerini kontrol edin
        try:
            uygulamali_bilimler_duyuru, created = UygulamaliBilimlerDuyuru.objects.get_or_create(
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
                uygulamali_bilimler_duyuru.baslik = instance.baslik
                uygulamali_bilimler_duyuru.icerik = instance.icerik
                uygulamali_bilimler_duyuru.ozet = instance.ozet
                uygulamali_bilimler_duyuru.yayin_tarihi = instance.yayin_tarihi
                uygulamali_bilimler_duyuru.yayinda = instance.yayinda
                uygulamali_bilimler_duyuru.save()
            
            copy_attached_files(instance, uygulamali_bilimler_duyuru)
                
        except Exception as e:
            print(f"Hata oluştu: {e}")

def copy_attached_files(ana_duyuru, uygulamali_duyuru):
    try:
        uygulamali_duyuru.dosyalar.all().delete()
        
        for ana_dosya in ana_duyuru.dosyalar.all():
            UygulamaliBilimlerDosya.objects.create(
                duyuru=uygulamali_duyuru,
                dosya=ana_dosya.dosya,
                dosya_adi=ana_dosya.dosya_adi,
                tur=ana_dosya.tur,
                aciklama=ana_dosya.aciklama
            )
    except Exception as e:
        print(f"Dosya kopyalama hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_uygulamali_bilimler_duyuru(sender, instance, **kwargs):
    if instance.fakulte == 'UYG_BIL' and hasattr(instance, 'uygulamali_bilimler_duyuru'):  # Burada fakulte değerini kontrol edin
        try:
            uygulamali_bilimler_duyuru = instance.uygulamali_bilimler_duyuru
            uygulamali_bilimler_duyuru.baslik = instance.baslik
            uygulamali_bilimler_duyuru.icerik = instance.icerik
            uygulamali_bilimler_duyuru.ozet = instance.ozet
            uygulamali_bilimler_duyuru.yayin_tarihi = instance.yayin_tarihi
            uygulamali_bilimler_duyuru.yayinda = instance.yayinda
            uygulamali_bilimler_duyuru.save()
            
            copy_attached_files(instance, uygulamali_bilimler_duyuru)
            
        except Exception as e:
            print(f"Güncelleme hatası: {e}")