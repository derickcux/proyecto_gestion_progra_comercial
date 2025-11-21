from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    #rutas de clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    #rutas de proveedores
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/nuevo/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    #categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),

    #productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    #ventas
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/nueva/', views.crear_venta, name='crear_venta'),
    path('ventas/detalle/<int:id>/', views.detalle_venta, name='detalle_venta'),
    path('ventas/finalizar/<int:id>/', views.finalizar_venta, name='finalizar_venta'),
    path('ventas/eliminar-item/<int:id>/', views.eliminar_detalle_venta, name='eliminar_detalle_venta'),
    path('ventas/cancelar/<int:id>/', views.cancelar_venta, name='cancelar_venta'),

    #compras
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/nueva/', views.crear_compra, name='crear_compra'),
    path('compras/detalle/<int:id>/', views.detalle_compra, name='detalle_compra'),
    path('compras/finalizar/<int:id>/', views.finalizar_compra, name='finalizar_compra'),
    path('compras/eliminar-item/<int:id>/', views.eliminar_detalle_compra, name='eliminar_detalle_compra'),
    path('compras/cancelar/<int:id>/', views.cancelar_compra, name='cancelar_compra'),

    #reportes
    path('reportes/ventas/', views.reporte_ventas, name='reporte_ventas'),
    path('reportes/compras/', views.reporte_compras, name='reporte_compras'),
    path('reportes/inventario/', views.reporte_inventario, name='reporte_inventario'),

    #dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]