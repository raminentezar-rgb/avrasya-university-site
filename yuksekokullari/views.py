from django.shortcuts import render

def yuksekokullari(request):
    context = {
        'title': 'Yüksekokullari',
    }
    return render(request, 'yuksekokullari/includes/yuksekokullari.html', context)