from django.shortcuts import render


def kutuphane(request):
    return render(request,'kutuphane/includes/anasayfa.html')

def genel_bilgiler(request):
    return render(request, 'kutuphane/includes/genel_bilgiler.html')


def acik_erisim(request):
    return render(request, 'kutuphane/includes/acik_erisim.html')

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect

def calisma_takvimi(request):
    if request.method == 'POST':
        ad_soyad = request.POST.get('adSoyad')
        email = request.POST.get('email')
        talep = request.POST.get('talep')
        talep_gunu = request.POST.get('talepGunu')

        subject = f"Kütüphane Çalışma Takvimi Talebi: {ad_soyad}"
        message = (
            f"Yeni bir kütüphane çalışma saati talebi alındı:\n\n"
            f"Ad Soyad: {ad_soyad}\n"
            f"E-posta: {email}\n"
            f"Talep Günü: {talep_gunu}\n"
            f"Talep/Mesaj:\n{talep}\n"
        )

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['kutuphane@avrasya.edu.tr'],
                fail_silently=False,
            )
            messages.success(request, 'Talebiniz başarıyla gönderildi. Teşekkür ederiz.')
        except Exception as e:
            messages.error(request, 'Talebiniz gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyiniz.')
            
        return redirect('kutuphane:calisma_takvimi')
        
    return render(request, 'kutuphane/includes/calisma_takvimi.html')
def hizli_baglantilar(request):
    return render(request, 'kutuphane/includes/hizli_baglantilar.html')


def iletisim(request):
    return render(request, 'kutuphane/includes/iletisim.html')

