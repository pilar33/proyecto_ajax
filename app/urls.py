from django.urls import path
from app import views

urlpatterns = [
    path('',views.inicio, name="Inicio"),
    path("productos/",views.productos,name="productos"),
    path('api/productos/', views.productos_json, name='api_productos'),
    path('agregar/productos/', views.agregar_productos, name='add_productos'),
    path("home/",views.home,name="home"),

    path("reporte/",views.generar_pdf,name="reporteProducto"),
    
]