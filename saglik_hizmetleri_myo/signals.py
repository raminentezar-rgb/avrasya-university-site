# saglik_hizmetleri_myo/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from duyurular.models import Duyuru
from .models import SaglikHizmetleriMYODuyuru, SaglikHizmetleriMYODosya

@receiver(post_save, sender=Duyuru)
def create_saglik_hizmetleri_myo_duyuru(sender, instance, created, **kwargs):
    if instance.fakulte == 'SHMYO' and instance.yayinda:
        try:
            saglik_hizmetleri_myo_duyuru, created = SaglikHizmetleriMYODuyuru.objects.get_or_create(
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
                saglik_hizmetleri_myo_duyuru.baslik = instance.baslik
                saglik_hizmetleri_myo_duyuru.icerik = instance.icerik
                saglik_hizmetleri_myo_duyuru.ozet = instance.ozet
                saglik_hizmetleri_myo_duyuru.yayin_tarihi = instance.yayin_tarihi
                saglik_hizmetleri_myo_duyuru.yayinda = instance.yayinda
                saglik_hizmetleri_myo_duyuru.save()
            
            copy_attached_files(instance, saglik_hizmetleri_myo_duyuru)
                
        except Exception as e:
            print(f"Hata oluştu: {e}")

def copy_attached_files(ana_duyuru, saglik_hizmetleri_duyuru):
    try:
        saglik_hizmetleri_duyuru.dosyalar.all().delete()
        
        for ana_dosya in ana_duyuru.dosyalar.all():
            SaglikHizmetleriMYODosya.objects.create(
                duyuru=saglik_hizmetleri_duyuru,
                dosya=ana_dosya.dosya,
                dosya_adi=ana_dosya.dosya_adi,
                tur=ana_dosya.tur,
                aciklama=ana_dosya.aciklama
            )
    except Exception as e:
        print(f"Dosya kopyalama hatası: {e}")

@receiver(post_save, sender=Duyuru)
def update_saglik_hizmetleri_myo_duyuru(sender, instance, **kwargs):
    if instance.fakulte == 'SHMYO' and hasattr(instance, 'saglik_hizmetleri_myo_duyuru'):
        try:
            saglik_hizmetleri_myo_duyuru = instance.saglik_hizmetleri_myo_duyuru
            saglik_hizmetleri_myo_duyuru.baslik = instance.baslik
            saglik_hizmetleri_myo_duyuru.icerik = instance.icerik
            saglik_hizmetleri_myo_duyuru.ozet = instance.ozet
            saglik_hizmetleri_myo_duyuru.yayin_tarihi = instance.yayin_tarihi
            saglik_hizmetleri_myo_duyuru.yayinda = instance.yayinda
            saglik_hizmetleri_myo_duyuru.save()
            
            copy_attached_files(instance, saglik_hizmetleri_myo_duyuru)
            
        except Exception as e:
            print(f"Güncelleme hatası: {e}")