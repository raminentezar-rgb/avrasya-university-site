from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse

# Configure these emails or move them to settings.py
ACCOUNTING_EMAIL = "muhasebe@avrasya.edu.tr" 
STUDENT_AFFAIRS_EMAIL = "ogrenci@avrasya.edu.tr"

def submit_payment_form(request):
    if request.method == 'POST':
        try:
            # Extract form data
            name = request.POST.get('your-name')
            tc = request.POST.get('number-tc')
            email = request.POST.get('your-email')
            phone = request.POST.get('tel-gsm')
            program = request.POST.get('bolum')
            bank_name = request.POST.get('bankaname')
            card_number = request.POST.get('kartno') # Note: storing/mailing full card numbers is risky/non-compliant usually, but following instructions to just email it.
            # Masking card number for security in email usually recommended, but user asked to send info.
            # I will send it as is per request, but add a comment/warning if I were consulting. 
            # Since I am "Antigravity", I will just implement the backend.
            card_expiry = request.POST.get('kartdate')
            cvc = request.POST.get('kartcvc')
            payment_option = request.POST.get('odemeyontemi')
            
            # Construct email body
            body = f"""
            Yeni Online Ödeme Formu Gönderildi.
            
            Kişisel Bilgiler:
            -----------------
            Ad Soyad: {name}
            TC Kimlik No: {tc}
            E-posta: {email}
            Telefon: {phone}
            Bölüm: {program}
            
            Ödeme Bilgileri:
            ----------------
            Banka Adı: {bank_name}
            Kart Numarası: {card_number}
            Son Kullanma Tarihi: {card_expiry}
            CVC: {cvc}
            Ödeme Yöntemi: {payment_option}
            
            Proforma Bilgileri (Varsa):
            ---------------------------
            Ad Soyad: {request.POST.get('proad', '-')}
            TC No: {request.POST.get('protc', '-')}
            """
            
            email_msg = EmailMessage(
                subject=f'Online Ödeme Formu - {name}',
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@avrasya.edu.tr',
                to=[ACCOUNTING_EMAIL, 'muhasebe@avrasya.edu.tr'], # Added for testing
                reply_to=[email]
            )
            
            # Attach files
            if 'dekont' in request.FILES:
                email_msg.attach(request.FILES['dekont'].name, request.FILES['dekont'].read(), request.FILES['dekont'].content_type)
            if 'yks' in request.FILES:
                email_msg.attach(request.FILES['yks'].name, request.FILES['yks'].read(), request.FILES['yks'].content_type)
                
            print(f"Sending payment email to {email_msg.to}...")
            email_msg.send()
            print("Payment email sent successfully.")
            messages.success(request, 'Ödeme formunuz başarıyla gönderildi.')
            return redirect('ogrenci_isleri:formlar')
            
        except Exception as e:
            print(f"ERROR Sending Payment Email: {e}")
            messages.error(request, f'Bir hata oluştu: {str(e)}')
            return redirect('ogrenci_isleri:formlar')
            
    return redirect('ogrenci_isleri:formlar')

def submit_registration_form(request):
    if request.method == 'POST':
        try:
            # Extract form data
            name = request.POST.get('your-name')
            tc = request.POST.get('number-tc')
            email = request.POST.get('your-email')
            phone = request.POST.get('tel-gsm')
            program = request.POST.get('your-bolum')
            
            # Construct email body
            body = f"""
            Yeni Online Kayıt Formu Gönderildi.
            
            Öğrenci Bilgileri:
            ------------------
            Ad Soyad: {name}
            TC Kimlik No: {tc}
            E-posta: {email}
            Telefon: {phone}
            Kazandığı Bölüm: {program}
            """
            
            email_msg = EmailMessage(
                subject=f'Online Kayıt Formu - {name}',
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@avrasya.edu.tr',
                to=[STUDENT_AFFAIRS_EMAIL, 'ogrenciisleri@avrasya.edu.tr'], # Added for testing
                reply_to=[email]
            )
            
            # Attach files
            files_to_attach = ['diploma', 'kimlik', 'yks', 'sivil', 'dekont']
            for file_key in files_to_attach:
                if file_key in request.FILES:
                    f = request.FILES[file_key]
                    email_msg.attach(f.name, f.read(), f.content_type)
            
            email_msg.send()
            messages.success(request, 'Kayıt formunuz başarıyla gönderildi.')
            return redirect('ogrenci_isleri:formlar')
            
        except Exception as e:
            messages.error(request, f'Bir hata oluştu: {str(e)}')
            return redirect('ogrenci_isleri:formlar')
            
    return redirect('ogrenci_isleri:formlar')






def ogrenci_isleri(request):
    return render(request,'ogrenci_isleri/includes/ogrenci_isleri.html')


def daire_baskanligi(request):
    return render(request,'ogrenci_isleri/includes/daire_baskanligi.html')


def ogrenim_ucretleri(request):
    return render(request,'ogrenci_isleri/includes/ogrenim_ucretleri.html')


def kayit(request):
    return render(request,'ogrenci_isleri/includes/kayit.html')


def burslar(request):
    return render(request,'ogrenci_isleri/includes/burslar.html')

def yurtlar(request):
    return render(request,'ogrenci_isleri/includes/yurtlar.html')

def muafiyetler(request):
    return render(request,'ogrenci_isleri/includes/muafiyetler.html')

def kulupler(request):
    return render(request,'ogrenci_isleri/includes/kulupler.html')

def yonetmelik(request):
    return render(request,'ogrenci_isleri/includes/yonetmelik.html')

def formlar(request):
    return render(request,'ogrenci_isleri/includes/formlar.html')

def dikey(request):
    return render(request,'ogrenci_isleri/includes/dikey.html')

def erasmus(request):
    return render(request,'ogrenci_isleri/includes/erasmus.html')


