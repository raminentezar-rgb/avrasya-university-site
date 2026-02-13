from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from support.models import Ticket,Department,Category
from support.services.notifier import notify_department

@login_required
def create_ticket(request):
    if request.method == 'POST':
        ticket = Ticket.objects.create(
            user=request.user,
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
            department_id=request.POST.get('department'),
            category_id=request.POST.get('category')
        )

        notify_department(ticket)
        return redirect('support:ticket_detail', ticket_id=ticket.id)

    departments = Department.objects.all()
    categories = Category.objects.all()

    return render(request, 'support/ticket_create.html', {
        'departments': departments,
        'categories': categories,
    })