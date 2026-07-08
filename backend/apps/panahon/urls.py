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

]