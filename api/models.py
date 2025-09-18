from django.db import models

class Cat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    breed = models.CharField(max_length=100)
    salary = models.IntegerField()

    def __str__(self):
        return self.name
