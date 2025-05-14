from django.template import loader
from django.shortcuts import render
from .models import Producto

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

    productos = Producto.objects.all()

    try:
        if categoria and int(categoria) > 0:
            productos = productos.filter(categoria=int(categoria))
    except (ValueError, TypeError):
        pass
    return render(request, 'ListaProductos.html', {'productos': productos})


def ListaProductos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos,
    }
    return render(request, 'ListaProductos.html',data)