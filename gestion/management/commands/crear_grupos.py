"""
Comando para crear los grupos de usuarios y asignar permisos.

Uso: python manage.py crear_grupos
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from gestion.models import Venta, Compra, Producto, Cliente, Proveedor, Categoria


class Command(BaseCommand):
    help = 'Crea los grupos de usuarios (administrador, vendedor, comprador) con sus permisos'

    def handle(self, *args, **options):
        # Definir los grupos y sus permisos
        grupos_config = {
            'administrador': {
                'descripcion': 'Acceso total al sistema',
                'modelos': ['auth.permission', 'auth.user', 'auth.group'],
                'permisos_especificos': self.obtener_todos_permisos(),
            },
            'vendedor': {
                'descripcion': 'Acceso a gestión de ventas y vista de productos',
                'modelos': ['Venta', 'Cliente', 'Producto', 'Categoria'],
                'acciones': ['view', 'add', 'change', 'delete'],
            },
            'comprador': {
                'descripcion': 'Acceso a gestión de compras y proveedores',
                'modelos': ['Compra', 'Proveedor', 'Producto', 'Categoria'],
                'acciones': ['view', 'add', 'change', 'delete'],
            },
        }

        for nombre_grupo, config in grupos_config.items():
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Grupo "{nombre_grupo}" creado correctamente')
                )
            else:
                self.stdout.write(f'  Grupo "{nombre_grupo}" ya existe')

            # Asignar permisos
            if nombre_grupo == 'administrador':
                # Admin tiene todos los permisos
                grupo.permissions.set(Permission.objects.all())
                self.stdout.write(f'  ✓ Se asignaron todos los permisos')
            else:
                # Vendedor y Comprador tienen permisos específicos
                permisos = self.obtener_permisos_grupo(
                    config['modelos'],
                    config.get('acciones', ['view'])
                )
                grupo.permissions.set(permisos)
                self.stdout.write(f'  ✓ Se asignaron {permisos.count()} permisos')

        self.stdout.write(
            self.style.SUCCESS('\n✓ Grupos creados y configurados correctamente')
        )

        # Agregar superusuarios al grupo administrador automáticamente
        self.agregar_superusuarios_al_grupo()

        self.mostrar_resumen()

    def agregar_superusuarios_al_grupo(self):
        """Agrega todos los superusuarios al grupo administrador."""
        try:
            admin_group = Group.objects.get(name='administrador')
            superusers = User.objects.filter(is_superuser=True)

            if superusers.exists():
                self.stdout.write('\n' + '='*50)
                self.stdout.write('CONFIGURANDO SUPERUSUARIOS')
                self.stdout.write('='*50)

            for user in superusers:
                if not user.groups.filter(name='administrador').exists():
                    user.groups.add(admin_group)
                    self.stdout.write(f'✓ Usuario "{user.username}" agregado al grupo administrador')
                else:
                    self.stdout.write(f'  Usuario "{user.username}" ya está en el grupo administrador')
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('\n! El grupo administrador no fue creado')
            )

    def obtener_permisos_grupo(self, modelos, acciones):
        """Obtiene los permisos para un grupo específico."""
        permisos = Permission.objects.none()

        for modelo in modelos:
            if '.' in modelo:  # Permiso de la forma 'app.permission'
                app_label, codename = modelo.split('.')
                permisos |= Permission.objects.filter(
                    content_type__app_label=app_label,
                    codename=codename
                )
            else:
                # Obtener permisos para un modelo específico
                try:
                    content_type = ContentType.objects.get(
                        app_label='gestion',
                        model=modelo.lower()
                    )
                    for accion in acciones:
                        permisos |= Permission.objects.filter(
                            content_type=content_type,
                            codename__startswith=accion
                        )
                except ContentType.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'  ! Modelo {modelo} no encontrado')
                    )

        return permisos.distinct()

    def obtener_todos_permisos(self):
        """Retorna todos los permisos del sistema."""
        return Permission.objects.all()

    def mostrar_resumen(self):
        """Muestra un resumen de los grupos creados."""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('RESUMEN DE GRUPOS CREADOS')
        self.stdout.write('='*50)

        for grupo in Group.objects.all():
            self.stdout.write(f'\n📋 {grupo.name.upper()}')
            self.stdout.write(f'   Permisos: {grupo.permissions.count()}')

            # Mostrar usuarios en el grupo
            usuarios = grupo.user_set.all()
            if usuarios.exists():
                self.stdout.write(f'   Usuarios: {", ".join([u.username for u in usuarios])}')
