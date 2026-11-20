# support/views/dashboard.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from support.models import Ticket, TicketReply
from support.services.notifier import notify_student_reply
from support.services.uploads import validate_attachment


def _is_support_staff(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    profile = getattr(user, 'profile', None)
    return getattr(profile, 'role', None) == 'staff'


def _get_user_department(user):
    dept = getattr(user, 'department', None)
    if dept:
        return dept
    profile = getattr(user, 'profile', None)
    return getattr(profile, 'department', None)


@login_required
def department_dashboard(request):
    if not _is_support_staff(request.user):
        return redirect('support:faq_list')

    user_department = _get_user_department(request.user)
    if not user_department and not request.user.is_superuser:
        return redirect('support:faq_list')

    base_qs = Ticket.objects.select_related('user', 'department', 'category').order_by('-created_at')
    if not (request.user.is_superuser and not user_department):
        base_qs = base_qs.filter(department=user_department)

    status_filter = (request.GET.get('status') or 'all').strip()
    priority_filter = (request.GET.get('priority') or 'all').strip()
    query_filter = (request.GET.get('q') or '').strip()

    tickets = base_qs
    if status_filter in {'open', 'answered', 'closed'}:
        tickets = tickets.filter(status=status_filter)
    if priority_filter in {'low', 'medium', 'high'}:
        tickets = tickets.filter(priority=priority_filter)
    if query_filter:
        tickets = tickets.filter(
            Q(tracking_code__icontains=query_filter)
            | Q(subject__icontains=query_filter)
            | Q(guest_name__icontains=query_filter)
            | Q(guest_email__icontains=query_filter)
            | Q(user__username__icontains=query_filter)
            | Q(user__first_name__icontains=query_filter)
            | Q(user__last_name__icontains=query_filter)
            | Q(user__email__icontains=query_filter)
        )

    return render(
        request,
        'support/department/dashboard.html',
        {
            'tickets': tickets,
            'total_tickets': base_qs.count(),
            'pending_tickets': base_qs.filter(status='open').count(),
            'resolved_tickets': base_qs.filter(status='answered').count(),
            'closed_tickets': base_qs.filter(status='closed').count(),
            'status_filter': status_filter,
            'priority_filter': priority_filter,
            'query_filter': query_filter,
        },
    )


@login_required
def reply_ticket(request, ticket_id):
    if not _is_support_staff(request.user):
        return HttpResponseForbidden("Bu departmana erişim yetkiniz bulunmamaktadır.")

    user_department = _get_user_department(request.user)
    if request.user.is_superuser:
        ticket = get_object_or_404(Ticket.objects.select_related('department', 'category', 'user'), id=ticket_id)
    elif user_department:
        ticket = get_object_or_404(
            Ticket.objects.select_related('department', 'category', 'user'),
            id=ticket_id,
            department=user_department,
        )
    else:
        return HttpResponseForbidden("Bu departmana erişim yetkiniz bulunmamaktadır.")

    if request.method == 'POST':
        message_text = (request.POST.get('message') or request.POST.get('response') or '').strip()
        new_status = (request.POST.get('status') or 'answered').strip()
        if new_status not in {'open', 'answered', 'closed'}:
            new_status = 'answered'

        attachment = request.FILES.get('attachment')
        attachment_ok, attachment_err = validate_attachment(attachment)

        if not attachment_ok:
            messages.error(request, attachment_err)
        elif not message_text and not attachment and new_status == ticket.status:
            messages.error(request, "Lütfen yanıt metnini giriniz.")
        else:
            if message_text or attachment:
                TicketReply.objects.create(
                    ticket=ticket,
                    staff=request.user,
                    sender_name=request.user.get_full_name() or request.user.username,
                    is_staff_reply=True,
                    message=message_text or "Ek dosya gönderildi.",
                    attachment=attachment,
                )
            ticket.status = new_status
            ticket.save(update_fields=['status', 'updated_at'])

            if message_text or attachment:
                notify_student_reply(ticket, message_text or "Ek dosya gönderildi.")
            messages.success(request, "Yanıt ve talep durumu güncellendi.")
            return redirect('support:department_dashboard')

    replies = ticket.replies.select_related('staff').all().order_by('created_at')
    return render(request, 'support/department/reply_ticket.html', {
        'ticket': ticket,
        'replies': replies,
    })
