from django.shortcuts import render

# صفحات استاتیک مدیریت کسب و کار انگلیسی
def mutevelli_heyet_baskani(request):
    return render(request, 'avrasya_universitesi_yonetim/includes/mutevelli_heyet_baskani.html')


def mutevelli_heyeti(request):
    return render(request, 'avrasya_universitesi_yonetim/includes/mutevelli_heyeti.html')

def rektor(request):
    return render(request, 'avrasya_universitesi_yonetim/includes/rektor.html')

def rektor_yardimcilari(request):
    return render(request, 'avrasya_universitesi_yonetim/includes/rektor_yardimcilari.html')

def dekanlar(request):
    return render(request, 'avrasya_universitesi_yonetim/includes/dekanlar.html')

def genel_sekreter(request):
    return render(request, 'avrasya_universitesi_yonetim/includes/genel_sekreter.html')

def universite_senatosu(request):
    return render(request, 'avrasya_universitesi_yonetim/includes/universite_senatosu.html')

def yonetim_kurulu(request):
    return render(request, 'avrasya_universitesi_yonetim/includes/yonetim_kurulu.html')


