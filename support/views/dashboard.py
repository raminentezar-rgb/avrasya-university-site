# support/views/dashboard.py
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from support.models import Ticket, TicketReply
from support.services.notifier import notify_student_reply


def _get_user_department(user):
    dept = getattr(user, 'department', None)
    if dept:
        return dept
    profile = getattr(user, 'profile', None)
    return getattr(profile, 'department', None)


@login_required
@staff_member_required
def department_dashboard(request):
    user_department = _get_user_department(request.user)
    if not user_department and not request.user.is_superuser:
        return redirect('support:faq_list')

    if request.user.is_superuser and not user_department:
        tickets = Ticket.objects.filter(status='open')
    else:
        tickets = Ticket.objects.filter(
            department=user_department,
            status='open'
        )

    return render(
        request,
        'support/department/dashboard.html',
        {'tickets': tickets}
    )


@login_required
@staff_member_required
def reply_ticket(request, ticket_id):
    user_department = _get_user_department(request.user)
    if request.user.is_superuser:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    elif user_department:
        ticket = get_object_or_404(Ticket, id=ticket_id, department=user_department)
    else:
        return HttpResponseForbidden("Bu departmana erişim yetkiniz bulunmamaktadır.")

    if request.method == 'POST':
        message = (request.POST.get('message') or '').strip()
        if message:
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
