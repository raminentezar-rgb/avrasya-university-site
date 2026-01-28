# support/views.py
from django.shortcuts import render
from .models import FAQ

def faq_list_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'support/faq_list.html', {'faqs': faqs})
