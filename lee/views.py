from django.shortcuts import render, get_object_or_404, redirect
from .models import LeeDuyuru, Lee_Etkinlik
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings

# Email Constants
LEE_STUDENT_AFFAIRS_EMAIL = 'ogrenciisleri@avrasya.edu.tr'
LEE_INTERNATIONAL_EMAIL = 'iso@avrasya.edu.tr' # Default for International Office

def submit_online_application(request):
    if request.method == 'POST':
        try:
            # Extract form data
            name = request.POST.get('your-name')
            phone = request.POST.get('tel-gsm')
            email = request.POST.get('your-email')

            # Construct email body
            body = f"""
            Yeni Lisansüstü Ön Başvuru (Online - Türk Öğrenci)
            
            Kişisel Bilgiler:
            -----------------
            Ad Soyad: {name}
            Telefon: {phone}
            E-posta: {email}
            
            Kabul Edilen Şartlar:
            ---------------------
            KVKK Onayı: {'Evet' if request.POST.get('acceptance-985') else 'Hayır'}
            Belge Doğruluk Beyanı: {'Evet' if request.POST.get('acceptance-documents') else 'Hayır'}
            """
            
            email_msg = EmailMessage(
                subject=f'Lisansüstü Ön Başvuru - {name}',
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@avrasya.edu.tr',
                to=[LEE_STUDENT_AFFAIRS_EMAIL, 'lisansustusekreterligi@avrasya.edu.tr'], # Backup/Test
                reply_to=[email]
            )
            
            # Attach files
            files_to_attach = ['kimlik', 'basvuru', 'diploma', 'ales', 'transkript', 'yds', 'foto', 'dekont']
            for file_key in files_to_attach:
                if file_key in request.FILES:
                    f = request.FILES[file_key]
                    email_msg.attach(f.name, f.read(), f.content_type)
            
            email_msg.send()
            messages.success(request, 'Başvurunuz başarıyla gönderildi.')
            return redirect('lee:on_basvuru_formu')
            
        except Exception as e:
            messages.error(request, f'Bir hata oluştu: {str(e)}')
            return redirect('lee:on_basvuru_formu')
            
    return redirect('lee:on_basvuru_formu')

def submit_international_application(request):
    if request.method == 'POST':
        try:
            # Extract form data
            name = request.POST.get('your-name')
            passport = request.POST.get('passport-number')
            phone = request.POST.get('tel-gsm')
            email = request.POST.get('your-email')
            country = request.POST.get('country')

            # Construct email body
            body = f"""
            New International Student Application (Lisansüstü Yabancı Öğrenci Başvurusu)
            
            Personal Information:
            ---------------------
            Full Name: {name}
            Passport Number: {passport}
            Phone: {phone}
            Email: {email}
            Country: {country}
            
            Agreements:
            -----------
            KVKK Approval: {'Yes' if request.POST.get('acceptance-985') else 'No'}
            Document Truthfulness: {'Yes' if request.POST.get('acceptance-documents') else 'No'}
            Visa Commitment: {'Yes' if request.POST.get('acceptance-visa') else 'No'}
            """
            
            email_msg = EmailMessage(
                subject=f'International Student Application - {name}',
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@avrasya.edu.tr',
                to=[LEE_INTERNATIONAL_EMAIL, 'lisansustusekreterligi@avrasya.edu.tr'],
                reply_to=[email]
            )
            
            # Attach files
            # Note: Input names in HTML might differ, checking...
            # HTML uses: kimlik (Passport), basvuru, diploma, ales, transkript, yds, foto, dekont
            files_to_attach = ['kimlik', 'basvuru', 'diploma', 'ales', 'transkript', 'yds', 'foto', 'dekont']
            for file_key in files_to_attach:
                if file_key in request.FILES:
                    f = request.FILES[file_key]
                    email_msg.attach(f.name, f.read(), f.content_type)
            
            email_msg.send()
            messages.success(request, 'Application submitted successfully. (Başvurunuz başarıyla gönderildi.)')
            return redirect('lee:on_basvuru_formu')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('lee:on_basvuru_formu')
            
    return redirect('lee:on_basvuru_formu')

def etkinlik_listesi(request):
    now = timezone.now()
    
    # رویدادهای آینده (از حالا به بعد)
    gelecek_etkinlikler = Lee_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # رویدادهای گذشته (قبل از حالا)
    gecmis_etkinlikler = Lee_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__lt=now
    ).order_by('-baslangic_tarihi')
    
    # برای دیباگ - چاپ تعداد رویدادها
    print(f"Gelecek etkinlikler: {gelecek_etkinlikler.count()}")
    print(f"Geçmiş etkinlikler: {gecmis_etkinlikler.count()}")
    
    context = {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_etkinlikler,
    }
    
    return render(request, 'lee/includes/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(Lee_Etkinlik, slug=slug, yayinda=True)
    return render(request, 'lee/includes/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = Lee_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'lee/includes/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })




def duyurular(request):
    """نمایش تمام اطلاعیه‌های دانشکده LEE"""
    duyurular = LeeDuyuru.objects.filter(yayinda=True)
    
    # فیلتر بر اساس دسته‌بندی
    kategori = request.GET.get('kategori', '')
    if kategori:
        duyurular = duyurular.filter(kategori=kategori)
    
    # اطلاعیه‌های مهم
    onemli_duyurular = duyurular.filter(onemli=True)
    
    context = {
        'duyurular': duyurular,
        'onemli_duyurular': onemli_duyurular,
        'kategori': kategori,
    }
    return render(request, 'lee/includes/duyurular.html', context)

def duyuru_detay(request, id):
    """نمایش جزئیات یک اطلاعیه LEE"""
    duyuru = get_object_or_404(LeeDuyuru, id=id, yayinda=True)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = LeeDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'lee/includes/duyuru_detay.html', context)





# سایر viewهای موجود...
def lee(request):
    return render(request, 'lee/lee.html')

# سایر viewهای موجود...
def lee(request):
    return render(request, 'lee/includes/lee.html')

def tarihce(request):
    return render(request, 'lee/includes/tarihce.html')

def on_basvuru_formu(request):
    return render(request, 'lee/includes/on_basvuru_formu.html')

def tezli_yukseklisans_programlari(request):
    return render(request, 'lee/includes/tezli_yukseklisans_programlari.html')

def akademik_takvim(request):
    return render(request, 'lee/includes/akademik_takvim.html')

def doktora_programları(request):
    return render(request, 'lee/includes/doktora_programları.html')

def akademik_kadro(request):
    return render(request, 'lee/includes/akademik_kadro.html')

def mevzuat_formlar(request):
    return render(request, 'lee/includes/mevzuat_formlar.html')

def kalite(request):
    return render(request, 'lee/includes/kalite.html')

def iletisim(request):
    return render(request, 'lee/includes/iletisim.html')

def tezsiz_yukseklisans_programlari(request):
    return render(request, 'lee/includes/tezsiz_yukseklisans_programlari.html')
