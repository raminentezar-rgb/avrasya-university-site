from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from support.models import Ticket, TicketReply
from support.services.notifier import notify_department_followup, notify_student_reply
from support.services.uploads import validate_attachment
from .dashboard import _get_user_department, _is_support_staff


def _can_access_ticket(request, ticket):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return True
        if ticket.user_id == user.id:
            return True
        if user.email and ticket.guest_email and ticket.guest_email.lower() == user.email.lower():
            return True
        if _is_support_staff(user):
            dept = _get_user_department(user)
            if dept and ticket.department_id == dept.id:
                return True

    verified_codes = request.session.get('verified_ticket_codes', [])
    return bool(ticket.tracking_code and ticket.tracking_code in verified_codes)


def my_tickets(request):
    if not request.user.is_authenticated:
        return redirect('support:track_ticket')

    email_filter = Q(user=request.user)
    if request.user.email:
        email_filter |= Q(guest_email__iexact=request.user.email)

    tickets = Ticket.objects.filter(email_filter).select_related('department', 'category').order_by('-created_at')

    return render(request, 'support/my_tickets.html', {
        'tickets': tickets,
        'open_tickets': tickets.filter(status='open').count(),
        'answered_tickets': tickets.filter(status='answered').count(),
        'closed_tickets': tickets.filter(status='closed').count(),
    })


def track_ticket(request):
    verified_codes = request.session.get('verified_ticket_codes', [])
    session_tickets = Ticket.objects.filter(tracking_code__in=verified_codes).select_related('department', 'category').order_by('-created_at') if verified_codes else Ticket.objects.none()

    lookup_code = ''
    lookup_email = ''

    if request.method == 'POST':
        lookup_code = (request.POST.get('tracking_code') or '').strip().upper()
        lookup_email = (request.POST.get('email') or '').strip()

        if not lookup_code or not lookup_email:
            messages.error(request, "Lütfen talep takip kodunu ve e-posta adresinizi giriniz.")
        else:
            ticket = Ticket.objects.filter(tracking_code__iexact=lookup_code).filter(
                Q(guest_email__iexact=lookup_email) | Q(user__email__iexact=lookup_email)
            ).first()
            if not ticket:
                messages.error(request, "Bu takip kodu ve e-posta adresine ait bir talep bulunamadı.")
            else:
                if ticket.tracking_code not in verified_codes:
                    verified_codes = list(verified_codes) + [ticket.tracking_code]
                    request.session['verified_ticket_codes'] = verified_codes
                return redirect('support:ticket_detail', ticket_id=ticket.id)

    return render(request, 'support/ticket_track.html', {
        'session_tickets': session_tickets,
        'lookup_code': lookup_code,
        'lookup_email': lookup_email,
    })


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(
        Ticket.objects.select_related('department', 'category', 'user'),
        id=ticket_id,
    )
    if not _can_access_ticket(request, ticket):
        if not request.user.is_authenticated:
            messages.info(request, "Talebinizi görüntülemek için takip kodunuz ve e-posta adresinizle doğrulama yapınız.")
            return redirect('support:track_ticket')
        raise Http404("Talep bulunamadı.")

    is_dept_staff = request.user.is_authenticated and (
        request.user.is_superuser
        or (_is_support_staff(request.user) and _get_user_department(request.user) == ticket.department)
    )

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'close':
            if ticket.status != 'closed':
                ticket.status = 'closed'
                ticket.save(update_fields=['status', 'updated_at'])
                messages.success(request, "Destek talebi kapatıldı.")
            return redirect('support:ticket_detail', ticket_id=ticket.id)

        if action == 'reply':
            reply_text = (request.POST.get('message') or '').strip()
            attachment = request.FILES.get('attachment')
            attachment_ok, attachment_err = validate_attachment(attachment)

            if ticket.status == 'closed':
                messages.error(request, "Kapalı bir talebe yeni yanıt eklenemez.")
            elif not reply_text and not attachment:
                messages.error(request, "Lütfen yanıt mesajınızı yazınız veya dosya ekleyiniz.")
            elif not attachment_ok:
                messages.error(request, attachment_err)
            else:
                as_staff = bool(is_dept_staff and ticket.user_id != request.user.id)
                sender_name = (
                    (request.user.get_full_name() or request.user.username)
                    if request.user.is_authenticated
                    else ticket.requester_name
                )
                TicketReply.objects.create(
                    ticket=ticket,
                    staff=request.user if request.user.is_authenticated else None,
                    sender_name=sender_name,
                    is_staff_reply=as_staff,
                    message=reply_text or "Ek dosya gönderildi.",
                    attachment=attachment,
                )
                if as_staff:
                    ticket.status = 'answered'
                    ticket.save(update_fields=['status', 'updated_at'])
                    notify_student_reply(ticket, reply_text or "Ek dosya gönderildi.")
                else:
                    ticket.status = 'open'
                    ticket.save(update_fields=['status', 'updated_at'])
                    notify_department_followup(ticket, reply_text or "Ek dosya gönderildi.")
                messages.success(request, "Yanıtınız başarıyla gönderildi.")
            return redirect('support:ticket_detail', ticket_id=ticket.id)

    replies = ticket.replies.select_related('staff').all().order_by('created_at')

    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket,
        'replies': replies,
        'is_dept_staff': is_dept_staff,
    })
