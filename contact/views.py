from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # ۱. ذخیره در دیتابیس
            contact_instance = form.save()
            
            # استخراج داده‌ها برای استفاده در ایمیل
            name = form.cleaned_data['name']
            student_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_body = form.cleaned_data['message']

            # ۲. ارسال ایمیل اطلاع‌رسانی به مدیریت (شما)
            admin_subject = f"فرم تماس جدید: {subject}"
            admin_message = f"نام فرستنده: {name}\nایمیل: {student_email}\n\nمتن پیام:\n{message_body}"
            
            try:
                # ارسال به مدیریت
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER], # ایمیل شما که در settings تعریف شده
                    fail_silently=False,
                )

                # ۳. ارسال ایمیل تایید خودکار به دانشجو (اختیاری اما حرفه‌ای)
                student_subject = "Avrasya Üniversitesi - Mesajınız Alındı"
                student_body = f"Merhaba {name},\n\nMesajınız bize ulaştı. En kısa sürede size dönüş yapacağız.\n\nİyi günler dileriz."
                
                send_mail(
                    student_subject,
                    student_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [student_email],
                    fail_silently=False,
                )

                messages.success(request, 'Mesajınız başarıyla gönderildi ve e-posta onayı yollandı.')
                # هدایت به صفحه تشکر (فایل thanks.html که داشتید)
                return render(request, 'contact/thanks.html', {'name': name})
                
            except Exception as e:
                # اگر ایمیل ارسال نشد، پیام ذخیره شده اما خطا نمایش داده می‌شود
                messages.warning(request, 'Mesaj kaydedildi ancak e-posta gönderilirken bir hata oluştu.')
                return redirect('contact:contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact/includes/contact.html', {'form': form})