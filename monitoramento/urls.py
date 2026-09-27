from django.urls import path
from django.views.generic import TemplateView

from monitoramento.views import (
    criar_cisterna,
    criar_usuario,
    editar_cisterna,
    excluir_cisterna,
    lista_alertas,
    lista_cisternas,
    lista_usuarios,
    monitoramento,
)


urlpatterns = [

    path(
    '',
    TemplateView.as_view(
        template_name='monitoramento/apresentacao.html'
    ),
    name='apresentacao'
),

    path(
        'cisternas/',
        lista_cisternas,
        name='lista_cisternas'
    ),

    path(
        'cisternas/cadastrar/',
        criar_cisterna,
        name='criar_cisterna'
    ),

    path(
        'cisternas/<int:id>/editar/',
        editar_cisterna,
        name='editar_cisterna'
    ),

    path(
        'cisternas/<int:id>/excluir/',
        excluir_cisterna,
        name='excluir_cisterna'
    ),

    path(
        'usuarios/',
        lista_usuarios,
        name='lista_usuarios'
    ),

    path(
        'usuarios/cadastrar/',
        criar_usuario,
        name='criar_usuario'
    ),

    path(
        'monitoramento/',
        monitoramento,
        name='monitoramento'
    ),

    path(
        'alertas/', 
        lista_alertas,
        name='lista_alertas'),
]