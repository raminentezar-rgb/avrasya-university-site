from django.shortcuts import render, redirect, resolve_url
from django.db.models import Count, Q
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import StudentSignUpForm
from .models import Profile


class CustomLoginView(auth_views.LoginView):
    """Redirect department staff to their support panel when no ?next= target is set."""

    template_name = 'accounts/login.html'

    def get_default_redirect_url(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        role = getattr(profile, 'role', None)
        if user.is_authenticated and not user.is_superuser and role == 'staff':
            return resolve_url('support:department_dashboard')
        return super().get_default_redirect_url()

def student_signup(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@user_passes_test(lambda u: u.is_superuser)
def crm_dashboard(request):
    total_users = User.objects.count()
    profile_counts = Profile.objects.aggregate(
        students_count=Count('id', filter=Q(role='student')),
        staff_count=Count('id', filter=Q(role='staff')),
        professors_count=Count('id', filter=Q(role='professor'))
    )
    students_count = profile_counts['students_count']
    staff_count = profile_counts['staff_count']
    professors_count = profile_counts['professors_count']
    
    recent_users = User.objects.select_related('profile').order_by('-date_joined')[:10]
    all_users = User.objects.select_related('profile', 'profile__department').all().order_by('-date_joined')
    
    context = {
        'total_users': total_users,
        'students_count': students_count,
        'staff_count': staff_count,
        'professors_count': professors_count,
        'recent_users': recent_users,
        'all_users': all_users,
    }
    return render(request, 'accounts/crm_dashboard.html', context)
