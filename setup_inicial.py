#!/usr/bin/env python
"""
Script de setup inicial para el proyecto de gestión empresarial.
Ejecutar: python setup_inicial.py
"""

import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_empresarial_project.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from gestion.models import Venta, Compra, Producto

def crear_grupos():
    """Crea los grupos de usuarios con sus permisos."""
    print("\n" + "="*50)
    print("CREANDO GRUPOS DE USUARIOS")
    print("="*50)

    # Definir grupos
    grupos_config = {
        'administrador': {
            'descripcion': 'Acceso total al sistema',
        },
        'vendedor': {
            'descripcion': 'Acceso a gestión de ventas',
        },
        'comprador': {
            'descripcion': 'Acceso a gestión de compras',
        },
    }

    for nombre_grupo, config in grupos_config.items():
        grupo, created = Group.objects.get_or_create(name=nombre_grupo)

        if created:
            print(f"✓ Grupo '{nombre_grupo}' creado")
        else:
            print(f"  Grupo '{nombre_grupo}' ya existe")

        # Administrador obtiene todos los permisos
        if nombre_grupo == 'administrador':
            grupo.permissions.set(Permission.objects.all())
            print(f"  → {grupo.permissions.count()} permisos asignados")

    print("\n✓ Grupos creados exitosamente")


def crear_usuarios_demo():
    """Crea usuarios de demostración."""
    print("\n" + "="*50)
    print("CREANDO USUARIOS DE DEMOSTRACIÓN")
    print("="*50)

    usuarios_demo = [
        {
            'username': 'admin',
            'email': 'admin@empresa.com',
            'password': 'admin123',
            'grupo': 'administrador',
            'is_superuser': True  # Este será superusuario
        },
        {
            'username': 'vendedor1',
            'email': 'vendedor@empresa.com',
            'password': 'vendedor123',
            'grupo': 'vendedor',
            'is_superuser': False
        },
        {
            'username': 'comprador1',
            'email': 'comprador@empresa.com',
            'password': 'comprador123',
            'grupo': 'comprador',
            'is_superuser': False
        },
    ]

    for user_data in usuarios_demo:
        username = user_data['username']

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"  Usuario '{username}' ya existe")
            continue

        # Crear usuario
        if user_data.get('is_superuser'):
            user = User.objects.create_superuser(
                username=username,
                email=user_data['email'],
                password=user_data['password']
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password=user_data['password']
            )

        # Asignar grupo
        grupo = Group.objects.get(name=user_data['grupo'])
        user.groups.add(grupo)

        role_text = f"grupo: {user_data['grupo']}"
        if user_data.get('is_superuser'):
            role_text += " (SUPERUSUARIO)"

        print(f"✓ Usuario '{username}' creado ({role_text})")

    print("\n✓ Usuarios de demostración creados")


def mostrar_credenciales():
    """Muestra las credenciales de acceso."""
    print("\n" + "="*50)
    print("CREDENCIALES DE ACCESO")
    print("="*50)

    usuarios_demo = [
        ('admin', 'admin123', 'Administrador - Acceso total'),
        ('vendedor1', 'vendedor123', 'Vendedor - Gestión de ventas'),
        ('comprador1', 'comprador123', 'Comprador - Gestión de compras'),
    ]

    for username, password, rol in usuarios_demo:
        print(f"\nUsuario: {username}")
        print(f"Contraseña: {password}")
        print(f"Rol: {rol}")

    print("\n" + "="*50)
    print("Acceso a la aplicación:")
    print("  URL: http://localhost:8000/")
    print("  Admin: http://localhost:8000/admin/")
    print("="*50 + "\n")


def main():
    """Ejecuta el setup inicial completo."""
    print("\n╔════════════════════════════════════════════════════╗")
    print("║      SETUP INICIAL - GESTIÓN EMPRESARIAL          ║")
    print("╚════════════════════════════════════════════════════╝")

    try:
        # Crear grupos
        crear_grupos()

        # Crear usuarios de demostración
        crear_usuarios_demo()
        mostrar_credenciales()

        print("\n✓ Setup inicial completado exitosamente")
        print("\nProximos pasos:")
        print("  1. Ejecuta: python manage.py runserver")
        print("  2. Accede a: http://localhost:8000/admin/")
        print("  3. Inicia sesión con las credenciales creadas")

    except Exception as e:
        print(f"\n✗ Error durante el setup: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
