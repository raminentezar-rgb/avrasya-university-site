from django.shortcuts import render

def enstituler(request):
    context = {
        'title': 'Enstitüler',
    }
    return render(request, 'enstituler/enstituler.html', context)