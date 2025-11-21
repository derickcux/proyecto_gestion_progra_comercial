from django import forms
from .models import Cliente, Proveedor, Producto, Venta, Compra, Categoria, DetalleVenta, DetalleCompra

#formularios de catalogos

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

#formularios de transacciones
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente'] # El usuario solo elige cliente, la fecha es auto y el estado inicial es pendiente

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'costo_unitario']
