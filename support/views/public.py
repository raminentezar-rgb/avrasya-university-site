# support/views/public.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q, Count
from support.models import FAQ, KnowledgeBase, ImportantLink, Department, Category, Tag
from django.core.paginator import Paginator

def support_search(request):
    query = request.GET.get("q", "").strip()
    results = {
        'faqs': [],
        'knowledge': [],
        'links': [],
        'departments': [],
        'categories': [],
        'tags': [],
    }
    
    if query:
        # جستجوی هوشمند در FAQ
        results['faqs'] = FAQ.objects.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query)
        ).select_related('department')
        
        # جستجوی جامع در پایگاه دانش
        results['knowledge'] = KnowledgeBase.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).select_related('category', 'department')
        
        # جستجوی لینک‌های مهم
        results['links'] = ImportantLink.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
        
        # جستجو در دپارتمان‌ها
        results['departments'] = Department.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )
        
        # جستجو در دسته‌بندی‌ها
        results['categories'] = Category.objects.filter(
            Q(name__icontains=query)
        )
        
        # جستجو در تگ‌ها
        results['tags'] = Tag.objects.filter(
            Q(name__icontains=query)
        )
    
    # ترکیب و مرتب‌سازی نتایج
    all_results = []
    
    # FAQ‌ها با اولویت بالا
    for faq in results['faqs']:
        all_results.append({
            'type': 'faq',
            'title': faq.question,
            'content': faq.answer,
            'category': 'SSS',
            'department': faq.department.name if faq.department else 'Genel',
            'created_at': None,
            'url': reverse('support:faq_detail', kwargs={'pk': faq.pk}),
        })
    
    # مطالب پایگاه دانش
    for kb in results['knowledge']:
        all_results.append({
            'id': kb.pk,
            'type': kb.content_type,
            'title': kb.title,
            'content': kb.content,
            'category': kb.category.name if kb.category else 'Bilgi Bankası',
            'department': kb.department.name if kb.department else 'Genel',
            'created_at': kb.created_at,
            'url': reverse('support:knowledge_detail', kwargs={'pk': kb.pk}),
        })
    
    # لینک‌های مهم
    for link in results['links']:
        all_results.append({
            'type': 'link',
            'title': link.title,
            'content': link.description,
            'category': 'Bağlantı',
            'department': '',
            'created_at': None,
            'url': link.url,
        })
    
    # مرتب‌سازی
    with_date = [r for r in all_results if r.get('created_at')]
    without_date = [r for r in all_results if not r.get('created_at')]
    
    if with_date:
        with_date.sort(key=lambda x: x['created_at'], reverse=True)
    all_results = with_date + without_date
    
    # اگر درخواست AJAX بود، نتایج را به صورت JSON برگردان
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'results': all_results[:5],  # فقط 5 نتیجه اول برای پیش‌نمایش
            'total': len(all_results)
        })

    # صفحه‌بندی
    paginator = Paginator(all_results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # موضوعات محبوب
    try:
        popular_topics = Category.objects.annotate(
            ticket_count=Count('ticket')
        ).order_by('-ticket_count')[:6]
    except:
        popular_topics = Category.objects.all()[:6]
    
    return render(request, "support/search.html", {
        "page_obj": page_obj,
        "query": query,
        "total_results": len(all_results),
        "popular_topics": popular_topics,
        "results_by_type": results,
    })


def faq_list_view(request):
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'support/faq_list.html', {'faqs': faqs})

def faq_detail(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    return render(request, 'support/faq_detail.html', {'faq': faq})

def knowledge_detail(request, pk):
    item = get_object_or_404(KnowledgeBase, pk=pk)
    item.views += 1
    item.save()
    return render(request, 'support/knowledge_detail.html', {'item': item})
