
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import StudentSignUpForm
from .models import Profile

def student_signup(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
    students_count = Profile.objects.filter(role='student').count()
    staff_count = Profile.objects.filter(role='staff').count()
    professors_count = Profile.objects.filter(role='professor').count()
    
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
