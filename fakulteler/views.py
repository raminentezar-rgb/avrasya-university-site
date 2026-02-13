# fakulteler/views.py
from django.shortcuts import render

def fakulteler(request):
    context = {
        'title': 'Fakülteler',
    }
    return render(request, 'fakulteler/includes/fakulteler.html', context)