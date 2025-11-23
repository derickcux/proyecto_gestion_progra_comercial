from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Cliente, Proveedor, Categoria, Producto, Venta, Compra, MovimientoInventario
from .serializers import (
    ClienteSerializer, ProveedorSerializer, CategoriaSerializer, 
    ProductoSerializer, VentaSerializer, CompraSerializer, MovimientoSerializer
)

#viewsets (controladores automaticos de la API REST)
class ClienteViewSet(ReadOnlyModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProveedorViewSet(ReadOnlyModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class CategoriaViewSet(ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(ReadOnlyModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class VentaViewSet(ReadOnlyModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha')
    serializer_class = VentaSerializer

class CompraViewSet(ReadOnlyModelViewSet):
    queryset = Compra.objects.all().order_by('-fecha')
    serializer_class = CompraSerializer

class MovimientoViewSet(ReadOnlyModelViewSet):
    queryset = MovimientoInventario.objects.all().order_by('-fecha')
    serializer_class = MovimientoSerializer