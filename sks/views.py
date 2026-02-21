from django.shortcuts import render

# Create your views here.
def sks(request):
    return render(request, 'sks/index.html')