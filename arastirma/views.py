from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from .models import ResearchPolicy, BAPProject, Laboratory

def research_home(request):
    context = {
        'policies': ResearchPolicy.objects.filter(is_active=True)[:6],
        'featured_projects': BAPProject.objects.filter(status='ongoing')[:6],
        'active_labs': Laboratory.objects.filter(is_active=True)[:8],
        'stats': {
            'total_projects': BAPProject.objects.count(),
            'total_labs': Laboratory.objects.filter(is_active=True).count(),
            'total_centers': 0,  # بعداً اضافه می‌شود
            'total_patents': 0,  # بعداً اضافه می‌شود
        }
    }
    return render(request, 'arastirma/home.html', context)

def policy_list(request):
    policies = ResearchPolicy.objects.filter(is_active=True)
    return render(request, 'arastirma/policy_list.html', {'policies': policies})

def policy_detail(request, pk):
    policy = get_object_or_404(ResearchPolicy, pk=pk, is_active=True)
    return render(request, 'arastirma/policy_detail.html', {'policy': policy})

def bap_list(request):
    projects = BAPProject.objects.all()
    status_filter = request.GET.get('status')
    
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    context = {
        'projects': projects,
        'total_budget': projects.aggregate(Sum('budget'))['budget__sum'] or 0,
        'project_count': projects.count(),
    }
    return render(request, 'arastirma/bap_list.html', context)

def bap_detail(request, project_id):
    project = get_object_or_404(BAPProject, pk=project_id)
    return render(request, 'arastirma/bap_detail.html', {'project': project})

def lab_list(request):
    labs = Laboratory.objects.filter(is_active=True)
    faculty_filter = request.GET.get('faculty')
    
    if faculty_filter:
        labs = labs.filter(faculty__icontains=faculty_filter)
    
    return render(request, 'arastirma/lab_list.html', {'labs': labs})

def lab_detail(request, lab_id):
    lab = get_object_or_404(Laboratory, pk=lab_id, is_active=True)
    return render(request, 'arastirma/lab_detail.html', {'lab': lab})

def arastirma_merkezleri(request):
    # موقتاً از داده‌های نمونه استفاده می‌کنیم
    centers = []  # بعداً: ResearchCenter.objects.filter(is_active=True)
    context = {
        'centers': centers,
        'active_count': len([c for c in centers if c.status == 'active']),
        'total_researchers': sum(c.researcher_count for c in centers),
    }
    return render(request, 'arastirma/arastirma_merkezleri.html', context)

def fikri_Sinai_mulkiyet(request):
    return render(request, 'arastirma/fikri_Sinai_mulkiyet.html')

def arastirma_ciktilari(request):
    return render(request, 'arastirma/arastirma_ciktilari.html')

def oduller(request):
    return render(request, 'arastirma/oduller.html')

def arastirma_politikalari_danisma_kurulu(request):
    return render(request, 'arastirma/arastirma_politikalari_danisma_kurulu.html')

def arastirma_politikalari_komisyonu(request):
    return render(request, 'arastirma/arastirma_politikalari_komisyonu.html')


def bap_komisyonu(request):
    return render(request, 'arastirma/bap_komisyonu.html')

def bap_bilim_insani(request):
    return render(request, 'arastirma/bap_bilim_insani.html')

def bap_koordinatorlugu(request):
    return render(request, 'arastirma/bap_koordinatorlugu.html')





#####################################################################################




def kadin(request):
    return render(request, 'arastirma/kadin.html')

def bagimlilikla_mucadele(request):
    return render(request, 'arastirma/bagimlilikla_mucadele.html')

def uzaktan_egitim(request):
    return render(request, 'arastirma/uzaktan_egitim.html')

def girisimcilik_yenilikcilik(request):
    return render(request, 'arastirma/girisimcilik_yenilikcilik.html')

def gida_egitim(request):
    return render(request, 'arastirma/gida_egitim.html')

def goc_calismalari(request):
    return render(request, 'arastirma/goc_calismalari.html')

def turkce_ogretimi(request):
    return render(request, 'arastirma/turkce_ogretimi.html')

def kariyer_gelistirme(request):
    return render(request, 'arastirma/kariyer_gelistirme.html')

def ulastirma_uygulama(request):
    return render(request, 'arastirma/ulastirma_uygulama.html')

def teknoloji_transfer(request):
    return render(request, 'arastirma/teknoloji_transfer.html')

def surekli_egitim(request):
    return render(request, 'arastirma/surekli_egitim.html')

