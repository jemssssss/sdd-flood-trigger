from django.urls import path
from . import views

urlpatterns = [ 
    path("point", views.point, name="ecmwf_point"),
]