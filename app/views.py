from django.shortcuts import render, HttpResponse
from app.models import producto
from django.http import JsonResponse
from .forms import ProductoForm
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

# /*para el reporte*/
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

# para el dashboard
import pandas as pd

# dashboard con plotly
from plotly.offline import plot
import plotly.graph_objs as go

# Create your views here.
def inicio(request):
    return render(request, "index.html")

#@login_required
def home(request):
    # if request.user.is_authenticated:
    #     print(f"Usuario autenticado: {request.user}")
    # else:
    #     print("Usuario no autenticado")
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


# vista para generar pdf
def generar_pdf(request):
    datos = producto.objects.all()
    lista = [[obj.nombre, obj.descripcion] for obj in datos]  # Ajustar campos
    encabezados = ["Nombre Producto", "Descripcion"]
    template = get_template("reporte.html")
    context = {"titulo": "Mi Reporte", "datos": lista, "encabezados": encabezados}
    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=reporte.pdf"
    pisa.CreatePDF(html, dest=response)
    return response
      
# para el dashboard de productos
def dashboard_productos(request):
    # 1. Consultar todos los productos desde la base de datos
    #    .values(...) devuelve diccionarios con solo los campos indicados
    qs = producto.objects.all().values('idproducto','nombre','descripcion','iEstado')

    # 2. Convertir el QuerySet a un DataFrame de Pandas
    df = pd.DataFrame.from_records(qs)

    # 3. Si el DataFrame está vacío (no hay productos), devolver la plantilla
    #    con mensajes predefinidos
    if df.empty:
        return render(request, 'dashboard.html', {
            'tabla_activos': '<p class="text-muted">No hay datos.</p>',
            'tabla_letras': '',
            'prom_len': 0,
        })

    # 4. Reemplazar valores nulos en la columna 'descripcion' por cadenas vacías
    df['descripcion'] = df['descripcion'].fillna('')

    # 5. Calcular la longitud de cada descripción y guardarla en una nueva columna
    df['len_desc'] = df['descripcion'].astype(str).str.len()

    # 6. Crear una columna con la primera letra del nombre (en mayúscula)
    df['letra'] = df['nombre'].astype(str).str[0].str.upper()

    # 7. Agrupar por estado (iEstado) y contar cuántos productos hay en cada uno
    activos = (
        df.groupby('iEstado')['idproducto']  # agrupar por iEstado
          .count()                           # contar cantidad de registros
          .reset_index(name='Cantidad')      # volver a DataFrame con columna 'Cantidad'
          .sort_values('iEstado')            # ordenar por iEstado
    )

    # 8. Calcular la longitud promedio de las descripciones
    prom_len = round(df['len_desc'].mean(), 2)

    # 9. Agrupar por la primera letra del nombre y contar productos en cada grupo
    por_letra = (
        df.groupby('letra')['idproducto']
          .count()
          .reset_index(name='Cantidad')
          .sort_values(['Cantidad','letra'], ascending=[False, True])  # ordenar por cantidad desc, luego letra
    )

    # 10. Convertir los DataFrames de métricas a tablas HTML con clases de Bootstrap
    tabla_activos = activos.to_html(classes='table table-bordered table-striped table-sm', index=False)
    tabla_letras  = por_letra.to_html(classes='table table-bordered table-striped table-sm', index=False)

    # 11. Renderizar la plantilla 'dashboard.html' enviando las tablas e indicadores
    return render(request, 'dashboard.html', {
        'tabla_activos': tabla_activos,
        'tabla_letras': tabla_letras,
        'prom_len': prom_len,
    })

def dashboard_productos_plotly(request):
    # 1. Consultar todos los productos de la base de datos
    #    .values(...) devuelve solo los campos especificados
    qs = producto.objects.all().values('idproducto','nombre','descripcion','iEstado')

    # 2. Convertir el QuerySet en un DataFrame de Pandas
    df = pd.DataFrame.from_records(qs)

    # 3. Si no hay registros, renderizar la plantilla con mensajes de "sin datos"
    if df.empty:
        return render(request, 'dashboard_plotly.html', {
            'tabla_activos': '<p class="text-muted">No hay datos.</p>',
            'tabla_letras': '',
            'prom_len': 0,
            'plot_div': '<div class="text-muted">Sin datos para graficar.</div>'
        })

    # 4. Reemplazar valores nulos en la descripción con cadena vacía
    df['descripcion'] = df['descripcion'].fillna('')

    # 5. Crear columna con la longitud de cada descripción
    df['len_desc'] = df['descripcion'].astype(str).str.len()

    # 6. Crear columna con la primera letra del nombre, en mayúscula
    df['letra'] = df['nombre'].astype(str).str[0].str.upper()

    # 7. Agrupar por estado (iEstado) y contar productos en cada grupo
    activos = (
        df.groupby('iEstado')['idproducto']   # agrupar por estado
          .count()                            # contar cantidad de productos
          .reset_index(name='Cantidad')       # convertir a DataFrame con columna 'Cantidad'
          .sort_values('iEstado')             # ordenar por iEstado
    )

    # 8. Calcular la longitud promedio de las descripciones
    prom_len = round(df['len_desc'].mean(), 2)

    # 9. Agrupar por primera letra del nombre y contar cuántos productos hay en cada letra
    por_letra = (
        df.groupby('letra')['idproducto']
          .count()
          .reset_index(name='Cantidad')
          .sort_values(['Cantidad','letra'], ascending=[False, True])  # ordenar por cantidad desc y luego por letra
    )

    # 10. Convertir los DataFrames en tablas HTML con estilos Bootstrap
    tabla_activos = activos.to_html(classes='table table-bordered table-striped table-sm', index=False)
    tabla_letras  = por_letra.to_html(classes='table table-bordered table-striped table-sm', index=False)

    # 11. Preparar los datos para el gráfico con Plotly (conteo por estado)
    x_vals = activos['iEstado'].astype(str)  # convertir valores de estado a texto ("0", "1")
    y_vals = activos['Cantidad']             # cantidades por estado

    # 12. Crear gráfico de barras con Plotly
    fig = go.Figure(data=[go.Bar(x=x_vals, y=y_vals)])
    fig.update_layout(
        title='Productos por estado (iEstado)',
        xaxis_title='iEstado (0=inactivo, 1=activo)',
        yaxis_title='Cantidad',
        margin=dict(l=10, r=10, t=40, b=10),
        height=420
    )

    # 13. Generar el gráfico como HTML embebido (div con JS incluido)
    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    # 14. Renderizar la plantilla con las tablas, el promedio y el gráfico
    return render(request, 'dashboard_plotly.html', {
        'tabla_activos': tabla_activos,
        'tabla_letras': tabla_letras,
        'prom_len': prom_len,
        'plot_div': plot_div
    })


