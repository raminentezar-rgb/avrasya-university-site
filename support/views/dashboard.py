# support/views/dashboard.py
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from support.models import Ticket, TicketReply
from support.services.notifier import notify_student
from support.services.notifier import notify_student_reply




@login_required
@staff_member_required
def department_dashboard(request):
    if not hasattr(request.user, 'department') or request.user.department is None:
        return redirect('support:faq_list')

    tickets = Ticket.objects.filter(
        department=request.user.department,
        status='open'
    )

    return render(
        request,
        'support/department/dashboard.html',
        {'tickets': tickets}
    )


@staff_member_required
def reply_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        message = request.POST.get('message')

        TicketReply.objects.create(
            ticket=ticket,
            staff=request.user,
            message=message
        )

        ticket.status = 'answered'
        ticket.save()

        notify_student_reply(ticket, message)

        return redirect('support:department_dashboard')

    return render(request, 'support/department/reply_ticket.html', {
        'ticket': ticket
    })

