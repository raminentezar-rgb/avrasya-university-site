# support/views/staff.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from support.models import Ticket, TicketReply
from support.services.notifier import notify_student_reply
from support.permissions import staff_required
from .dashboard import _get_user_department


@login_required
@staff_required
def respond_ticket(request, ticket_id):
    profile = getattr(request.user, 'profile', None)

    # ⛔ فقط Staff یا Superuser
    if not request.user.is_superuser and (not profile or profile.role != 'staff'):
        return HttpResponseForbidden("Access Denied")

    user_department = _get_user_department(request.user)
    if request.user.is_superuser:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    elif user_department:
        ticket = get_object_or_404(Ticket, id=ticket_id, department=user_department)
    else:
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        response_text = (request.POST.get('response') or request.POST.get('message') or '').strip()
        if response_text:
            TicketReply.objects.create(
                ticket=ticket,
                staff=request.user,
                message=response_text
            )
            ticket.status = 'answered'
            ticket.save()

            # ✉ ایمیل به دانشجو
            notify_student_reply(ticket, response_text)

        return redirect('support:department_dashboard')

    return render(request, 'support/respond_ticket.html', {
        'ticket': ticket
    })
