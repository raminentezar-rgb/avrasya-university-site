from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
import sys

class Etkinlik(models.Model):
    ETKINLIK_TURU_CHOICES = [
        ('konferans', 'Konferans / Kongre / Sempozyum'),
        ('seminer', 'Seminer / Panel'),
        ('kultur', 'Kültür-Sanat Etkinliği'),
        ('spor', 'Spor Etkinliği'),
        ('tanitim', 'Tanıtım Günleri'),
        ('workshop', 'Workshop / Atölye'),
        ('diger', 'Diğer'),
    ]
    
    baslik = models.CharField(max_length=255, verbose_name="Etkinlik Başlığı")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="SEO URL")
    kisa_aciklama = models.TextField(blank=True, verbose_name="Kısa Açıklama")
    detayli_aciklama = models.TextField(verbose_name="Detaylı Açıklama")
    etkinlik_turu = models.CharField(
        max_length=50, 
        choices=ETKINLIK_TURU_CHOICES, 
        default='diger',
        verbose_name="Etkinlik Türü"
    )
    
    baslangic_tarihi = models.DateTimeField(verbose_name="Başlangıç Tarihi")
    bitis_tarihi = models.DateTimeField(verbose_name="Bitiş Tarihi", blank=True, null=True)
    yer = models.CharField(max_length=255, verbose_name="Etkinlik Yeri")
    
    afis = models.ImageField(
        max_length=500,
        upload_to='etkinlikler/afis/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Etkinlik Afişi",
        help_text="Önerilen boyut: Genişlik maksimum 1200px, yükseklik serbest. Posterin tamamı görünecektir."
    )
    
    katilim_linki = models.URLField(max_length=500, blank=True, verbose_name="Katılım Linki")
    kayit_gerekiyor = models.BooleanField(default=False, verbose_name="Kayıt Gerekiyor")
    ucretli = models.BooleanField(default=False, verbose_name="Ücretli Etkinlik")
    
    yayinda = models.BooleanField(default=False, verbose_name="Yayında")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['baslangic_tarihi']
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse('etkinlikler:detay', args=[self.slug])

    def yaklasan_etkinlik(self):
        """Etkinliğin yaklaşıp yaklaşmadığını kontrol eder"""
        return self.baslangic_tarihi <= timezone.now() + timezone.timedelta(days=7)

    def devam_ediyor(self):
        """Etkinliğin devam edip etmediğini kontrol eder"""
        now = timezone.now()
        if self.bitis_tarihi:
            return self.baslangic_tarihi <= now <= self.bitis_tarihi
        return self.baslangic_tarihi.date() == now.date()

    def gun_kaldi(self):
        """Etkinliğe kaç gün kaldığını hesaplar"""
        kalan_gun = (self.baslangic_tarihi.date() - timezone.now().date()).days
        return max(0, kalan_gun)

    def optimize_afis(self):
        """Afiş görselini optimize eder - boyutlandırır ve sıkıştırır"""
        if not self.afis:
            return
        
        # Dosya yolunu al
        img_path = self.afis.path
        
        # Dosya mevcut mu kontrol et
        if not os.path.exists(img_path):
            return
        
        try:
            # Görseli aç
            img = Image.open(img_path)
            
            # RGB formatına çevir (şeffaflık sorunları için)
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Maksimum genişlik 1200px, yükseklik otomatik orantılı
            max_width = 1200
            if img.width > max_width:
                oran = max_width / img.width
                yeni_yukseklik = int(img.height * oran)
                img = img.resize((max_width, yeni_yukseklik), Image.LANCZOS)
            
            # Görseli kaydet (kalite: 85, optimize et)
            img.save(img_path, 'JPEG', quality=85, optimize=True)
            
        except Exception as e:
            # Hata durumunda logla ama kaydetmeyi engelleme
            print(f"Afiş optimize edilirken hata: {e}")

    def auto_generate_summaries(self):
        """
        Kısa Açıklama boş bırakıldığında veya Detaylı Açıklama ile birebir aynı yapıştırıldığında,
        Detaylı Açıklamadan otomatik olarak anlamlı ve profesyonel bir etkinlik özeti üretir.
        Modeltranslation'ın tüm dillerini (tr, en, fa, ar, ru, de) ve ana alanı destekler.
        """
        for lang in ['', '_tr', '_en', '_fa', '_ar', '_ru', '_de']:
            kisa_attr = f'kisa_aciklama{lang}'
            detay_attr = f'detayli_aciklama{lang}'
            
            if hasattr(self, kisa_attr) and hasattr(self, detay_attr):
                kisa_val = getattr(self, kisa_attr, None) or ''
                detay_val = getattr(self, detay_attr, None) or ''
                
                kisa_strip = kisa_val.strip()
                detay_strip = detay_val.strip()
                
                # Eğer detay dolu ama kısa açıklama boşsa VEYA ikisi de aynıysa (kullanıcı tüm metni kopyaladıysa)
                if detay_strip and (not kisa_strip or kisa_strip == detay_strip):
                    baslik_attr = f'baslik{lang}'
                    title_val = getattr(self, baslik_attr, '') or self.baslik or ''
                    summary = generate_event_summary(detay_strip, title=title_val)
                    if summary:
                        setattr(self, kisa_attr, summary)

    @property
    def get_ozet(self):
        """Kısa açıklama varsa döner, yoksa veya detayla aynıysa otomatik özet üretip döner."""
        kisa = (self.kisa_aciklama or '').strip()
        detay = (self.detayli_aciklama or '').strip()
        if kisa and kisa != detay:
            return kisa
        if detay:
            return generate_event_summary(detay, title=self.baslik)
        return ""

    def save(self, *args, **kwargs):
        """Kaydetme işlemi - özeti otomatik oluştur ve afişi optimize et"""
        # Detaylı açıklamadan otomatik özet üret
        self.auto_generate_summaries()
        
        # Normal kaydet
        super().save(*args, **kwargs)
        
        # Kaydettikten sonra afişi optimize et
        self.optimize_afis()


def generate_event_summary(text, title='', max_chars=350):
    """
    Detaylı metinden otomatik, anlamlı ve temiz bir etkinlik özeti üretir.
    Gereksiz satırları, tarih/saat/yer tekrarlarını ve emojileri filtreler;
    etkinliğin ana konusunu ve amacını anlatan ilk 1-3 cümleyi seçer.
    """
    if not text:
        return ""
        
    import re
    from django.utils.html import strip_tags
    
    clean_text = strip_tags(text).replace('&nbsp;', ' ')
    
    meta_prefixes = (
        'tarih:', 'saat:', 'yer:', 'eğitmen:', 'konuşmacı:', 'egitmen:', 'konusmaci:',
        'tarih :', 'saat :', 'yer :', 'date:', 'time:', 'location:', 'venue:', 'speaker:',
        'تاریخ:', 'ساعت:', 'مکان:', 'مدرس:', 'برگزارکننده:', 'datum:', 'zeit:', 'ort:',
        'дата:', 'время:', 'место:'
    )
    meta_emojis = ('📅', '🕒', '📍', '🗓️', '⏰', '📌', '👨‍🏫', '👩‍🏫', '🎯', '✨', '💚', '🔔', '📢')
    
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    cleaned_sentences = []
    
    title_norm = re.sub(r'[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]', '', title).lower().strip() if title else ''
    
    for l in lines:
        l_lower = l.lower()
        if any(l_lower.startswith(p) for p in meta_prefixes):
            continue
        if any(l.startswith(e) for e in meta_emojis):
            continue
            
        l_norm = re.sub(r'[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]', '', l).lower().strip()
        # Başlıkla aynı veya çok kısa başlıksı satırları atla
        if title_norm and (l_norm == title_norm or (len(l_norm) < 60 and l_norm in title_norm)):
            continue
        if len(l) < 55 and not l.endswith(('.', '!', '?', ';', ':')) and not re.search(r'(dir|tir|dır|tır|cek|cak|miş|mış|yor|du|dü|dı|di)$', l.lower()):
            continue
            
        if not l.endswith(('.', '!', '?', ';')):
            l += '.'
        cleaned_sentences.append(l)
        
    combined = ' '.join(cleaned_sentences)
    combined = re.sub(r'\s+', ' ', combined).strip()
    if not combined:
        return clean_text[:max_chars].strip()
        
    sentences = re.split(r'(?<=[.!?。؛])\s+', combined)
    selected = []
    curr_len = 0
    
    for s in sentences:
        s_clean = s.strip()
        if not s_clean or len(s_clean) < 15:
            continue
        selected.append(s_clean)
        curr_len += len(s_clean)
        if curr_len >= 200 or len(selected) >= 2:
            if curr_len >= 180:
                break
                
    if not selected:
        return combined[:max_chars].strip()
        
    summary = ' '.join(selected)
    if len(summary) > max_chars + 80:
        summary = summary[:max_chars].rsplit(' ', 1)[0]
        if not summary.endswith(('.', '!', '?')):
            summary += '...'
    return summary