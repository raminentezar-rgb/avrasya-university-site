import os
import django
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avrasya_site.settings')
django.setup()

print("--- Email Configuration Diagnostic ---")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print("--------------------------------------")

try:
    print("Attempting to send test email...")
    # Using EmailMessage as viewed in the code, but send_mail is simpler wrapper.
    # Testing with simple send_mail first.
    send_mail(
        'Test Email from Avrasya Site Config',
        'This is a test email to verify SMTP settings.',
        settings.DEFAULT_FROM_EMAIL,
        ['ramin.ent33@gmail.com'], 
        fail_silently=False,
    )
    print("SUCCESS: Email sent successfully!")
except Exception as e:
    print(f"FAILURE: Error sending email: {e}")
