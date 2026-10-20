from django.db import models
from django.urls import reverse
from PIL import Image
import os
import re
from django.utils.html import strip_tags

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Haber Başlığı")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="SEO URL")
    summary = models.TextField(blank=True, verbose_name="Özet")
    content = models.TextField(verbose_name="Haber İçeriği")
    published_at = models.DateTimeField(verbose_name="Yayın Tarihi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_published = models.BooleanField(default=False, verbose_name="Yayında")
    main_image = models.ImageField(
        max_length=500,
        upload_to='news/%Y/%m/%d/', 
        blank=True, 
        null=True, 
        verbose_name="Ana Görsel",
        help_text="Önerilen boyut: Genişlik maksimum 1200px"
    )

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Haber'
        verbose_name_plural = 'Haberler'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', args=[self.slug])

    def auto_generate_summaries(self):
        """
        Özet boş ise, içerikle birebir aynıysa veya eski hatalı kesik özet ise,
        içerikten otomatik ve anlamlı bir haber özeti üretir.
        """
        content_val = (
            getattr(self, 'content_tr', None) or 
            getattr(self, 'content', None) or 
            getattr(self, 'content_en', None) or 
            ''
        ).strip()
        
        title_val = (
            getattr(self, 'title_tr', None) or 
            getattr(self, 'title', None) or 
            ''
        ).strip()
        
        sum_val = (self.summary or '').strip()
        
        # Eğer içerik doluysa ve (özet boşsa VEYA içerikle birebir aynıysa VEYA eski hatalı '...' ile bitiyorsa)
        if content_val and (not sum_val or sum_val == content_val or sum_val.endswith('...')):
            generated = generate_news_summary(content_val, title=title_val)
            if generated:
                self.summary = generated

    @property
    def get_summary(self):
        """Özet varsa döner, yoksa veya içerikle aynıysa otomatik özet üretip döner."""
        sum_val = (self.summary or '').strip()
        content_val = (
            getattr(self, 'content_tr', None) or 
            getattr(self, 'content', None) or 
            ''
        ).strip()
        if sum_val and sum_val != content_val and not sum_val.endswith('...'):
            return sum_val
        if content_val:
            title_val = getattr(self, 'title_tr', None) or getattr(self, 'title', '')
            return generate_news_summary(content_val, title=title_val)
        return ""

    @property
    def get_ozet(self):
        """Etkinlikler ile tam uyumluluk sağlayan alias"""
        return self.get_summary

    def optimize_main_image(self):
        """Ana görseli optimize eder ve boyutlandırır."""
        if not self.main_image:
            return
        img_path = self.main_image.path
        if not os.path.exists(img_path):
            return
        try:
            img = Image.open(img_path)
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            max_width = 1200
            if img.width > max_width:
                ratio = max_width / img.width
                img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
            img.save(img_path, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            print(f"Haber görseli optimize edilirken hata: {e}")

    def save(self, *args, **kwargs):
        self.auto_generate_summaries()
        super().save(*args, **kwargs)
        self.optimize_main_image()

    @property
    def image(self):
        return self.main_image or self.images.first()


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images', verbose_name="Haber")
    image = models.ImageField(max_length=500, upload_to='news/images/%Y/%m/%d/', verbose_name="Görsel")
    caption = models.CharField(max_length=255, blank=True, verbose_name="Görsel Başlığı / Açıklaması")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Haber Görseli'
        verbose_name_plural = 'Haber Görselleri'

    def __str__(self):
        return f"Image for {self.news.title}"


class NewsAttachment(models.Model):
    NEWS_ATTACHMENT_TYPES = [
        ('pdf', 'PDF'),
        ('word', 'Word'),
        ('excel', 'Excel'),
        ('image', 'Görsel'),
        ('other', 'Diğer'),
    ]
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='attachments', verbose_name="Haber")
    file = models.FileField(max_length=500, upload_to='news/attachments/%Y/%m/%d/', verbose_name="Dosya")
    file_type = models.CharField(max_length=10, choices=NEWS_ATTACHMENT_TYPES, verbose_name="Dosya Türü")
    title = models.CharField(max_length=255, verbose_name="Dosya Başlığı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ek Dosya'
        verbose_name_plural = 'Ek Dosyalar'

    def __str__(self):
        return f"{self.title} - {self.news.title}"
    
    def get_file_icon(self):
        icons = {
            'pdf': 'fas fa-file-pdf',
            'word': 'fas fa-file-word',
            'excel': 'fas fa-file-excel',
            'image': 'fas fa-file-image',
            'other': 'fas fa-file',
        }
        return icons.get(self.file_type, 'fas fa-file')
    
    def get_file_size(self):
        try:
            size = self.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        except:
            return "0 B"


def generate_news_summary(text, title="", max_chars=360):
    """
    Haber içeriğinden otomatik, anlamlı, akıcı ve profesyonel bir haber özeti üretir.
    Metnin sadece ilk satırlarını kopyalamak yerine; giriş, gelişme ve sonuç paragraflarındaki
    ana fikirleri ve eylemleri sentezleyerek gerçek bir haber özeti (çekirdek metin) oluşturur.
    """
    if not text:
        return ""
    import re
    from django.utils.html import strip_tags

    clean = strip_tags(text).replace('&nbsp;', ' ')
    lines = [l.strip() for l in clean.splitlines() if l.strip()]
    if not lines:
        return ""

    meta_prefixes = (
        'tarih:', 'saat:', 'yer:', 'kaynak:', 'muhabir:', 'yazar:', 'eğitmen:', 'konuşmacı:',
        'egitmen:', 'konusmaci:', 'tarih :', 'saat :', 'yer :', 'date:', 'time:', 'source:',
        'author:', 'location:', 'venue:', 'speaker:', 'تاریخ:', 'ساعت:', 'مکان:', 'منبع:',
        'نویسنده:', 'خبرنگار:', 'datum:', 'zeit:', 'ort:', 'quelle:', 'дата:', 'время:', 'место:'
    )
    meta_emojis = ('📅', '🕒', '📍', '🗓️', '⏰', '📌', '📰', '📢', '🎯', '✨', '💚', '🔔', '🎤', '📸')

    title_norm = re.sub(r'[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]', '', title).lower().strip() if title else ''
    filtered_paras = []
    for l in lines:
        l_lower = l.lower()
        if any(l_lower.startswith(p) for p in meta_prefixes) or any(l.startswith(e) for e in meta_emojis):
            continue
        l_norm = re.sub(r'[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]', '', l).lower().strip()
        if title_norm and (l_norm == title_norm or (len(l_norm) < 60 and l_norm in title_norm)):
            continue
        if len(l) < 30 and not l.endswith(('.', '!', '?', ';', ':')) and not re.search(r'(dir|tir|dır|tır|cek|cak|miş|mış|yor|du|dü|dı|di)$', l.lower()):
            continue
        filtered_paras.append(l)

    if not filtered_paras:
        return clean[:max_chars].strip()

    # Paragrafları cümlelerine ayrıştır
    parsed_paras = []
    for p in filtered_paras:
        sents = [s.strip() for s in re.split(r'(?<=[.!?。؛])\s+', p) if len(s.strip()) > 15]
        if sents:
            parsed_paras.append(sents)

    if not parsed_paras:
        return filtered_paras[0][:max_chars].strip()

    lead_sents = parsed_paras[0]
    lead = lead_sents[0]

    # Giriş cümlesini bürokratik kalıplardan arındırarak sadeleştir (özet dili)
    condensed_lead = lead
    m_quote = re.search(r'[“"\'‘]([^”"\'’]+)[”"\'’]', lead)
    quote_title = m_quote.group(1) if m_quote else ""

    if len(lead) > 130 and quote_title:
        if "tarafından" in lead and any(v in lead for v in ("düzenlendi", "gerçekleştirildi", "yapıldı", "buluştu", "başladı", "gerçekleştirilmiştir")):
            organizer_match = re.search(r'(?:Üniversitemiz\s+)?([A-ZÇĞİÖŞÜa-zçğıöşü\s,]+?)\s+tarafından', lead)
            org = organizer_match.group(1).strip() if organizer_match else ""
            if org and len(org) < 80:
                condensed_lead = f"{org} tarafından düzenlenen “{quote_title}” etkinliğinde öğrenciler bir araya geldi."
            else:
                condensed_lead = f"Avrasya Üniversitesi'nde “{quote_title}” etkinliği gerçekleştirildi."

    # Gelişme / Detay cümlesi (yapılan faaliyetler, katılımcılar, atölyeler vb.)
    activity_sent = ""
    action_verbs = (
        'fırsatı buldu', 'katıldı', 'deneyimledi', 'keşfetti', 'paylaştı', 'bilgi aldı', 
        'dinledi', 'sağlayarak', 'sağladı', 'ele alındı', 'gerçekleştirdi', 'aktardı', 
        'konuştu', 'değerlendirdi', 'sundu', 'vurguladı', 'bir araya gelerek'
    )

    if len(parsed_paras) > 1:
        body_sents = []
        for p in (parsed_paras[1:-1] if len(parsed_paras) > 2 else [parsed_paras[1]]):
            body_sents.extend(p)
        for s in body_sents:
            if any(v in s.lower() for v in action_verbs):
                activity_sent = s
                break
        if not activity_sent and body_sents:
            activity_sent = body_sents[0]
    elif len(lead_sents) > 1:
        for s in lead_sents[1:]:
            if any(v in s.lower() for v in action_verbs):
                activity_sent = s
                break
        if not activity_sent:
            activity_sent = lead_sents[1]

    # Sonuç / Etki cümlesi (varsa ve karakter limiti yetiyorsa)
    outcome_sent = ""
    if len(parsed_paras) >= 3:
        last_sents = parsed_paras[-1]
        impact_verbs = ('katkı sağladı', 'güçlenmesine', 'hedefledi', 'amaçlandı', 'tamamlandı', 'sona erdi', 'vurgulandı', 'memnuniyetini belirtti')
        for s in last_sents:
            if any(v in s.lower() for v in impact_verbs) and s != activity_sent:
                outcome_sent = s
                break

    chosen = [condensed_lead]
    current_len = len(condensed_lead)

    if activity_sent and activity_sent != condensed_lead:
        chosen.append(activity_sent)
        current_len += len(activity_sent)

    if outcome_sent and outcome_sent not in chosen and current_len + len(outcome_sent) <= max_chars + 60:
        chosen.append(outcome_sent)

    summary = ' '.join(chosen)
    if len(summary) > max_chars + 80:
        summary = summary[:max_chars].rsplit(' ', 1)[0]
        if not summary.endswith(('.', '!', '?')):
            summary += '...'
    return summary