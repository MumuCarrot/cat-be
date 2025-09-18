from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import get_cat_breeds
from .models import Cat, Mission, Target

@csrf_exempt
def cats_api(request, cat_id=None):
    try:
        if request.method == "GET" and cat_id is not None:
            cat = Cat.objects.get(id=cat_id)
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

        elif request.method == "GET":
            cats = Cat.objects.all().values("id", "name", "years_of_experience", "breed", "salary")
            return JsonResponse(list(cats), safe=False)

        elif request.method == "POST":
            try:
                data = json.loads(request.body)
                valid_breeds = get_cat_breeds()

                if data["breed"] not in valid_breeds:
                    return JsonResponse({"error": "Invalid breed"}, status=400)

                cat = Cat.objects.create(
                    name=data["name"],
                    years_of_experience=data["years_of_experience"],
                    breed=data["breed"],
                    salary=data["salary"],
                )
                return JsonResponse({"id": cat.id, "message": "Cat created"}, status=201)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

        elif request.method in ["PUT", "PATCH"] and cat_id is not None:
            data = json.loads(request.body)
            valid_breeds = get_cat_breeds()

            if data["breed"] not in valid_breeds:
                return JsonResponse({"error": "Invalid breed"}, status=400)

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


@csrf_exempt
def missions_api(request, mission_id=None):
    try:
        if request.method == "GET":
            if mission_id:
                mission = Mission.objects.get(id=mission_id)
                return JsonResponse({
                    "id": mission.id,
                    "name": mission.name,
                    "description": mission.description,
                    "is_completed": mission.is_completed,
                    "cat": mission.cat.id if mission.cat else None,
                    "targets": list(mission.targets.all().values("id", "name", "country", "notes", "is_completed")),
                })
            else:
                missions = Mission.objects.all()
                return JsonResponse([
                    {
                        "id": m.id,
                        "name": m.name,
                        "description": m.description,
                        "is_completed": m.is_completed,
                        "cat": m.cat.id if m.cat else None,
                        "targets": list(m.targets.all().values("id", "name", "country", "notes", "is_completed")),
                    }
                    for m in missions
                ], safe=False)

        elif request.method == "POST":
            data = json.loads(request.body)
            mission = Mission.objects.create(
                name=data.get("name", ""),
                description=data.get("description", ""),
                is_completed=bool(data.get("is_completed", False)),
                cat=Cat.objects.get(id=data["cat"]) if data.get("cat") else None
            )
            targets_data = data.get("targets", [])
            for t in targets_data:
                Target.objects.create(
                    mission=mission,
                    name=t.get("name", ""),
                    country=t.get("country", ""),
                    notes=t.get("notes", ""),
                    is_completed=bool(t.get("is_completed", False))
                )
            return JsonResponse({"id": mission.id}, status=201)

        elif request.method == "DELETE" and mission_id:
            mission = Mission.objects.get(id=mission_id)
            if mission.cat:
                return JsonResponse({"error": "Cannot delete mission assigned to a cat"}, status=400)
            mission.delete()
            return JsonResponse({"success": True})

        elif request.method == "PUT" and mission_id:
            data = json.loads(request.body)
            mission = Mission.objects.get(id=mission_id)

            if mission.is_completed:
                return JsonResponse({"error": "Cannot update a completed mission"}, status=400)

            mission.name = data.get("name", mission.name)
            mission.description = data.get("description", mission.description)
            mission.save()

            for t_data in data.get("targets", []):
                target = Target.objects.get(id=t_data["id"], mission=mission)
                if t_data.get("is_completed"):
                    target.is_completed = True
                if not mission.is_completed and not target.is_completed:
                    target.notes = t_data.get("notes", target.notes)
                target.save()

            return JsonResponse({"success": True})

        elif request.method == "PATCH" and mission_id:
            data = json.loads(request.body)
            mission = Mission.objects.get(id=mission_id)
            if "cat" in data:
                mission.cat = Cat.objects.get(id=data["cat"])
                mission.save()
            return JsonResponse({"success": True})

        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)

    except Mission.DoesNotExist:
        return JsonResponse({"error": "Mission not found"}, status=404)
    except Target.DoesNotExist:
        return JsonResponse({"error": "Target not found"}, status=404)
    except Cat.DoesNotExist:
        return JsonResponse({"error": "Cat not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
