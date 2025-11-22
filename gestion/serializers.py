from rest_framework import serializers
from .models import Cliente, Proveedor, Categoria, Producto, Venta, Compra, DetalleVenta, DetalleCompra

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # Campos extra para mostrar nombres
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.empresa')

    class Meta:
        model = Producto
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario']

class DetalleCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = DetalleCompra
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'costo_unitario']

class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre')
    #se agregan los detalles de la venta
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.empresa')
    
    #se agregan los detalles de la compra
    detalles = DetalleCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = '__all__'