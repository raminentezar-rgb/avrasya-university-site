from django.shortcuts import render, get_object_or_404

# صفحات استاتیک مدیریت کسب و کار انگلیسی
def anasayfa(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/anasayfa.html')


def felsefemiz(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/felsefemiz.html')

def misyon_vizyon(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/misyon_vizyon.html')

def kurucu_vakif(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/kurucu_vakif.html')

def akreditasyon(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/akreditasyon.html')

def kalite_politikasi(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/kalite_politikasi.html')

def tarihce(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/tarihce.html')

def organizasyon_semasi(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/organizasyon_semasi.html')

def stratejik_plan(request):
    return render(request, 'avrasya_universitesi_hakkinda/includes/stratejik_plan.html')
