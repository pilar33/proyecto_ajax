from django.shortcuts import render
from app.models import producto
# Create your views here.
def inicio(request):
    return render(request, "index.html")

def productos(request):
    productos = producto.objects.all()
    return render(request, "productos.html", {"productos":"productos"})
