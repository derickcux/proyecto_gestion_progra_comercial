import django_filters
from django import forms
from .models import Venta, Compra, Producto, Categoria

class VentaFilter(django_filters.FilterSet):
    #filtro por rango de fechas
    start_date = django_filters.DateFilter(field_name='fecha', lookup_expr='gte', label='Desde', 
                                           widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = django_filters.DateFilter(field_name='fecha', lookup_expr='lte', label='Hasta', 
                                         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    
    #filltro por cliente (buscador)
    cliente = django_filters.CharFilter(field_name='cliente__nombre', lookup_expr='icontains', label='Cliente',
                                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}))

    class Meta:
        model = Venta
        fields = ['cliente']

class CompraFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='fecha', lookup_expr='gte', label='Desde',
                                           widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = django_filters.DateFilter(field_name='fecha', lookup_expr='lte', label='Hasta',
                                         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    
    proveedor = django_filters.CharFilter(field_name='proveedor__empresa', lookup_expr='icontains', label='Proveedor',
                                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre empresa'}))

    class Meta:
        model = Compra
        fields = ['proveedor']

class InventarioFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains', label='Producto',
                                       widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar producto...'}))
    
    ccategoria = django_filters.ModelChoiceFilter(
        queryset=Categoria.objects.all(), 
        label='Categoría',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    #filtro para cantidad mínima
    min_stock = django_filters.NumberFilter(field_name='cantidad', lookup_expr='lte', label='Stock Máximo (Ver bajos)',
                                            widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Producto
        fields = ['categoria', 'nombre']