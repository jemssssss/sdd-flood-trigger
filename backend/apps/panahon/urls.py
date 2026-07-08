from django.urls import path
from . import views

urlpatterns = [

    path(
        "synoptic",
        views.synoptic,
        name="synoptic",
    ),

    path(
        "aws",
        views.aws,
        name="aws",
    ),

    path(
        "point",
        views.point,
        name="point",
    ),

    path(
        "footprints",
        views.footprints,
        name="footprints",
    ),

]