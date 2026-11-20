from django.http import JsonResponse
from support.models import Category


def load_categories(request):
    department_id = request.GET.get('department_id')
    try:
        dept_id = int(department_id)
    except (TypeError, ValueError):
        return JsonResponse([], safe=False)

    categories = Category.objects.filter(department_id=dept_id).order_by('name')
    data = [
        {'id': cat.id, 'name': cat.name}
        for cat in categories
    ]
    return JsonResponse(data, safe=False)
