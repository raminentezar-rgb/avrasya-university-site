from django.db import migrations, models

def create_initial_bolumler(apps, schema_editor):
    Bolum = apps.get_model('duyurular', 'Bolum')
    
    # رشته‌های نمونه - شما می‌توانید این لیست را بر اساس تصاویر ارسالی تکمیل کنید
    initial_bolumler = [
        {'ad': 'İngiliz Dili ve Edebiyatı', 'kod': 'ingiliz-dili-ve-edebiyati', 'fakulte': 'FEF'},
        {'ad': 'Psikoloji', 'kod': 'psikoloji', 'fakulte': 'FEF'},
        {'ad': 'Türk Dili ve Edebiyatı', 'kod': 'turk-dili-ve-edebiyati', 'fakulte': 'FEF'},
        # ... سایر رشته‌ها را اینجا اضافه کنید
    ]
    
    for bolum_data in initial_bolumler:
        Bolum.objects.create(**bolum_data)

class Migration(migrations.Migration):

    dependencies = [
        ('duyurular', '0002_duyurudosya_remove_duyuru_excel_dosyasi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bolum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=255, verbose_name='Bölüm Adı')),
                ('kod', models.SlugField(unique=True, verbose_name='Bölüm Kodu')),
                ('fakulte', models.CharField(choices=[('LEE', 'LEE'), ('FEF', 'FEF'), ('IIBF', 'IIBF'), ('MMF', 'MMF'), ('SBF', 'SBF'), ('ILTF', 'ILTF'), ('SPOR', 'SPOR'), ('UBY', 'UBY'), ('MYO', 'MYO'), ('SHMYO', 'SHMYO'), ('GENEL', 'Genel Duyuru')], max_length=10, verbose_name='Bağlı Fakülte')),
                ('aciklama', models.TextField(blank=True, verbose_name='Açıklama')),
                ('aktif', models.BooleanField(default=True, verbose_name='Aktif')),
            ],
            options={
                'verbose_name': 'Bölüm',
                'verbose_name_plural': 'Bölümler',
                'ordering': ['fakulte', 'ad'],
            },
        ),
        migrations.AddField(
            model_name='duyuru',
            name='bolumler',
            field=models.ManyToManyField(blank=True, help_text='Bu duyurunun gösterileceği bölümleri seçin', to='duyurular.bolum', verbose_name='İlgili Bölümler'),
        ),
        migrations.RunPython(create_initial_bolumler),
    ]