from django.template import loader
from django.shortcuts import render
from .models import Producto
import requests 
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q

# Create your views here.

def catalogo(request):
    return render(request,'Principal.html')

def Menu(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos,
    }
    return render(request, 'Menu.html',data)

def FiltroProductos(request):
    categoria = request.GET.get('categoria')
    tipo = request.GET.get('tipo')

    productos = Producto.objects.all()

    try:
        if categoria and int(categoria) > 0:
            productos = productos.filter(categoria=int(categoria))
    except (ValueError, TypeError):
        pass

    try:
        if tipo and int(tipo) > -1:
            productos = productos.filter(tipo=int(tipo))
    except (ValueError, TypeError):
        pass

    # Filtrar por nombre

    nombre = request.GET.get('nombre')
    if nombre:
        productos = productos.filter(
            Q(nombre_producto__icontains=nombre)|
            Q(id_producto__icontains=nombre)|
            Q(tipo__icontains=nombre)
        )

    mensaje = None
    if not productos.exists():
        mensaje = 'No se encontraron productos con esos filtros.'
    return render(request, 'ListaProductos.html', {'productos': productos})


def ListaProductos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos,
    }
    return render(request, 'ListaProductos.html',data)



def obtener_clima(request):
    API_KEY = '537bb6c03f595de9f255320d7af7679b'
    ciudad = request.GET.get('ciudad', 'Viña del Mar,CL')  # Puedes pasar ?ciudad=Santiago,CL

    url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es'

    try:
        respuesta = requests.get(url)
        data = respuesta.json()

        if respuesta.status_code == 200:
            clima = {
                'ciudad': data['name'],
                'temperatura': data['main']['temp'],
                'descripcion': data['weather'][0]['description'],
                'icono': data['weather'][0]['icon'],
            }
            return JsonResponse(clima)
        else:
            return JsonResponse({'error': 'No se pudo obtener el clima', 'detalle': data.get('message', '')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'Error al conectar con la API', 'detalle': str(e)}, status=500)
    

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, 'Usuario creado correctamente')
            return redirect(to='Menu')
        data['form'] = form

    return render(request,'registration/registro.html', data)

