# support/services/notifier.py
from django.core.mail import send_mail
from django.conf import settings


def notify_department(ticket):
    if ticket.department and ticket.department.email:
        send_mail(
            subject=f"Yeni Destek Talebi: {ticket.subject}",
            message=ticket.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ticket.department.email],
            fail_silently=True,
        )


def notify_student(ticket):
    if ticket.user and ticket.user.email:
        send_mail(
            subject=f"Destek Talebinize Yanıt Verildi: {ticket.subject}",
            message="Destek talebinize yanıt verilmiştir. Yanıtı görüntülemek için lütfen sisteme giriş yapınız.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ticket.user.email],
            fail_silently=True,
        )


def notify_student_reply(ticket, reply_message):
    if not ticket.user or not ticket.user.email:
        return
    subject = f"Destek Talebinize Yanıt: {ticket.subject}"
    message = f"""Merhaba {ticket.user.username},

Destek talebinize ilgili birim tarafından yanıt verilmiştir:

{reply_message}

Sorularınız için bizimle tekrar iletişime geçebilirsiniz.

Saygılarımızla,
Avrasya Üniversitesi Öğrenci Destek Birimi
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [ticket.user.email],
        fail_silently=True,
    )
