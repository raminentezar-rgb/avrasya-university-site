
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import StudentSignUpForm

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
