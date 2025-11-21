from django.contrib import admin
from .models import (
    Categoria, Proveedor, Producto, 
    Cliente, Venta, DetalleVenta, 
    Compra, DetalleCompra, MovimientoInventario
)

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1  #muestra una fila vacia para llenar el detalle de venta
    autocomplete_fields = ['producto']

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1 #muestra una fila vacia para llenar el detalle de compra
    autocomplete_fields = ['producto']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'contacto', 'telefono')
    search_fields = ('empresa',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo')
    search_fields = ('nombre', 'correo')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'precio_venta', 'cantidad', 'categoria')
    list_filter = ('categoria', 'proveedor') 
    search_fields = ('codigo', 'nombre')
    ordering = ['nombre'] #para mostrar en orden A-Z los productos del autocompletado en el detalle de venta y compra

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_pedido', 'fecha', 'cliente', 'estado', 'total')
    list_filter = ('estado', 'fecha')
    inlines = [DetalleVentaInline] #esto permite agregar la fila para llenar productos en la misma pagina de venta
    readonly_fields = ('fecha',)

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'fecha', 'proveedor', 'estado', 'total')
    inlines = [DetalleCompraInline] #esto permite agregar la fila para llenar productos en la misma pagina de compra
    list_filter = ('estado', 'fecha')
    readonly_fields = ('fecha',)

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'producto', 'cantidad')
    list_filter = ('tipo',)