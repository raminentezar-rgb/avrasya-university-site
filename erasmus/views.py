from django.shortcuts import render

def erasmus(request):
    return render(request, 'erasmus/includes/erasmus.html')