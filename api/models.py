from django.db import models

class Cat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    breed = models.CharField(max_length=100)
    salary = models.IntegerField()

    def __str__(self):
        return self.name


class Mission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    cat = models.ForeignKey(Cat, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.country})"
