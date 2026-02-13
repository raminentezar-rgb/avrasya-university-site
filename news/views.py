from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import News, NewsAttachment

def news_list(request):
    items = News.objects.filter(is_published=True).order_by('-published_at')
    
    # دریافت پارامترهای جستجو
    search_query = request.GET.get('q')
    date_filter = request.GET.get('date')
    
    # اعمال فیلتر جستجو
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    if date_filter:
        items = items.filter(published_at__date=date_filter)
    
    return render(request, 'news/list.html', {
        'items': items,
        'search_query': search_query or '',
        'date_filter': date_filter or ''
    })


def news_detail(request, slug):
    item = get_object_or_404(
        News.objects.prefetch_related('images', 'attachments'), 
        slug=slug, 
        is_published=True
    )
    
    # دسته‌بندی پیوست‌ها بر اساس نوع
    attachments_by_type = {}
    for attachment in item.attachments.all():
        if attachment.file_type not in attachments_by_type:
            attachments_by_type[attachment.file_type] = []
        attachments_by_type[attachment.file_type].append(attachment)
    
    return render(request, 'news/detail.html', {
        'item': item,
        'attachments_by_type': attachments_by_type,
    })