from django.shortcuts import render

def international(request):
    return render(request,'international/includes/international.html')


def city_of_trabzon(request):
    return render(request,'international/includes/city_of_trabzon.html')

def campus_life(request):
    return render(request,'international/includes/campus_life.html')

def application(request):
    return render(request,'international/includes/application.html')

def academic_enviorment(request):
    return render(request,'international/includes/academic_enviorment.html')

def programers(request):
    return render(request,'international/includes/programers.html')


def application_form(request):
    return render(request,'international/includes/application_form.html')


