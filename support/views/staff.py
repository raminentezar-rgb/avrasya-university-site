# support/views/staff.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone

from support.models import Ticket
from support.services.notifier import notify_student
from support.permissions import staff_required

@login_required
@staff_required
def respond_ticket(request, ticket_id):
    profile = request.user.profile

    # ⛔ فقط Staff
    if profile.role != 'staff':
        return HttpResponseForbidden("Access Denied")

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        department=profile.department
    )

    if request.method == 'POST':
        ticket.response = request.POST['response']
        ticket.status = 'answered'
        ticket.responded_at = timezone.now()
        ticket.save()

        # ✉ ایمیل به دانشجو
        notify_student(ticket)

        return redirect('support:department_dashboard')

    return render(request, 'support/respond_ticket.html', {
        'ticket': ticket
    })
