from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to='news/%Y/%m/%d/', blank=True, null=True, verbose_name="تصویر اصلی")

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'خبر'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', args=[self.slug])


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news/images/%Y/%m/%d/', verbose_name="تصویر")
    caption = models.CharField(max_length=255, blank=True, verbose_name="عنوان تصویر")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'تصویر خبر'
        verbose_name_plural = 'News images'

    def __str__(self):
        return f"Image for {self.news.title}"


class NewsAttachment(models.Model):
    NEWS_ATTACHMENT_TYPES = [
        ('pdf', 'PDF'),
        ('word', 'Word'),
        ('excel', 'Excel'),
        ('image', 'Image'),
        ('other', 'Other'),
    ]
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='news/attachments/%Y/%m/%d/', verbose_name="فایل")
    file_type = models.CharField(max_length=10, choices=NEWS_ATTACHMENT_TYPES, verbose_name="نوع فایل")
    title = models.CharField(max_length=255, verbose_name="عنوان فایل")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'فایل پیوست'
        verbose_name_plural = 'Attached files'

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
        

    @property
    def image(self):
        return self.main_image or self.images.first()