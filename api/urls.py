from django.urls import path
from . import views

urlpatterns = [
    path("cats/", views.cats_api, name="cats_list"),
    path("cats/<int:cat_id>/", views.cats_api, name="cat_detail"),

    path("missions/", views.missions_api, name="missions_list"),
    path("missions/<int:mission_id>/", views.missions_api, name="mission_detail"),
]
