# yatay_gecis/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Mevcut view fonksiyonları (sadece bir kez tanımlanmalı)
def yatay_gecis_view(request):
    """
    ویو اصلی صفحه یاتای گچیش با فرم درخواست تماس
    """
    if request.method == 'POST':
        try:
            # JSON verisini parse et
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Geçersiz veri formatı.'
                }, status=400)
            
            # Verileri kontrol et
            full_name = data.get('full_name')
            email = data.get('email')
            phone = data.get('phone')
            accept_communication = data.get('accept_communication')
            accept_kvkk = data.get('accept_kvkk')
            
            # Basit validasyon
            errors = {}
            if not full_name:
                errors['full_name'] = 'Ad Soyad alanı zorunludur.'
            if not email:
                errors['email'] = 'E-posta alanı zorunludur.'
            elif '@' not in email:
                errors['email'] = 'Geçerli bir e-posta adresi giriniz.'
            if not phone:
                errors['phone'] = 'Telefon alanı zorunludur.'
            if not accept_communication:
                errors['accept_communication'] = 'İletişim izni vermelisiniz.'
            if not accept_kvkk:
                errors['accept_kvkk'] = 'KVKK onayı vermelisiniz.'
            
            if errors:
                return JsonResponse({
                    'status': 'error',
                    'errors': errors
                }, status=400)
            
            # E-posta gönder (basit versiyon)
            try:
                # Admin e-postası
                admin_subject = f'Yeni Geri Arama Talebi - {full_name}'
                admin_message = f"""
                Yeni bir geri arama talebi alındı.
                
                Ad Soyad: {full_name}
                E-posta: {email}
                Telefon: {phone}
                Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}
                """
                
                send_mail(
                    subject=admin_subject,
                    message=admin_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
                
                # Kullanıcıya onay e-postası
                user_subject = 'Geri Arama Talebiniz Alındı - Avrasya Üniversitesi'
                user_message = f"""
                Sayın {full_name},
                
                Geri arama talebiniz tarafımıza ulaşmıştır. En kısa sürede {phone} numaralı telefondan sizinle iletişime geçeceğiz.
                
                Saygılarımızla,
                Avrasya Üniversitesi
                """
                
                send_mail(
                    subject=user_subject,
                    message=user_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Email gönderim hatası: {str(e)}")
                # Email hatası olsa bile kullanıcıya başarılı mesajı göster
            
            return JsonResponse({
                'status': 'success',
                'message': 'Formunuz başarıyla gönderildi! En kısa sürede sizinle iletişime geçeceğiz.'
            })
            
        except Exception as e:
            logger.error(f"Form işleme hatası: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Bir hata oluştu. Lütfen daha sonra tekrar deneyin.'
            }, status=500)
    
    # GET isteği için normal sayfayı göster
    return render(request, 'yatay_gecis/includes/yatay_gecis.html')


def yatay_Kontenjanlar(request):
    return render(request, 'yatay_gecis/includes/yatay_Kontenjanlar.html')


def yatay_geciste_istenilen_Bbelgeler(request):
    return render(request, 'yatay_gecis/includes/yatay_geciste_istenilen_Bbelgeler.html')


def ortalama(request):
    return render(request, 'yatay_gecis/includes/ortalama.html')


def ek_madde(request):
    return render(request, 'yatay_gecis/includes/ek_madde.html')


def degerlendirme_bicimi(request):
    return render(request, 'yatay_gecis/includes/degerlendirme_bicimi.html')


def burslar(request):
    return render(request, 'yatay_gecis/includes/burslar.html')


def kayıt_yeri(request):
    return render(request, 'yatay_gecis/includes/kayıt_yeri.html')


def yatay_taban(request):
    return render(request, 'yatay_gecis/includes/yatay_taban_puanlar.html')


def orenci_isleri_daire_baskanli(request):
    return render(request, 'yatay_gecis/includes/orenci_isleri_daire_baskanli.html')


def takvim(request):
    return render(request, 'yatay_gecis/includes/takvim.html')


def bahar(request):
    return render(request, 'yatay_gecis/includes/bahar.html')


# API endpoint için ek fonksiyon
@csrf_exempt
def callback_request_api(request):
    """
    API endpoint for callback requests (separate from the main view)
    """
    if request.method == 'POST':
        try:
            # JSON verisini parse et
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Geçersiz veri formatı.'
                }, status=400)
            
            # Verileri kontrol et
            full_name = data.get('full_name')
            email = data.get('email')
            phone = data.get('phone')
            accept_communication = data.get('accept_communication')
            accept_kvkk = data.get('accept_kvkk')
            
            # Basit validasyon
            errors = {}
            if not full_name:
                errors['full_name'] = 'Ad Soyad alanı zorunludur.'
            if not email:
                errors['email'] = 'E-posta alanı zorunludur.'
            elif '@' not in email:
                errors['email'] = 'Geçerli bir e-posta adresi giriniz.'
            if not phone:
                errors['phone'] = 'Telefon alanı zorunludur.'
            if not accept_communication:
                errors['accept_communication'] = 'İletişim izni vermelisiniz.'
            if not accept_kvkk:
                errors['accept_kvkk'] = 'KVKK onayı vermelisiniz.'
            
            if errors:
                return JsonResponse({
                    'status': 'error',
                    'errors': errors
                }, status=400)
            
            # E-posta gönder
            try:
                # Admin e-postası
                admin_subject = f'Yeni Geri Arama Talebi (API) - {full_name}'
                admin_message = f"""
                Yeni bir geri arama talebi alındı (API üzerinden).
                
                Ad Soyad: {full_name}
                E-posta: {email}
                Telefon: {phone}
                Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}
                """
                
                send_mail(
                    subject=admin_subject,
                    message=admin_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
                
                # Kullanıcıya onay e-postası
                user_subject = 'Geri Arama Talebiniz Alındı - Avrasya Üniversitesi'
                user_message = f"""
                Sayın {full_name},
                
                Geri arama talebiniz tarafımıza ulaşmıştır. En kısa sürede {phone} numaralı telefondan sizinle iletişime geçeceğiz.
                
                Saygılarımızla,
                Avrasya Üniversitesi
                """
                
                send_mail(
                    subject=user_subject,
                    message=user_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"API email gönderim hatası: {str(e)}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Formunuz başarıyla gönderildi! En kısa sürede sizinle iletişime geçeceğiz.'
            })
            
        except Exception as e:
            logger.error(f"API form işleme hatası: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Bir hata oluştu. Lütfen daha sonra tekrar deneyin.'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Geçersiz metod. Sadece POST isteklerine izin verilir.'
    }, status=405)