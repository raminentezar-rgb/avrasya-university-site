from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ResearchPolicy(models.Model):
    title = models.CharField(max_length=300, verbose_name="Başlık")
    content = models.TextField(verbose_name="İçerik")
    commission = models.CharField(max_length=400, verbose_name="Komisyon")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Araştırma Politikası"
        verbose_name_plural = "Araştırma Politikaları"
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

class BAPProject(models.Model):
    title = models.CharField(max_length=400, verbose_name="Proje Başlığı")
    coordinator = models.CharField(max_length=200, verbose_name="Koordinatör")
    description = models.TextField(verbose_name="Açıklama")
    budget = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Bütçe")
    status = models.CharField(max_length=20, choices=(
        ('ongoing', 'Devam Ediyor'),
        ('completed', 'Tamamlandı'),
    ))
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "BAP Projesi"
        verbose_name_plural = "BAP Projeleri"

    def __str__(self):
        return self.title

class Laboratory(models.Model):
    name = models.CharField(max_length=300, verbose_name="Laboratuvar Adı")
    faculty = models.CharField(max_length=150, verbose_name="Fakülte/Bölüm")
    director = models.CharField(max_length=200, verbose_name="Sorumlu Öğretim Üyesi")
    equipment = models.TextField(verbose_name="Ekipmanlar")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Laboratuvar"
        verbose_name_plural = "Laboratuvarlar"

    def __str__(self):
        return self.name
    



# مدل جدید برای Araştırma Merkezleri
class ResearchCenter(models.Model):
    name = models.CharField(max_length=300, verbose_name="Merkez Adı")
    director = models.CharField(max_length=200, verbose_name="Müdür")
    faculty = models.CharField(max_length=150, verbose_name="Bağlı Fakülte")
    description = models.TextField(verbose_name="Açıklama")
    research_areas = models.TextField(verbose_name="Araştırma Alanları")
    status = models.CharField(max_length=20, choices=(
        ('active', 'Aktif'),
        ('planning', 'Planlama Aşamasında'),
        ('inactive', 'Pasif'),
    ), default='active')
    established_date = models.DateField(verbose_name="Kuruluş Tarihi", null=True, blank=True)
    researcher_count = models.PositiveIntegerField(verbose_name="Araştırmacı Sayısı", default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Araştırma Merkezi"
        verbose_name_plural = "Araştırma Merkezleri"
        ordering = ['name']

    def __str__(self):
        return self.name

# مدل جدید برای Fikri ve Sınai Mülkiyet
class IntellectualProperty(models.Model):
    PROPERTY_TYPES = (
        ('patent', 'Patent'),
        ('utility_model', 'Faydalı Model'),
        ('trademark', 'Ticari Marka'),
        ('copyright', 'Telif Hakkı'),
        ('industrial_design', 'Endüstriyel Tasarım'),
    )
    
    STATUS_CHOICES = (
        ('approved', 'Onaylı'),
        ('application', 'Başvuru Sürecinde'),
        ('rejected', 'Reddedildi'),
        ('expired', 'Süresi Dolmuş'),
    )

    title = models.CharField(max_length=400, verbose_name="Başlık")
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, verbose_name="Mülkiyet Türü")
    registration_number = models.CharField(max_length=100, verbose_name="Tescil Numarası", blank=True)
    inventor = models.CharField(max_length=200, verbose_name="Mucit/Sahip")
    faculty = models.CharField(max_length=150, verbose_name="Fakülte/Bölüm")
    description = models.TextField(verbose_name="Açıklama")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Durum")
    application_date = models.DateField(verbose_name="Başvuru Tarihi", null=True, blank=True)
    registration_date = models.DateField(verbose_name="Tescil Tarihi", null=True, blank=True)
    expiration_date = models.DateField(verbose_name="Son Geçerlilik Tarihi", null=True, blank=True)
    is_international = models.BooleanField(default=False, verbose_name="Uluslararası")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fikri Mülkiyet"
        verbose_name_plural = "Fikri Mülkiyetler"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_property_type_display()}"

# مدل جدید برای Araştırma Çıktıları
class ResearchOutput(models.Model):
    OUTPUT_TYPES = (
        ('sci_article', 'SCI Makale'),
        ('international_article', 'Uluslararası Makale'),
        ('national_article', 'Ulusal Makale'),
        ('book', 'Kitap'),
        ('book_chapter', 'Kitap Bölümü'),
        ('conference_paper', 'Konferans Bildirisi'),
        ('report', 'Rapor'),
    )

    title = models.CharField(max_length=500, verbose_name="Başlık")
    output_type = models.CharField(max_length=50, choices=OUTPUT_TYPES, verbose_name="Çıktı Türü")
    authors = models.TextField(verbose_name="Yazarlar")
    journal = models.CharField(max_length=300, verbose_name="Dergi/Kitap", blank=True)
    publisher = models.CharField(max_length=200, verbose_name="Yayınevi", blank=True)
    publication_date = models.DateField(verbose_name="Yayın Tarihi")
    volume = models.CharField(max_length=50, verbose_name="Cilt", blank=True)
    issue = models.CharField(max_length=50, verbose_name="Sayı", blank=True)
    pages = models.CharField(max_length=50, verbose_name="Sayfalar", blank=True)
    doi = models.CharField(max_length=100, verbose_name="DOI", blank=True)
    issn_isbn = models.CharField(max_length=50, verbose_name="ISSN/ISBN", blank=True)
    abstract = models.TextField(verbose_name="Özet", blank=True)
    citation_count = models.PositiveIntegerField(verbose_name="Atıf Sayısı", default=0)
    impact_factor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Etki Faktörü", null=True, blank=True)
    quartile = models.CharField(max_length=2, choices=(
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),
    ), blank=True, verbose_name="Kuartil")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Araştırma Çıktısı"
        verbose_name_plural = "Araştırma Çıktıları"
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

# مدل جدید برای Ödüller
class Award(models.Model):
    AWARD_TYPES = (
        ('international', 'Uluslararası Ödül'),
        ('national', 'Ulusal Ödül'),
        ('tubitak', 'TÜBİTAK Ödülü'),
        ('patent', 'Patent Ödülü'),
        ('young_researcher', 'Genç Araştırmacı Ödülü'),
        ('industry', 'Sanayi İşbirliği Ödülü'),
        ('conference', 'Konferans Ödülü'),
    )

    title = models.CharField(max_length=400, verbose_name="Ödül Adı")
    award_type = models.CharField(max_length=50, choices=AWARD_TYPES, verbose_name="Ödül Türü")
    recipient = models.CharField(max_length=200, verbose_name="Ödül Alan")
    faculty = models.CharField(max_length=150, verbose_name="Fakülte/Bölüm")
    awarding_organization = models.CharField(max_length=300, verbose_name="Veren Kuruluş")
    category = models.CharField(max_length=200, verbose_name="Kategori", blank=True)
    award_date = models.DateField(verbose_name="Ödül Tarihi")
    description = models.TextField(verbose_name="Açıklama")
    prize_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Ödül Miktarı", null=True, blank=True)
    project_title = models.CharField(max_length=400, verbose_name="Proje Başlığı", blank=True)
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ödül"
        verbose_name_plural = "Ödüller"
        ordering = ['-award_date']

    def __str__(self):
        return f"{self.title} - {self.recipient}"