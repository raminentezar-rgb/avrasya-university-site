# support/services/notifier.py
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q

logger = logging.getLogger(__name__)


def _get_tracking_url():
    base = (getattr(settings, 'SITE_URL', '') or '').rstrip('/')
    return f"{base}/support/takip/" if base else "/support/takip/"


def _send_safe_email(subject, message, recipient_list):
    recipients = [addr for addr in recipient_list if addr]
    if not recipients:
        return False
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        return True
    except Exception as exc:
        logger.warning("Destek e-postası gönderilemedi (%s): %s", recipients, exc)
        return False


def _notify_department_staff_in_app(ticket, title, message_preview):
    try:
        from chat.models import Notification
    except Exception:
        return

    recipient_users = set()
    if ticket.department and ticket.department.staff_id:
        recipient_users.add(ticket.department.staff)

    if ticket.department:
        dept_staff = User.objects.filter(
            Q(profile__department=ticket.department, profile__role='staff')
            | Q(is_superuser=True, is_active=True)
        ).distinct()
        for u in dept_staff:
            recipient_users.add(u)

    reply_path = f"/support/department/ticket/{ticket.id}/reply/"
    channel_layer = get_channel_layer()

    for user in recipient_users:
        notif = Notification.objects.create(
            user=user,
            notification_type='ticket',
            title=title[:255],
            message=message_preview[:500],
            link_url=reply_path,
        )
        if channel_layer:
            try:
                async_to_sync(channel_layer.group_send)(
                    f'notifications_{user.id}',
                    {
                        'type': 'send_notification',
                        'notification_id': notif.id,
                        'title': notif.title,
                        'message': notif.message,
                        'thread_id': None,
                        'sender_id': None,
                        'created_at': notif.created_at.strftime('%H:%M'),
                    },
                )
            except Exception:
                pass


def notify_department(ticket):
    code = ticket.tracking_code or f"#{ticket.id}"
    _notify_department_staff_in_app(
        ticket,
        title=f"Yeni Destek Talebi ({code})",
        message_preview=f"{ticket.requester_name} - {ticket.subject}",
    )

    if ticket.department and ticket.department.email:
        message = f"""Yeni destek talebi oluşturuldu.

Talep Kodu: {code}
Gönderen: {ticket.requester_name} ({ticket.requester_email or 'E-posta yok'})
Öncelik: {ticket.get_priority_display()}
Konu: {ticket.subject}

Mesaj:
{ticket.message}
"""
        _send_safe_email(
            subject=f"[{code}] Yeni Destek Talebi: {ticket.subject}",
            message=message,
            recipient_list=[ticket.department.email],
        )


def notify_requester_created(ticket):
    email = ticket.requester_email
    if not email:
        return
    tracking_url = _get_tracking_url()
    message = f"""Merhaba {ticket.requester_name},

Destek talebiniz başarıyla alınmıştır.

Talep Takip Kodu: {ticket.tracking_code}
İlgili Birim: {ticket.department.name}
Konu: {ticket.subject}

Talebinizi ve birim yanıtlarını aşağıdaki bağlantıdan takip kodunuz ve e-posta adresinizle görüntüleyebilirsiniz:
{tracking_url}

Saygılarımızla,
Avrasya Üniversitesi Destek Merkezi
"""
    _send_safe_email(
        subject=f"[{ticket.tracking_code}] Destek Talebiniz Alındı: {ticket.subject}",
        message=message,
        recipient_list=[email],
    )


def notify_student(ticket):
    email = ticket.requester_email
    if email:
        tracking_url = _get_tracking_url()
        _send_safe_email(
            subject=f"[{ticket.tracking_code or ticket.id}] Destek Talebinize Yanıt Verildi: {ticket.subject}",
            message=f"Merhaba {ticket.requester_name},\n\nDestek talebinize yanıt verilmiştir. Takip kodunuz ({ticket.tracking_code}) ile aşağıdaki adresten görüntüleyebilirsiniz:\n{tracking_url}",
            recipient_list=[email],
        )


def notify_student_reply(ticket, reply_message):
    email = ticket.requester_email
    if not email:
        return
    tracking_url = _get_tracking_url()
    subject = f"[{ticket.tracking_code or ticket.id}] Destek Talebinize Yanıt: {ticket.subject}"
    message = f"""Merhaba {ticket.requester_name},

Destek talebinize ilgili birim tarafından yanıt verilmiştir:

{reply_message}

Talebinize ek bilgi veya yeni yanıt göndermek için takip kodunuz ({ticket.tracking_code}) ve e-posta adresinizle giriş yapabilirsiniz:
{tracking_url}

Saygılarımızla,
Avrasya Üniversitesi Destek Merkezi
"""
    _send_safe_email(
        subject=subject,
        message=message,
        recipient_list=[email],
    )


def notify_department_followup(ticket, reply_message):
    code = ticket.tracking_code or f"#{ticket.id}"
    _notify_department_staff_in_app(
        ticket,
        title=f"Talebe Yeni Yanıt ({code})",
        message_preview=f"{ticket.requester_name}: {reply_message[:120]}",
    )

    if ticket.department and ticket.department.email:
        message = f"""Talep sahibi yeni bir yanıt ekledi.

Talep Kodu: {code}
Gönderen: {ticket.requester_name} ({ticket.requester_email or 'E-posta yok'})
Konu: {ticket.subject}

Yeni Mesaj:
{reply_message}
"""
        _send_safe_email(
            subject=f"[{code}] Talep Yanıtı: {ticket.subject}",
            message=message,
            recipient_list=[ticket.department.email],
        )
