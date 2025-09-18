from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cat

@csrf_exempt
def cats_api(request, cat_id=None):
    if request.method == "GET":
        cats = Cat.objects.all().values("id", "name", "years_of_experience", "breed", "salary")
        return JsonResponse(list(cats), safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            cat = Cat.objects.create(
                name=data["name"],
                years_of_experience=data["years_of_experience"],
                breed=data["breed"],
                salary=data["salary"]
            )
            return JsonResponse({
                "id": cat.id,
                "name": cat.name,
                "years_of_experience": cat.years_of_experience,
                "breed": cat.breed,
                "salary": cat.salary
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method in ["PUT", "PATCH"] and cat_id is not None:
        try:
            data = json.loads(request.body)
            cat = Cat.objects.get(id=cat_id)
            cat.name = data.get("name", cat.name)
            cat.breed = data.get("breed", cat.breed)
            cat.years_of_experience = data.get("years_of_experience", cat.years_of_experience)
            cat.salary = data.get("salary", cat.salary)
            cat.save()
            return JsonResponse({
                "id": cat.id,
                "name": cat.name,
                "years_of_experience": cat.years_of_experience,
                "breed": cat.breed,
                "salary": cat.salary
            })
        except Cat.DoesNotExist:
            return JsonResponse({"error": "Cat not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
