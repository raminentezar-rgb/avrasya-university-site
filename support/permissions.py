# support/permissions.py
from django.http import HttpResponseForbidden

def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'profile'):
            return HttpResponseForbidden("Access Denied")

        if request.user.profile.role != 'staff':
            return HttpResponseForbidden("Staff only")

        return view_func(request, *args, **kwargs)

    return wrapper
