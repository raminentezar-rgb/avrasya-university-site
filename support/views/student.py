from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from support.models import Ticket


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'support/my_tickets.html', {
        'tickets': tickets
    })


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        user=request.user
    )

    replies = ticket.replies.all().order_by('created_at')

    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket,
        'replies': replies
    })

