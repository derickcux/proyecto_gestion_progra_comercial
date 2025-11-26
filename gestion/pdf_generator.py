"""
Generador de PDFs usando ReportLab (compatible con Railway).
Esta es la solución recomendada para producción en Railway.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime


class PDFReporter:
    """Generador de reportes en PDF con ReportLab."""

    def __init__(self, titulo, tipo_reporte):
        self.titulo = titulo
        self.tipo_reporte = tipo_reporte
        self.buffer = BytesIO()
        self.pagesize = A4
        self.styles = getSampleStyleSheet()

    def _get_title_style(self):
        """Retorna el estilo personalizado para títulos."""
        return ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
        )

    def _get_fecha_style(self):
        """Retorna el estilo personalizado para fechas."""
        return ParagraphStyle(
            'Fecha',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey
        )

    def _crear_tabla(self, table_data, col_widths):
        """Crea una tabla con estilos aplicados."""
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table

    def generar_reporte_ventas(self, data):
        """Genera PDF de reporte de ventas."""
        doc = SimpleDocTemplate(self.buffer, pagesize=self.pagesize)
        elements = []

        # Título
        elements.append(Paragraph(self.titulo, self._get_title_style()))
        elements.append(Spacer(1, 0.3*inch))

        # Fecha de generación
        elements.append(Paragraph(
            f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self._get_fecha_style()
        ))
        elements.append(Spacer(1, 0.2*inch))

        # Tabla de datos
        table_data = [['Pedido', 'Fecha', 'Cliente', 'Total', 'Estado']]

        total_ventas = 0
        for venta in data:
            table_data.append([
                venta.numero_pedido,
                venta.fecha.strftime("%d/%m/%Y"),
                venta.cliente.nombre,
                f"${venta.total:,.2f}",
                venta.get_estado_display()
            ])
            total_ventas += venta.total

        # Agregar fila de total
        table_data.append(['', '', 'TOTAL:', f"${total_ventas:,.2f}", ''])

        # Crear tabla
        table = self._crear_tabla(table_data, [1.2*inch, 1.2*inch, 2*inch, 1*inch, 1.2*inch])
        elements.append(table)

        # Generar PDF
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer

    def generar_reporte_compras(self, data):
        """Genera PDF de reporte de compras."""
        doc = SimpleDocTemplate(self.buffer, pagesize=self.pagesize)
        elements = []

        # Título
        elements.append(Paragraph(self.titulo, self._get_title_style()))
        elements.append(Spacer(1, 0.3*inch))

        # Fecha de generación
        elements.append(Paragraph(
            f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self._get_fecha_style()
        ))
        elements.append(Spacer(1, 0.2*inch))

        # Tabla de datos
        table_data = [['Orden', 'Fecha', 'Proveedor', 'Total', 'Estado']]

        total_compras = 0
        for compra in data:
            table_data.append([
                compra.numero_orden,
                compra.fecha.strftime("%d/%m/%Y"),
                compra.proveedor.empresa,
                f"${compra.total:,.2f}",
                compra.get_estado_display()
            ])
            total_compras += compra.total

        # Agregar fila de total
        table_data.append(['', '', 'TOTAL:', f"${total_compras:,.2f}", ''])

        # Crear tabla
        table = self._crear_tabla(table_data, [1.2*inch, 1.2*inch, 2*inch, 1*inch, 1.2*inch])
        elements.append(table)

        # Generar PDF
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer

    def generar_reporte_inventario(self, data):
        """Genera PDF de reporte de inventario."""
        doc = SimpleDocTemplate(self.buffer, pagesize=self.pagesize)
        elements = []

        # Título
        elements.append(Paragraph(self.titulo, self._get_title_style()))
        elements.append(Spacer(1, 0.3*inch))

        # Fecha de generación
        elements.append(Paragraph(
            f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self._get_fecha_style()
        ))
        elements.append(Spacer(1, 0.2*inch))

        # Tabla de datos
        table_data = [['Código', 'Producto', 'Categoría', 'Stock', 'Precio Venta']]

        stock_total = 0
        valor_total = 0
        for producto in data:
            table_data.append([
                producto.codigo,
                producto.nombre[:25],  # Limitar longitud
                producto.categoria.nombre,
                str(producto.cantidad),
                f"${producto.precio_venta:,.2f}"
            ])
            stock_total += producto.cantidad
            valor_total += (producto.cantidad * producto.precio_venta)

        # Agregar filas de resumen
        table_data.append(['', '', 'TOTALES:', f"{stock_total} unidades", f"${valor_total:,.2f}"])

        # Crear tabla
        table = self._crear_tabla(table_data, [1*inch, 2.5*inch, 1.5*inch, 0.8*inch, 1.2*inch])
        elements.append(table)

        # Generar PDF
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer

    def obtener_response(self, filename='reporte.pdf'):
        """Retorna una HttpResponse con el PDF generado."""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write(self.buffer.getvalue())
        return response


def generar_pdf_ventas(data, titulo='Reporte de Ventas'):
    """Función auxiliar para generar PDF de ventas."""
    reporter = PDFReporter(titulo, 'venta')
    reporter.generar_reporte_ventas(data)
    return reporter.obtener_response(filename='reporte_ventas.pdf')


def generar_pdf_compras(data, titulo='Reporte de Compras'):
    """Función auxiliar para generar PDF de compras."""
    reporter = PDFReporter(titulo, 'compra')
    reporter.generar_reporte_compras(data)
    return reporter.obtener_response(filename='reporte_compras.pdf')


def generar_pdf_inventario(data, titulo='Reporte de Inventario'):
    """Función auxiliar para generar PDF de inventario."""
    reporter = PDFReporter(titulo, 'inventario')
    reporter.generar_reporte_inventario(data)
    return reporter.obtener_response(filename='reporte_inventario.pdf')
