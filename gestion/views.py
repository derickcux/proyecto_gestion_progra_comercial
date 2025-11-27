from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Proveedor, Producto, Categoria, Venta, DetalleVenta, Compra, DetalleCompra, MovimientoInventario
from .forms import ClienteForm, ProveedorForm, ProductoForm, CategoriaForm, VentaForm, DetalleVentaForm, CompraForm, DetalleCompraForm
from django.db.models import Sum
from django.contrib import messages
import csv
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from .filters import VentaFilter, CompraFilter, InventarioFilter
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json
from .decorators import grupo_requerido, solo_administrador, solo_vendedor, solo_comprador, administrador_o_vendedor, administrador_o_comprador
from .pdf_generator import generar_pdf_ventas, generar_pdf_compras, generar_pdf_inventario

@login_required
def inicio(request):
    return render(request, 'inicio.html')

@solo_administrador
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/lista.html', {'clientes': clientes})

@solo_administrador
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'cliente/form.html', {'form': form})

@solo_administrador
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente) #instance carga los datos previos
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('lista_clientes') #cargar el formulario con los datos del cliente
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'cliente/form.html', {'form': form})

@solo_administrador
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')

    return redirect('lista_clientes') #cargar el formulario con los datos del cliente

@administrador_o_comprador
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor/llista.html', {'proveedores': proveedores})

@administrador_o_comprador
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor registrado correctamente.')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedor/form.html', {'form': form})

@administrador_o_comprador
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedor/form.html', {'form': form})

@administrador_o_comprador
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado correctamente.')
    return redirect('lista_proveedores')

#categorias
@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/lista.html', {'categorias': categorias})

@solo_administrador
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categoria/form.html', {'form': form})

@solo_administrador
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/form.html', {'form': form})

@solo_administrador
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
    return redirect('lista_categorias')

#productos
@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'producto/lista.html', {'productos': productos})

@solo_administrador
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto registrado exitosamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'producto/form.html', {'form': form})

@solo_administrador
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto/form.html', {'form': form})

@solo_administrador
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
    return redirect('lista_productos')

#gestion de ventas
@solo_vendedor
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha') #las mas recientes primero
    return render(request, 'venta/lista.html', {'ventas': ventas})

@solo_vendedor
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            venta.save()
            #generar numero de pedido
            venta.numero_pedido = f"PED-{venta.id:05d}"
            venta.save()
            messages.success(request, 'Venta iniciada. Ahora agrega productos.')
            return redirect('detalle_venta', id=venta.id)
    else:
        form = VentaForm()
    return render(request, 'venta/form.html', {'form': form})

@solo_vendedor
def detalle_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    #recalcular total de la venta en la pagina
    total = 0
    for d in detalles:
        total += d.subtotal()

    if request.method == 'POST':
        form = DetalleVentaForm(request.POST)
        if form.is_valid():
            producto_seleccionado = form.cleaned_data['producto']
            cantidad_ingresada = form.cleaned_data['cantidad']

            #buscar si el producto ya existe en los detalles de la venta
            detalle_existente = DetalleVenta.objects.filter(venta=venta, producto=producto_seleccionado).first()

            if detalle_existente:
                #si existe, solo sumar la cantidad y actualizar precio
                detalle_existente.cantidad += cantidad_ingresada
                detalle_existente.precio_unitario = producto_seleccionado.precio_venta
                detalle_existente.save()
                messages.success(request, 'Cantidad actualizada en el pedido.')
            else:
                #sino existe, crear uno nuevo
                detalle = form.save(commit=False)
                detalle.venta = venta
                detalle.precio_unitario = producto_seleccionado.precio_venta
                detalle.save()
                messages.success(request, 'Producto agregado.')

            #recalcular total de la cabecera (venta)
            #esto es importante hacerlo después de guardar/actualizar
            nuevos_detalles = DetalleVenta.objects.filter(venta=venta)
            nuevo_total = 0
            for d in nuevos_detalles:
                nuevo_total += d.subtotal()
            venta.total = nuevo_total
            venta.save()

            return redirect('detalle_venta', id=id)
    else:
        form = DetalleVentaForm()

    return render(request, 'venta/detalle.html', {
        'venta': venta,
        'detalles': detalles,
        'form': form,
        'total': total
    })

@solo_vendedor
def finalizar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)

    if venta.estado == 'pendiente':
        detalles = DetalleVenta.objects.filter(venta=venta)

        # Validación de stock... (tu código existente sigue igual)
        for detalle in detalles:
            if detalle.producto.cantidad < detalle.cantidad:
                messages.error(request, f"Error: No hay suficiente stock...")
                return redirect('detalle_venta', id=id)

        #restar inventario y registrar movimiento
        for detalle in detalles:
            producto = detalle.producto
            producto.cantidad -= detalle.cantidad
            producto.save()

            MovimientoInventario.objects.create(
                tipo='salida',
                producto=producto,
                cantidad=detalle.cantidad,
                venta_asociada=venta
            )
            # --------------------------------------

        venta.estado = 'completado'
        venta.save()
        messages.success(request, 'Venta finalizada, stock actualizado y movimiento registrado.')

    return redirect('lista_ventas')

@solo_vendedor
def eliminar_detalle_venta(request, id):
    detalle = get_object_or_404(DetalleVenta, id=id)
    venta = detalle.venta #guardar la referencia de la venta antes de eliminar
    detalle.delete()

    #recalcular el total de la venta
    detalles_restantes = DetalleVenta.objects.filter(venta=venta)
    nuevo_total = 0
    for d in detalles_restantes:
        nuevo_total += d.subtotal()

    venta.total = nuevo_total
    venta.save()

    messages.warning(request, 'Producto eliminado. Total actualizado.')
    return redirect('detalle_venta', id=venta.id)

@solo_vendedor
def cancelar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)

    #solo se permite cancelar si no está completada
    if venta.estado == 'pendiente':
        venta.estado = 'cancelado'
        venta.save()
        messages.error(request, 'Venta cancelada exitosamente.')

    return redirect('lista_ventas')

#gestion de compras
@solo_comprador
def lista_compras(request):
    compras = Compra.objects.all().order_by('-fecha')
    return render(request, 'compra/lista.html', {'compras': compras})

@solo_comprador
def crear_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.save()
            compra.numero_orden = f"ORD-{compra.id:05d}"
            compra.save()
            messages.success(request, 'Orden de compra iniciada.')
            return redirect('detalle_compra', id=compra.id)
    else:
        form = CompraForm()
    return render(request, 'compra/form.html', {'form': form})

@solo_comprador
def detalle_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    detalles = DetalleCompra.objects.filter(compra=compra)

    #recalcular en total en la pagina
    total = 0
    for d in detalles:
        total += (d.cantidad * d.costo_unitario)

    if request.method == 'POST':
        form = DetalleCompraForm(request.POST)

        #al recibir datos, se filtra para validar que no se mande un producto de otro proveedor
        form.fields['producto'].queryset = Producto.objects.filter(proveedor=compra.proveedor)

        if form.is_valid():
            producto_seleccionado = form.cleaned_data['producto']
            cantidad_ingresada = form.cleaned_data['cantidad']
            costo_ingresado = form.cleaned_data['costo_unitario']

            detalle_existente = DetalleCompra.objects.filter(compra=compra, producto=producto_seleccionado).first()

            if detalle_existente:
                detalle_existente.cantidad += cantidad_ingresada
                detalle_existente.costo_unitario = costo_ingresado
                detalle_existente.save()
                messages.success(request, 'Cantidad actualizada en la orden.')
            else:
                detalle = form.save(commit=False)
                detalle.compra = compra
                detalle.save()
                messages.success(request, 'Producto agregado a la orden.')

            #Actualizar total
            nuevos_detalles = DetalleCompra.objects.filter(compra=compra)
            nuevo_total = 0
            for d in nuevos_detalles:
                nuevo_total += (d.cantidad * d.costo_unitario)
            compra.total = nuevo_total
            compra.save()

            return redirect('detalle_compra', id=id)
    else:
        form = DetalleCompraForm()

    form.fields['producto'].queryset = Producto.objects.filter(proveedor=compra.proveedor)

    return render(request, 'compra/detalle.html', {
        'compra': compra,
        'detalles': detalles,
        'form': form,
        'total': total
    })

@solo_comprador
def finalizar_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    if compra.estado == 'pendiente':
        compra.estado = 'recibida'
        compra.save()

        detalles = DetalleCompra.objects.filter(compra=compra)
        for detalle in detalles:
            producto = detalle.producto
            producto.cantidad += detalle.cantidad
            producto.precio_compra = detalle.costo_unitario
            producto.save()

            #guardar en el historial de movimientos
            MovimientoInventario.objects.create(
                tipo='entrada',
                producto=producto,
                cantidad=detalle.cantidad,
                compra_asociada=compra
            )
            # --------------------------------------

        messages.success(request, 'Compra recibida y movimientos registrados.')
    return redirect('lista_compras')

@solo_comprador
def eliminar_detalle_compra(request, id):
    detalle = get_object_or_404(DetalleCompra, id=id)
    compra = detalle.compra
    detalle.delete()

    # Recalcular total
    detalles_restantes = DetalleCompra.objects.filter(compra=compra)
    nuevo_total = 0
    for d in detalles_restantes:
        nuevo_total += (d.cantidad * d.costo_unitario)
    compra.total = nuevo_total
    compra.save()

    messages.warning(request, 'Producto eliminado de la orden.')
    return redirect('detalle_compra', id=compra.id)

@solo_comprador
def cancelar_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    if compra.estado == 'pendiente':
        compra.estado = 'cancelada'
        compra.save()
        messages.error(request, 'Orden de compra cancelada.')
    return redirect('lista_compras')

#reportes
@login_required
def reporte_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    filtro = VentaFilter(request.GET, queryset=ventas)
    data = filtro.qs # Datos ya filtrados

    # EXPORTAR A CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ventas.csv"'
        writer = csv.writer(response)
        writer.writerow(['Pedido', 'Fecha', 'Cliente', 'Total', 'Estado']) # Encabezados
        for v in data:
            writer.writerow([v.numero_pedido, v.fecha.strftime("%d/%m/%Y"), v.cliente.nombre, v.total, v.get_estado_display()])
        return response

    # EXPORTAR A PDF (usando ReportLab, compatible con Railway)
    if request.GET.get('export') == 'pdf':
        return generar_pdf_ventas(data, 'Reporte de Ventas')

    return render(request, 'reportes/ventas.html', {'filtro': filtro, 'ventas': data})

@login_required
def reporte_compras(request):
    compras = Compra.objects.all().order_by('-fecha')
    filtro = CompraFilter(request.GET, queryset=compras)
    data = filtro.qs

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="compras.csv"'
        writer = csv.writer(response)
        writer.writerow(['Orden', 'Fecha', 'Proveedor', 'Total', 'Estado'])
        for c in data:
            writer.writerow([c.numero_orden, c.fecha.strftime("%d/%m/%Y"), c.proveedor.empresa, c.total, c.get_estado_display()])
        return response

    # EXPORTAR A PDF (usando ReportLab, compatible con Railway)
    if request.GET.get('export') == 'pdf':
        return generar_pdf_compras(data, 'Reporte de Compras')

    return render(request, 'reportes/compras.html', {'filtro': filtro, 'compras': data})

@login_required
def reporte_inventario(request):
    productos = Producto.objects.all().order_by('nombre')
    filtro = InventarioFilter(request.GET, queryset=productos)
    data = filtro.qs

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventario.csv"'
        writer = csv.writer(response)
        writer.writerow(['Código', 'Producto', 'Categoría', 'Stock', 'Precio Venta'])
        for p in data:
            writer.writerow([p.codigo, p.nombre, p.categoria.nombre, p.cantidad, p.precio_venta])
        return response

    # EXPORTAR A PDF (usando ReportLab, compatible con Railway)
    if request.GET.get('export') == 'pdf':
        return generar_pdf_inventario(data, 'Reporte de Inventario')

    return render(request, 'reportes/inventario.html', {'filtro': filtro, 'productos': data})

#movimientos de inventario
@login_required
def movimientos_inventario(request):
    movimientos = MovimientoInventario.objects.all().order_by('-fecha')
    return render(request, 'reportes/movimientos.html', {'movimientos': movimientos})

#inicio
@login_required
def dashboard(request):
    #ventas por mes (grafico de barras)
    ventas_por_mes = Venta.objects.annotate(mes=TruncMonth('fecha'))\
        .values('mes')\
        .annotate(total_ventas=Sum('total'))\
        .order_by('mes')

    meses_label = []
    montos_data = []
    for v in ventas_por_mes:
        meses_label.append(v['mes'].strftime("%B %Y"))
        montos_data.append(float(v['total_ventas']))

    #productos más vendidos (grafico de pastel)
    productos_top = DetalleVenta.objects.values('producto__nombre')\
        .annotate(cantidad_total=Sum('cantidad'))\
        .order_by('-cantidad_total')[:5]

    prod_labels = []
    prod_data = []
    for p in productos_top:
        prod_labels.append(p['producto__nombre'])
        prod_data.append(p['cantidad_total'])

    context = {
        'meses_label': json.dumps(meses_label),
        'montos_data': json.dumps(montos_data),
        'prod_labels': json.dumps(prod_labels),
        'prod_data': json.dumps(prod_data),
    }
    return render(request, 'dashboard.html', context)

@login_required
def obtener_precio_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({
            'precio_compra': float(producto.precio_compra),
            'success': True
        })
    except Producto.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Producto no encontrado'
        }, status=404)