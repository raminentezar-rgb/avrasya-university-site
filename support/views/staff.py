# support/views/staff.py
from .dashboard import reply_ticket


def respond_ticket(request, ticket_id):
    """Unified delegate to the primary department ticket reply handler."""
    return reply_ticket(request, ticket_id)
