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
]