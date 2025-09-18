from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cat

@csrf_exempt
def cats_api(request, cat_id=None):
    try:
        if request.method == "GET":
            cats = Cat.objects.all().values("id", "name", "years_of_experience", "breed", "salary")
            return JsonResponse(list(cats), safe=False)

        elif request.method == "POST":
            data = json.loads(request.body)
            cat = Cat.objects.create(
                name=data.get("name", ""),
                breed=data.get("breed", ""),
                years_of_experience=int(data.get("years_of_experience", 0)),
                salary=int(data.get("salary", 0))
            )
            return JsonResponse({
                "id": cat.id,
                "name": cat.name,
                "breed": cat.breed,
                "years_of_experience": cat.years_of_experience,
                "salary": cat.salary
            })

        elif request.method in ["PUT", "PATCH"] and cat_id is not None:
            data = json.loads(request.body)
            cat = Cat.objects.get(id=cat_id)
            cat.name = data.get("name", cat.name)
            cat.breed = data.get("breed", cat.breed)
            cat.years_of_experience = int(data.get("years_of_experience", cat.years_of_experience))
            cat.salary = int(data.get("salary", cat.salary))
            cat.save()
            return JsonResponse({
                "id": cat.id,
                "name": cat.name,
                "breed": cat.breed,
                "years_of_experience": cat.years_of_experience,
                "salary": cat.salary
            })

        elif request.method == "DELETE" and cat_id is not None:
            cat = Cat.objects.get(id=cat_id)
            cat.delete()
            return JsonResponse({"success": True})

        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)

    except Cat.DoesNotExist:
        return JsonResponse({"error": "Cat not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
