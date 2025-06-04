from django.shortcuts import render, HttpResponse
from app.models import producto
from django.http import JsonResponse
from .forms import ProductoForm
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import render_to_string
# Create your views here.
def inicio(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def productos(request):
    return render(request, 'productos.html')

def productos_json(request):
    productos = list(producto.objects.values("nombre", "descripcion", "iEstado"))
    return JsonResponse({'data': productos})


# @xframe_options_exempt
# def agregar_productos(request):
#     if request.method == 'POST':
#         form = ProductoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True, 'message': 'Producto agregado exitosamente.'})
#         else:
#             html_form = render_to_string('agregar.html', {'form': form}, request=request)
#             return JsonResponse({'success': False, 'form_html': html_form}, status=400)
#     else:
#         form = ProductoForm()
#         html_form = render_to_string('agregar.html', {'form': form}, request=request)
#         return JsonResponse({'success': True, 'form_html': html_form})

@xframe_options_exempt
def agregar_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            # Avisar al iframe que debe cerrarse:
            return HttpResponse(
                "<script>window.parent.postMessage({action: 'closeBootbox'}, '*');</script>"
            )
    else:
        form = ProductoForm()
    return render(request, 'agregar.html', {'form': form})
      
