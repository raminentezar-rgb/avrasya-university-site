# support/views/public.py
from django.shortcuts import render
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
            'category': 'عمومی',  # FAQ فیلد category ندارد
            'department': faq.department.name if faq.department else 'همه',
            'created_at': None,
            'url': '#',
        })
    
    # مطالب پایگاه دانش
    for kb in results['knowledge']:
        all_results.append({
            'type': kb.content_type,
            'title': kb.title,
            'content': kb.content,
            'category': kb.category.name if kb.category else 'عمومی',
            'department': kb.department.name if kb.department else 'همه',
            'created_at': kb.created_at,
            'url': '#',
        })
    
    # لینک‌های مهم
    for link in results['links']:
        all_results.append({
            'type': 'link',
            'title': link.title,
            'content': link.description,
            'category': link.category.name if link.category else 'عمومی',
            'department': '',
            'created_at': None,
            'url': link.url,
        })
    
    # مرتب‌سازی
    with_date = [r for r in all_results if r.get('created_at')]
    without_date = [r for r in all_results if not r.get('created_at')]
    
    with_date.sort(key=lambda x: x['created_at'], reverse=True)
    all_results = with_date + without_date
    
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


# اضافه کردن تابع faq_list_view که در __init__.py فراخوانی شده
def faq_list_view(request):
    faqs = FAQ.objects.all()  # همه سوالات متداول
    return render(request, 'support/faq_list.html', {'faqs': faqs})