from django.urls import path
from monitoramento.views import (
    apresentacao, criar_cisterna, criar_dispositivo, criar_municipio,
    criar_usuario, editar_cisterna, editar_dispositivo, editar_municipio,
    editar_usuario, excluir_cisterna, excluir_dispositivo, excluir_municipio,
    excluir_usuario, historico_leituras, lista_alertas, lista_cisternas,
    lista_dispositivos, lista_municipios, lista_usuarios, mapa, monitoramento,
    receber_leitura,
)

urlpatterns = [
    path('apresentacao/', apresentacao, name='apresentacao'),
    path('cisternas/', lista_cisternas, name='lista_cisternas'),
    path('cisternas/cadastrar/', criar_cisterna, name='criar_cisterna'),
    path('cisternas/<int:id>/editar/', editar_cisterna, name='editar_cisterna'),
    path('cisternas/<int:id>/excluir/', excluir_cisterna, name='excluir_cisterna'),
    path('cisternas/<int:id>/historico/', historico_leituras, name='historico_leituras'),
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/cadastrar/', criar_usuario, name='criar_usuario'),
    path('usuarios/<int:id>/editar/', editar_usuario, name='editar_usuario'),
    path('usuarios/<int:id>/excluir/', excluir_usuario, name='excluir_usuario'),
    path('municipios/', lista_municipios, name='lista_municipios'),
    path('municipios/cadastrar/', criar_municipio, name='criar_municipio'),
    path('municipios/<int:id>/editar/', editar_municipio, name='editar_municipio'),
    path('municipios/<int:id>/excluir/', excluir_municipio, name='excluir_municipio'),
    path('monitoramento/', monitoramento, name='monitoramento'),
    path('mapa/', mapa, name='mapa'),
    path('alertas/', lista_alertas, name='lista_alertas'),
    path('dispositivos/', lista_dispositivos, name='lista_dispositivos'),
    path('dispositivos/cadastrar/', criar_dispositivo, name='criar_dispositivo'),
    path('dispositivos/<int:id>/editar/', editar_dispositivo, name='editar_dispositivo'),
    path('dispositivos/<int:id>/excluir/', excluir_dispositivo, name='excluir_dispositivo'),
    path('api/leituras/', receber_leitura, name='receber_leitura'),
]
