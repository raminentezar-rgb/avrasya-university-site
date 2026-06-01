from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .services import OBSIntegrationService, TuitionCalculatorService

def index(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        if not student_id:
            messages.error(request, "Lütfen T.C. Kimlik / Pasaport numaranızı giriniz.")
            return redirect('tuition:index')
        
        # ۱. دریافت اطلاعات خام از سرویس OBS
        raw_student_data = OBSIntegrationService.get_student_data(student_id)
        
        if raw_student_data:
            # اگر دانشجو وجود داشت، کاربر را به صفحه پرداخت هدایت می‌کنیم
            # در یک سیستم واقعی ممکن است اینجا بررسی کنیم که آیا اصلا بدهی دارد یا خیر
            return redirect('tuition:payment', student_id=student_id)
        else:
            messages.error(request, "Öğrenci bulunamadı veya bu döneme ait borcunuz bulunmamaktadır.")
            return redirect('tuition:index')

    return render(request, 'tuition/index.html')

def payment(request, student_id):
    # ۱. دریافت مجدد اطلاعات خام (یا دریافت از Session)
    raw_student_data = OBSIntegrationService.get_student_data(student_id)
    if not raw_student_data:
        messages.error(request, "Geçersiz işlem veya öğrenci bilgisi bulunamadı.")
        return redirect('tuition:index')
    
    # ۲. ارسال اطلاعات خام به سرویس محاسبه‌گر شهریه
    processed_student_data = TuitionCalculatorService.calculate_final_balance(raw_student_data)
    
    if request.method == 'POST':
        # Here we would normally integrate with a virtual POS (like PayTR, Iyzico, or a Bank)
        # We'll simulate a successful payment
        return redirect('tuition:success')

    context = {
        'student': processed_student_data,
        'student_id': student_id
    }
    return render(request, 'tuition/payment.html', context)

def success(request):
    return render(request, 'tuition/success.html')
