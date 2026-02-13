# meslek_yuksekokulu/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import MeslekYuksekokuluDuyuru, MeslekYuksekokuluDosya

@receiver(post_save, sender=Duyuru)
def create_meslek_yuksekokulu_duyuru(sender, instance, created, **kwargs):
    if instance.fakulte == 'MYO' and instance.yayinda:
        try:
            meslek_yuksekokulu_duyuru, created = MeslekYuksekokuluDuyuru.objects.get_or_create(
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
                meslek_yuksekokulu_duyuru.baslik = instance.baslik
                meslek_yuksekokulu_duyuru.icerik = instance.icerik
                meslek_yuksekokulu_duyuru.ozet = instance.ozet
                meslek_yuksekokulu_duyuru.yayin_tarihi = instance.yayin_tarihi
                meslek_yuksekokulu_duyuru.yayinda = instance.yayinda
                meslek_yuksekokulu_duyuru.save()
            
            copy_attached_files(instance, meslek_yuksekokulu_duyuru)
                
        except Exception as e:
            print(f"Hata oluştu: {e}")

def copy_attached_files(ana_duyuru, meslek_duyuru):
    try:
        meslek_duyuru.dosyalar.all().delete()
        
        for ana_dosya in ana_duyuru.dosyalar.all():
            MeslekYuksekokuluDosya.objects.create(
                duyuru=meslek_duyuru,
                dosya=ana_dosya.dosya,
                dosya_adi=ana_dosya.dosya_adi,
                tur=ana_dosya.tur,
                aciklama=ana_dosya.aciklama
            )
    except Exception as e:
        print(f"Dosya kopyalama hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_meslek_yuksekokulu_duyuru(sender, instance, **kwargs):
    if instance.fakulte == 'MYO' and hasattr(instance, 'meslek_yuksekokulu_duyuru'):
        try:
            meslek_yuksekokulu_duyuru = instance.meslek_yuksekokulu_duyuru
            meslek_yuksekokulu_duyuru.baslik = instance.baslik
            meslek_yuksekokulu_duyuru.icerik = instance.icerik
            meslek_yuksekokulu_duyuru.ozet = instance.ozet
            meslek_yuksekokulu_duyuru.yayin_tarihi = instance.yayin_tarihi
            meslek_yuksekokulu_duyuru.yayinda = instance.yayinda
            meslek_yuksekokulu_duyuru.save()
            
            copy_attached_files(instance, meslek_yuksekokulu_duyuru)
            
        except Exception as e:
            print(f"Güncelleme hatası: {e}")