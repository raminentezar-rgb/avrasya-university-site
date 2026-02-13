from django.shortcuts import render

def meslekyuksekokullari(request):
    context = {
        'title': 'MeslekYüksekokullari',
    }
    return render(request, 'meslekyuksekokullari/includes/meslekyuksekokullari.html', context)