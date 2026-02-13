from django.http import JsonResponse
from support.models import Category

def load_categories(request):
    department_id = request.GET.get('department_id')
    categories = Category.objects.filter(department_id=department_id)

    data = [
        {'id': c.id, 'name': c.name}
        for c in categories
    ]
    return JsonResponse(data, safe=False)
