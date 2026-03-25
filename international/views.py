from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .forms import InternationalApplicationForm

def international(request):
    return render(request,'international/includes/international.html')

def city_of_trabzon(request):
    return render(request,'international/includes/city_of_trabzon.html')

def campus_life(request):
    return render(request,'international/includes/campus_life.html')

def application(request):
    return render(request,'international/includes/application.html')

def academic_enviorment(request):
    return render(request,'international/includes/academic_enviorment.html')

def programers(request):
    return render(request,'international/includes/programers.html')

def application_form(request):
    if request.method == 'POST':
        form = InternationalApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            
            # Send email notification
            try:
                subject = f'New International Student Application: {application.first_name} {application.last_name}'
                context = {
                    'application': application,
                    'site_url': getattr(settings, 'SITE_URL', 'https://www.avrasya.edu.tr'),
                }
                html_message = render_to_string('international/emails/application_notification.html', context)
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = ['international@avrasya.edu.tr']
                
                send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)
            except Exception as e:
                # Log the error but don't fail the request
                print(f"Error sending email: {e}")
            
            return JsonResponse({'status': 'success', 'message': 'Application submitted successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    return render(request,'international/includes/application_form.html')


