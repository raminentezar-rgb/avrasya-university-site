# support/services/notifier.py
from django.core.mail import send_mail
from django.core.mail import send_mail
from django.conf import settings



def notify_department(ticket):
    if ticket.department and ticket.department.email:
        send_mail(
            subject=f"Yeni Destek Talebi: {ticket.subject}",
            message=ticket.message,
            from_email=None,
            recipient_list=[ticket.department.email],
        )


def notify_student(ticket):
    send_mail(
        subject=f"Destek Talebinize Yanıt Verildi",
        message=f"""
Merhaba {ticket.user.username},

Sorunuza yanıt verilmiştir:

{ticket.response}

Avrasya Üniversitesi
Öğrenci Destek Merkezi
""",
        from_email=None,
        recipient_list=[ticket.user.email],
    )



def notify_student(ticket):
    send_mail(
        subject=f"Answer to your ticket: {ticket.subject}",
        message="Your ticket has been answered. Please login to view the response.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[ticket.user.email],
    )






def notify_student_reply(ticket, reply_message):
    subject = f"Destek Talebinize Yanıt: {ticket.subject}"
    message = f"""
Merhaba {ticket.user.username},

Destek talebinize ilgili birim tarafından yanıt verilmiştir:

{reply_message}

Sorularınız için bizimle tekrar iletişime geçebilirsiniz.

Saygılarımızla,
Üniversite Destek Birimi
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [ticket.user.email],
        fail_silently=False
    )
