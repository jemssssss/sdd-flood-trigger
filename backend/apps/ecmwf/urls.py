from django.urls import path
from . import views

urlpatterns = [

    path(
        "footprints",
        views.footprints,
        name="ecmwf_footprints",
    ),

]