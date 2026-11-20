# support/views/public.py
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import translation

from support.models import Department, FAQ, KnowledgeBase
from support.services.search import search_site_content


def _classify_faq(faq):
    text = f"{faq.question} {faq.answer}".lower()
    if any(k in text for k in ('ücret', 'taksit', 'harç', 'burs', 'ödeme')):
        return 'mali', 'Burs & Ücretler'
    if any(k in text for k in ('tez', 'akts', 'lisansüstü', 'enstitü', 'devam zorunluluğu', 'geçme notu', 'başvuru')):
        return 'enstitu', 'Lisansüstü'
    if any(k in text for k in ('yemekhane', 'kütüphane', 'spor', 'wi-fi', 'eduroam', 'internet', 'yerleşke')):
        return 'kampus', 'Kampüs & Teknik'
    if any(k in text for k in ('dekan', 'müdür', 'fakülte', 'yüksekokul')):
        return 'yonetim', 'Yönetim & Birimler'
    return 'genel', 'Genel'


def support_search(request):
    query = request.GET.get("q", "").strip()
    active_type = (request.GET.get("type") or "all").strip()
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    lang_code = translation.get_language() or 'tr'

    all_results = search_site_content(query, lang_code=lang_code, limit=80) if len(query) >= 2 else []

    if is_ajax:
        return JsonResponse({
            'results': all_results[:7],
            'total': len(all_results),
        })

    type_labels = [
        ('page', 'Sayfa & Portal'),
        ('academic', 'Akademik & Bölüm'),
        ('faq', 'SSS'),
        ('news', 'Haber & Duyuru'),
        ('guide', 'Rehber & Kalite'),
    ]
    counts = {}
    for item in all_results:
        t = item.get('type', 'page')
        counts[t] = counts.get(t, 0) + 1

    type_tabs = [
        {'slug': slug, 'label': label, 'count': counts.get(slug, 0)}
        for slug, label in type_labels
        if counts.get(slug, 0) > 0
    ]

    valid_types = {t['slug'] for t in type_tabs}
    if active_type != 'all' and active_type not in valid_types:
        active_type = 'all'

    filtered_results = (
        all_results if active_type == 'all'
        else [r for r in all_results if r.get('type') == active_type]
    )

    paginator = Paginator(filtered_results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    popular_topics = []
    icon_map = [
        ('öğrenci', 'fa-user-graduate'),
        ('bilgi işlem', 'fa-laptop-code'),
        ('sağlık hizmetleri', 'fa-notes-medical'),
        ('mühendislik', 'fa-cogs'),
        ('sağlık bilimleri', 'fa-heartbeat'),
        ('idari', 'fa-building'),
        ('insan', 'fa-book-reader'),
        ('meslek', 'fa-briefcase'),
    ]
    preferred_names = [
        'Öğrenci İşleri',
        'Bilgi İşlem',
        'Sağlık Hizmetleri Meslek Yüksekokulu',
        'İdari Birimler',
        'Mühendislik ve Mimarlık Fakültesi',
        'İnsan ve Toplum Bilimleri Fakültesi',
    ]
    all_depts = list(Department.objects.all())
    dept_by_name = {d.name: d for d in all_depts}
    ordered_depts = [dept_by_name[n] for n in preferred_names if n in dept_by_name]
    for d in all_depts:
        if d not in ordered_depts and len(ordered_depts) < 6:
            ordered_depts.append(d)

    for dept in ordered_depts[:6]:
        lname = dept.name.lower()
        icon = next((ic for kw, ic in icon_map if kw in lname), 'fa-university')
        popular_topics.append({
            'id': dept.id,
            'name': dept.name,
            'subtitle': 'Doğrudan bu birime talep açın',
            'icon': icon,
        })

    return render(request, "support/search.html", {
        "page_obj": page_obj,
        "query": query,
        "active_type": active_type,
        "type_tabs": type_tabs,
        "total_results": len(all_results),
        "filtered_results_count": len(filtered_results),
        "popular_topics": popular_topics,
        "faq_count": FAQ.objects.filter(is_active=True).count(),
    })


def faq_list_view(request):
    initial_query = (request.GET.get('q') or '').strip()
    raw_faqs = FAQ.objects.filter(is_active=True).select_related('department').order_by('id')

    faqs_enriched = []
    seen = set()
    cat_counts = {}
    for faq in raw_faqs:
        norm_q = ' '.join((faq.question or '').lower().split())
        if norm_q in seen:
            continue
        seen.add(norm_q)
        cat_slug, cat_label = _classify_faq(faq)
        faq.category_slug = cat_slug
        faq.category_label = cat_label
        faqs_enriched.append(faq)
        cat_counts[cat_slug] = cat_counts.get(cat_slug, 0) + 1

    category_order = [
        ('yonetim', 'Yönetim & Dekanlık'),
        ('kampus', 'Kampüs & Teknik'),
        ('enstitu', 'Lisansüstü'),
        ('mali', 'Burs & Ücretler'),
        ('genel', 'Genel'),
    ]
    filter_categories = [
        {'slug': slug, 'label': label, 'count': cat_counts.get(slug, 0)}
        for slug, label in category_order
        if cat_counts.get(slug, 0) > 0
    ]

    return render(request, 'support/faq_list.html', {
        'faqs': faqs_enriched,
        'filter_categories': filter_categories,
        'initial_query': initial_query,
    })


def faq_detail(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    return render(request, 'support/faq_detail.html', {'faq': faq})


def knowledge_detail(request, pk):
    item = get_object_or_404(KnowledgeBase, pk=pk)
    KnowledgeBase.objects.filter(pk=item.pk).update(views=F('views') + 1)
    item.refresh_from_db(fields=['views'])
    return render(request, 'support/knowledge_detail.html', {'item': item})
