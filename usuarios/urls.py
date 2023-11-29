from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login),
    path('registro/', views.registro),
    path('camisetas/', views.catcamiseta),
    path('estampas/',views.catestampa),
    path('usuarioID/', views.usuarioID),
    path('factura/', views.generarFactura),
    path('catalogoCamisetas/', views.actualizarCantidad),
    path('artista/', views.actualizarVentas),
    path('nuevaEstampa/', views.nuevaEstampa),
    path('actualizarEstampa/', views.actualizarEstampa),
    path('ventasArtista/', views.ventasArtista)
]