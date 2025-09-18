from django.urls import path
from . import views

urlpatterns = [
    path("cats/", views.cats_api, name="cats_list_create"),         # GET / POST
    path("cats/<int:cat_id>/", views.cats_api, name="cats_update"), # PUT/PATCH
]
