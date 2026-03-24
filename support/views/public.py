# support/views/public.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q, Count, CharField, TextField
from django.apps import apps
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
    
    all_results = []
    
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
            
        # -- جستجوی پویا در تمام اپلیکیشن‌های دیگر --
        excluded_apps = ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'axes', 'daphne', 'modeltranslation', 'crispy_forms', 'crispy_bootstrap5', 'channels', 'support']
        
        for model in apps.get_models():
            if model._meta.app_label in excluded_apps:
                continue
                
            if not hasattr(model, 'get_absolute_url'):
                continue
                
            if model._meta.proxy:
                continue
                
            searchable_fields = [
                f.name for f in model._meta.get_fields()
                if isinstance(f, (CharField, TextField)) and getattr(f, 'choices', None) is None
            ]
            
            if not searchable_fields:
                continue
                
            q_objects = Q()
            for field in searchable_fields:
                q_objects |= Q(**{f"{field}__icontains": query})
                
            try:
                queryset = model.objects.all()
                field_names = [f.name for f in model._meta.get_fields()]
                
                if 'yayinda' in field_names:
                    queryset = queryset.filter(yayinda=True)
                if 'aktif' in field_names:
                    queryset = queryset.filter(aktif=True)
                if 'is_active' in field_names:
                    queryset = queryset.filter(is_active=True)
                    
                dynamic_results = queryset.filter(q_objects).distinct()[:5]
                
                for obj in dynamic_results:
                    try:
                        url = obj.get_absolute_url()
                    except Exception:
                        continue
                        
                    title_attr = next((attr for attr in ['baslik', 'title', 'question', 'name', 'ad'] if hasattr(obj, attr)), None)
                    title = getattr(obj, title_attr, str(obj)) if title_attr else str(obj)
                    if callable(title): title = title()
                    
                    content_attr = next((attr for attr in ['icerik', 'detayli_aciklama', 'aciklama', 'answer', 'description', 'kisa_aciklama', 'content'] if hasattr(obj, attr)), None)
                    content = getattr(obj, content_attr, '') if content_attr else ''
                    if callable(content): content = content()
                    
                    category = str(model._meta.verbose_name).title()
                    app_config = apps.get_app_config(model._meta.app_label)
                    department = str(app_config.verbose_name)
                    
                    created_at = None
                    if hasattr(obj, 'olusturulma_tarihi'):
                        created_at = obj.olusturulma_tarihi
                    elif hasattr(obj, 'created_at'):
                        created_at = obj.created_at
                    elif hasattr(obj, 'yayin_tarihi'):
                        created_at = obj.yayin_tarihi
                    
                    all_results.append({
                        'type': 'guide',  # Use generic type for proper icon in template
                        'title': title,
                        'content': content,
                        'category': category,
                        'department': department,
                        'created_at': created_at,
                        'url': url,
                    })
            except Exception as e:
                pass

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

