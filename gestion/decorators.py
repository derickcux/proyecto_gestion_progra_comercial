"""
Decoradores personalizados para control de acceso basado en grupos (RBAC).
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def grupo_requerido(*grupos):
    """
    Decorador que verifica si el usuario pertenece a uno de los grupos especificados.

    Uso:
        @grupo_requerido('vendedor')
        def mi_vista(request):
            ...

        @grupo_requerido('administrador', 'gerente')
        def otra_vista(request):
            ...
    """
    def decorador(vista):
        @wraps(vista)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario pertenece a alguno de los grupos requeridos
            if request.user.groups.filter(name__in=grupos).exists():
                return vista(request, *args, **kwargs)

            # Si no tiene permisos, mostrar mensaje y redirigir
            messages.error(request, 'No tiene permiso para acceder a esta página.')
            return redirect('inicio')

        return wrapper
    return decorador


def solo_administrador(vista):
    """
    Decorador que solo permite acceso al grupo 'administrador'.
    """
    @wraps(vista)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='administrador').exists():
            return vista(request, *args, **kwargs)

        messages.error(request, 'Solo administradores pueden acceder aquí.')
        return redirect('inicio')

    return wrapper


def solo_vendedor(vista):
    """
    Decorador que solo permite acceso al grupo 'vendedor'.
    """
    @wraps(vista)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='vendedor').exists():
            return vista(request, *args, **kwargs)

        messages.error(request, 'Solo vendedores pueden acceder aquí.')
        return redirect('inicio')

    return wrapper


def solo_comprador(vista):
    """
    Decorador que solo permite acceso al grupo 'comprador'.
    """
    @wraps(vista)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='comprador').exists():
            return vista(request, *args, **kwargs)

        messages.error(request, 'Solo compradores pueden acceder aquí.')
        return redirect('inicio')

    return wrapper


def administrador_o_vendedor(vista):
    """
    Decorador que permite acceso a administrador o vendedor.
    """
    @wraps(vista)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name__in=['administrador', 'vendedor']).exists():
            return vista(request, *args, **kwargs)

        messages.error(request, 'No tiene permiso para acceder a esta página.')
        return redirect('inicio')

    return wrapper


def administrador_o_comprador(vista):
    """
    Decorador que permite acceso a administrador o comprador.
    """
    @wraps(vista)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name__in=['administrador', 'comprador']).exists():
            return vista(request, *args, **kwargs)

        messages.error(request, 'No tiene permiso para acceder a esta página.')
        return redirect('inicio')

    return wrapper
