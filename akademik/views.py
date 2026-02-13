from django.shortcuts import render



def academic_page(request):
    return render(request, 'akademik/includes/home.html')
