from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),
    path('Menu/', views.Menu, name='Menu'),
    path('ListaProductos/', views.ListaProductos, name='ListaProductos'),
    path('FiltroProductos/', views.FiltroProductos, name='FiltroProductos'),
]