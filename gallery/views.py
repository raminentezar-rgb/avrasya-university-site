from django.shortcuts import render, get_object_or_404
from .models import GalleryCategory, GalleryImage
import json
from django.core.serializers.json import DjangoJSONEncoder


def gallery_main(request):
    categories = GalleryCategory.objects.filter(is_active=True).prefetch_related('images')
    featured_images = GalleryImage.objects.filter(is_active=True).order_by('-upload_date')[:12]
    
    context = {
        'categories': categories,
        'featured_images': featured_images,
    }
    return render(request, 'gallery/main.html', context)





def gallery_category(request, slug):
    category = get_object_or_404(GalleryCategory, slug=slug, is_active=True)
    images = category.images.filter(is_active=True).order_by('order', '-upload_date')
    
    # گرفتن همه دسته‌بندی‌های فعال برای بخش "دیگر دسته‌بندی‌ها"
    all_categories = GalleryCategory.objects.filter(is_active=True).exclude(id=category.id)
    
    context = {
        'category': category,
        'images': images,
        'categories': all_categories,  # اضافه کردن این خط
    }
    return render(request, 'gallery/category.html', context)






def gallery_detail(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id, is_active=True)
    related_images = GalleryImage.objects.filter(
        category=image.category, 
        is_active=True
    ).exclude(id=image.id)[:6]
    
    # آماده‌سازی داده‌های JSON برای تصاویر مرتبط
    related_images_data = list(related_images.values('id', 'title'))
    
    # اضافه کردن تصویر فعلی به لیست برای پیمایش
    all_related_images = list(GalleryImage.objects.filter(
        category=image.category, 
        is_active=True
    ).values('id', 'title').order_by('order', '-upload_date'))
    
    context = {
        'image': image,
        'related_images': related_images,
        'all_related_images_json': json.dumps(all_related_images),
        'current_image_index': next((i for i, img in enumerate(all_related_images) if img['id'] == image.id), 0),
        'total_images': len(all_related_images),
    }
    return render(request, 'gallery/detail.html', context)