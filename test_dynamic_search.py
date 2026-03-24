from django.apps import apps
from django.db.models import CharField, TextField, Q
import sys

def test_search(query):
    all_results = []
    excluded_apps = ['admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles', 'axes', 'daphne', 'modeltranslation', 'crispy_forms', 'crispy_bootstrap5', 'channels']
    
    for model in apps.get_models():
        if model._meta.app_label in excluded_apps:
            continue
            
        if not hasattr(model, 'get_absolute_url'):
            continue
            
        # exclude proxy models to avoid duplicate results from base models
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
                
            results = queryset.filter(q_objects).distinct()[:5]
            
            for obj in results:
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
                
                all_results.append({
                    'title': title,
                    'category': category,
                    'department': department,
                    'url': url,
                })
        except Exception as e:
            pass
            
    return all_results

q = sys.argv[1] if len(sys.argv) > 1 else 'bilgisayar'
res = test_search(q)
print(f"Found {len(res)} results for '{q}'")
for r in res[:10]:
    print(r)
