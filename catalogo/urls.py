from django.urls import path
from . import views
from .views import obtener_clima

urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),
    path('', views.Menu, name='Menu'),
    path('ListaProductos/', views.ListaProductos, name='ListaProductos'),
    path('FiltroProductos/', views.FiltroProductos, name='FiltroProductos'),
    path('registro/', views.registro, name='registro'),
    path('api/clima/', obtener_clima),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('agregar/<int:producto_id>/', views.agregar, name='agregar'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar'),
    path('restar/<int:producto_id>/', views.restar_producto, name='restar'),
    path('limpiar/', views.limpiar_carrito, name='limpiar'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
]
