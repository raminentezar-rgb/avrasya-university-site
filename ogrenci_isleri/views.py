import logging
import os
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from support.services.uploads import validate_attachment

logger = logging.getLogger(__name__)

# Configure these emails or move them to settings.py
ACCOUNTING_EMAIL = "muhasebe@avrasya.edu.tr"
STUDENT_AFFAIRS_EMAIL = "ogrenci@avrasya.edu.tr"


def _safe_header(val):
    return str(val or '').replace('\r', '').replace('\n', '').strip()


def _valid_reply_to(email_raw):
    cleaned = _safe_header(email_raw)
    if not cleaned:
        return []
    try:
        validate_email(cleaned)
        return [cleaned]
    except ValidationError:
        return []


def submit_payment_form(request):
    if request.method == 'POST':
        try:
            name = _safe_header(request.POST.get('your-name'))[:120]
            tc = _safe_header(request.POST.get('number-tc'))[:32]
            email = _safe_header(request.POST.get('your-email'))
            phone = _safe_header(request.POST.get('tel-gsm'))[:30]
            program = _safe_header(request.POST.get('bolum'))[:150]
            bank_name = _safe_header(request.POST.get('bankaname'))[:120]
            referans_no = _safe_header(request.POST.get('referans_no'))[:80]
            payment_option = _safe_header(request.POST.get('odemeyontemi'))[:200]

            # Never read, store, log, or email raw card PAN / expiry / CVC fields (PCI-DSS compliance).
            if not name or not tc or not email:
                messages.error(request, 'Lütfen ad soyad, kimlik numarası ve geçerli e-posta bilgilerini giriniz.')
                return redirect('ogrenci_isleri:formlar')

            reply_to = _valid_reply_to(email)
            if not reply_to:
                messages.error(request, 'Lütfen geçerli bir e-posta adresi giriniz.')
                return redirect('ogrenci_isleri:formlar')

            for field_name in ('dekont', 'yks'):
                up = request.FILES.get(field_name)
                if up:
                    ok, err = validate_attachment(up)
                    if not ok:
                        messages.error(request, err)
                        return redirect('ogrenci_isleri:formlar')

            body = f"""
            Yeni Online Ödeme Bildirim Formu Gönderildi.

            Kişisel Bilgiler:
            -----------------
            Ad Soyad: {name}
            TC Kimlik No: {tc}
            E-posta: {email}
            Telefon: {phone}
            Bölüm: {program}

            Ödeme ve Referans Bilgileri:
            ----------------------------
            Banka / Kurum Adı: {bank_name}
            Dekont / Referans No: {referans_no or '-'}
            Ödeme Yöntemi: {payment_option}
            Not: Kredi kartı numarası ve CVC bilgisi güvenlik politikası gereği form/e-posta ile alınmamaktadır.

            Proforma Bilgileri (Varsa):
            ---------------------------
            Ad Soyad: {_safe_header(request.POST.get('proad', '-'))[:120]}
            TC No: {_safe_header(request.POST.get('protc', '-'))[:32]}
            """

            email_msg = EmailMessage(
                subject=f'Online Ödeme Bildirimi - {name}',
                body=body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@avrasya.edu.tr'),
                to=[ACCOUNTING_EMAIL],
                reply_to=reply_to,
            )

            for field_name in ('dekont', 'yks'):
                up = request.FILES.get(field_name)
                if up:
                    email_msg.attach(os.path.basename(up.name), up.read(), up.content_type or 'application/octet-stream')

            email_msg.send()
            messages.success(request, 'Ödeme bildirim formunuz başarıyla gönderildi.')
            return redirect('ogrenci_isleri:formlar')

        except Exception:
            logger.exception('Payment notification form submission failed')
            messages.error(request, 'Form gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyiniz.')
            return redirect('ogrenci_isleri:formlar')

    return redirect('ogrenci_isleri:formlar')


def submit_registration_form(request):
    if request.method == 'POST':
        try:
            name = _safe_header(request.POST.get('your-name'))[:120]
            tc = _safe_header(request.POST.get('number-tc'))[:32]
            email = _safe_header(request.POST.get('your-email'))
            phone = _safe_header(request.POST.get('tel-gsm'))[:30]
            program = _safe_header(request.POST.get('your-bolum'))[:150]

            reply_to = _valid_reply_to(email)
            if not name or not tc or not reply_to:
                messages.error(request, 'Lütfen ad soyad, kimlik ve geçerli bir e-posta adresi giriniz.')
                return redirect('ogrenci_isleri:formlar')

            files_to_attach = ['diploma', 'kimlik', 'yks', 'sivil', 'dekont']
            validated_files = []
            for file_key in files_to_attach:
                if file_key in request.FILES:
                    f = request.FILES[file_key]
                    ok, err = validate_attachment(f)
                    if not ok:
                        messages.error(request, err)
                        return redirect('ogrenci_isleri:formlar')
                    validated_files.append(f)

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
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@avrasya.edu.tr'),
                to=[STUDENT_AFFAIRS_EMAIL],
                reply_to=reply_to,
            )

            for f in validated_files:
                email_msg.attach(os.path.basename(f.name), f.read(), f.content_type or 'application/octet-stream')

            email_msg.send()
            messages.success(request, 'Kayıt formunuz başarıyla gönderildi.')
            return redirect('ogrenci_isleri:formlar')

        except Exception:
            logger.exception('Registration form submission failed')
            messages.error(request, 'Kayıt formu gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyiniz.')
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



def cift_Anadal_yandal(request):
    return render(request,'ogrenci_isleri/includes/cift_Anadal_yandal.html')

def akademik_takvim(request):
    return render(request,'ogrenci_isleri/includes/akademik_takvim.html')


