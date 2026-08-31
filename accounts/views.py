from django.shortcuts import render, redirect
from django.db.models import Count, Q
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
