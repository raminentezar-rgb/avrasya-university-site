from django.apps import apps
from django.db.models import CharField, TextField

models_with_url = []
for model in apps.get_models():
    if hasattr(model, 'get_absolute_url'):
        models_with_url.append(model)

print(f"Total models with get_absolute_url: {len(models_with_url)}")
for m in models_with_url[:10]:
    print(m.__name__, m._meta.app_label)
