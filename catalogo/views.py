from django.template import loader
from django.shortcuts import render
from catalogo.Carrito import Carrito
from .models import Producto
import requests 
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from .decorator import solo_ferromax

# Create your views here.

def catalogo(request):
    return render(request,'Principal.html')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0
    for item in carrito.values():
        total += float(item['precio']) * int(item['cantidad'])
    context = {
        'total': total,
        'carrito': carrito,
    }
    return render(request, 'carrito.html', context)

def ver_carrito1(request):
    carrito = request.session.get('carrito', {})
    total = 0
    for item in carrito.values():
        total += float(item['precio']) * int(item['cantidad'])
    context = {
        'total': total,
        'carrito': carrito,
    }
    return render(request, 'ListaProductos.html', context)

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
    carrito = request.session.get('carrito', {})
    total = 0
    for item in carrito.values():
        total += float(item['precio']) * int(item['cantidad'])
    context = {
        'productos': productos,
        'carrito': carrito,
        'total': total,
    }
    return render(request, 'ListaProductos.html', context)



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

def agregar(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.agregar_producto(producto)
    return redirect('ListaProductos')

def sumar(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.agregar_producto(producto)
    return redirect('carrito')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.eliminar(producto)
    carrito_session = request.session.get('carrito', {})
    total = 0
    for item in carrito_session.values():
        total += float(item['precio']) * int(item['cantidad'])
    context = {
        'total': total,
        'carrito': carrito_session,
    }
    return render(request, 'carrito.html', context)
    
def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto=producto_id)
    carrito.restar_producto(producto)
    # Recalcular el total
    carrito_session = request.session.get('carrito', {})
    total = 0
    for item in carrito_session.values():
        total += float(item['precio']) * int(item['cantidad'])
    context = {
        'total': total,
        'carrito': carrito_session,
    }
    return render(request, 'carrito.html', context)

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return render(request,'carrito.html')


def pago_exitoso(request):
    carrito = request.session.get('carrito', {})
    for key, item in carrito.items():
        try:
            producto = Producto.objects.get(pk=key)
            producto.stock -= int(item['cantidad'])
            producto.save()
        except Producto.DoesNotExist:
            pass 
    request.session['carrito'] = {}
    messages.success(request, '¡Pago realizado con éxito! Gracias por tu compra.')
    return redirect('ListaProductos')



@solo_ferromax
def agregar_stock(request):
    if request.method != 'POST':
        return render(request, 'agregar_stock.html')
    else:
        nombre_producto = request.POST['nombre_producto']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        tipo = request.POST['tipo']
        categoria = request.POST['categoria']
        stock = request.POST['stock']
        imagen = request.FILES.get('imagen')

        try:
            precio = int(precio)
            tipo = int(tipo)
            categoria = int(categoria) if categoria else None
            stock = int(stock)
        except Exception as e:
            return render(request, 'agregar_stock.html', {'mensaje': 'Datos inválidos.'})

        obj = Producto.objects.create(
            nombre_producto=nombre_producto,
            descripcion=descripcion,
            precio=precio,
            tipo=tipo,
            categoria=categoria,
            stock=stock,
            imagen=imagen
        )
        obj.save()
        return render(request, 'ListaProductos.html', {'mensaje': 'Producto agregado correctamente.'})