from django.urls import path
from app import views

urlpatterns = [
    path('',views.inicio, name="Inicio"),
    path("productos/",views.productos,name="productos"),
]