from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    CisternaForm,
    DispositivoForm,
    MunicipioForm,
    UsuarioForm,
)
from .models import (
    Alerta,
    Cisterna,
    Dispositivo,
    LeituraTelemetria,
    Localidade,
    Municipio,
    Participante,
)

def somente_perfis(*perfis):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):

            if (
                request.user.is_superuser
                or request.user.groups.filter(name__in=perfis).exists()
            ):
                return view_func(request, *args, **kwargs)

            return render(
                request,
                'monitoramento/acesso_negado.html',
                status=403
            )

        return wrapper

    return decorator


@login_required
def index(request):
    contexto = {
        'total_cisternas': Cisterna.objects.count(),
        'total_participantes': Participante.objects.count(),
        'total_leituras': LeituraTelemetria.objects.count(),
        'total_alertas': Alerta.objects.count(),
        'total_localidades': Localidade.objects.count(),
        'ultimas_leituras': LeituraTelemetria.objects.select_related(
            'cisterna',
            'cisterna__localidade'
        ).order_by('-data_hora')[:5],
        'alertas_recentes': Alerta.objects.select_related(
            'cisterna'
        ).order_by('-data_hora')[:5],
    }

    return render(
        request,
        'monitoramento/index.html',
        contexto
    )


@login_required
def lista_cisternas(request):
    cisternas = Cisterna.objects.select_related(
        'participante',
        'localidade',
        'municipio'
    ).all()

    return render(
        request,
        'monitoramento/cisternas/lista.html',
        {
            'cisternas': cisternas
        }
    )


@somente_perfis('Administrador do sistema')
def criar_cisterna(request):
    if request.method == 'POST':
        form = CisternaForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('lista_cisternas')

    else:
        form = CisternaForm()

    return render(
        request,
        'monitoramento/cisternas/form.html',
        {
            'form': form,
            'titulo': 'Cadastrar cisterna'
        }
    )


@somente_perfis('Administrador do sistema')
def editar_cisterna(request, id):
    cisterna = get_object_or_404(
        Cisterna,
        id=id
    )

    if request.method == 'POST':
        form = CisternaForm(
            request.POST,
            request.FILES,
            instance=cisterna
        )

        if form.is_valid():
            form.save()
            return redirect('lista_cisternas')

    else:
        form = CisternaForm(
            instance=cisterna
        )

    return render(
        request,
        'monitoramento/cisternas/form.html',
        {
            'form': form,
            'titulo': 'Editar cisterna'
        }
    )


@somente_perfis('Administrador do sistema')
def excluir_cisterna(request, id):
    cisterna = get_object_or_404(
        Cisterna,
        id=id
    )

    if request.method == 'POST':
        cisterna.delete()
        return redirect('lista_cisternas')

    return render(
        request,
        'monitoramento/cisternas/confirmar_exclusao.html',
        {
            'cisterna': cisterna
        }
    )


@somente_perfis('Administrador do sistema')
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('username')

    return render(
        request,
        'monitoramento/usuarios/lista.html',
        {
            'usuarios': usuarios
        }
    )


@somente_perfis('Administrador do sistema')
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)

            usuario.first_name = form.cleaned_data['first_name']
            usuario.last_name = form.cleaned_data['last_name']
            usuario.email = form.cleaned_data['email']

            usuario.set_password(
                form.cleaned_data['senha']
            )

            usuario.save()

            perfil = form.cleaned_data['perfil']

            grupo, _ = Group.objects.get_or_create(
                name=perfil
            )

            usuario.groups.clear()
            usuario.groups.add(grupo)

            return redirect('lista_usuarios')

    else:
        form = UsuarioForm()

    return render(
        request,
        'monitoramento/usuarios/form.html',
        {
            'form': form,
            'titulo': 'Cadastrar usuário'
        }
    )


@login_required
def monitoramento(request):
    cisternas = Cisterna.objects.select_related(
        'participante',
        'localidade',
        'municipio'
    ).all()

    ultimas_leituras = (
        LeituraTelemetria.objects
        .select_related(
            'cisterna',
            'cisterna__localidade'
        )
        .order_by('-data_hora')
    )

    leituras_por_cisterna = {}

    for leitura in ultimas_leituras:
        if leitura.cisterna_id not in leituras_por_cisterna:
            leituras_por_cisterna[leitura.cisterna_id] = leitura

    for cisterna in cisternas:
        cisterna.ultima_leitura = leituras_por_cisterna.get(
            cisterna.id
        )

        if cisterna.ultima_leitura:
            nivel = cisterna.ultima_leitura.nivel

            if nivel >= 70:
                cisterna.status_monitoramento = 'Normal'
                cisterna.status_classe = 'normal'

            elif nivel >= 30:
                cisterna.status_monitoramento = 'Atenção'
                cisterna.status_classe = 'atencao'

            else:
                cisterna.status_monitoramento = 'Crítico'
                cisterna.status_classe = 'critico'

        else:
            cisterna.status_monitoramento = 'Sem dados'
            cisterna.status_classe = 'sem-dados'

    return render(
        request,
        'monitoramento/monitoramento.html',
        {
            'cisternas': cisternas,
            'total_monitoradas': cisternas.count(),
            'total_leituras': ultimas_leituras.count(),
        }
    )


@login_required
def lista_alertas(request):
    busca = request.GET.get('q', '').strip()

    alertas = (
        Alerta.objects
        .select_related(
            'cisterna',
            'cisterna__municipio',
            'cisterna__localidade'
        )
        .order_by('-data_hora')
    )

    if busca:
        alertas = alertas.filter(
            Q(mensagem__icontains=busca)
            | Q(cisterna__identificacao__icontains=busca)
            | Q(cisterna__municipio__nome__icontains=busca)
            | Q(cisterna__localidade__nome__icontains=busca)
        )

    return render(
        request,
        'monitoramento/alertas/lista.html',
        {
            'alertas': alertas,
            'busca': busca,
        }
    )


@somente_perfis('Administrador do sistema')
def lista_municipios(request):
    municipios = Municipio.objects.all().order_by(
        'nome'
    )

    return render(
        request,
        'monitoramento/municipios/lista.html',
        {
            'municipios': municipios
        }
    )


@somente_perfis('Administrador do sistema')
def criar_municipio(request):
    if request.method == 'POST':
        form = MunicipioForm(
            request.POST
        )

        if form.is_valid():
            form.save()
            return redirect('lista_municipios')

    else:
        form = MunicipioForm()

    return render(
        request,
        'monitoramento/municipios/form.html',
        {
            'form': form,
            'titulo': 'Cadastrar município'
        }
    )


@somente_perfis('Administrador do sistema')
def editar_municipio(request, id):
    municipio = get_object_or_404(
        Municipio,
        id=id
    )

    if request.method == 'POST':
        form = MunicipioForm(
            request.POST,
            instance=municipio
        )

        if form.is_valid():
            form.save()
            return redirect('lista_municipios')

    else:
        form = MunicipioForm(
            instance=municipio
        )

    return render(
        request,
        'monitoramento/municipios/form.html',
        {
            'form': form,
            'titulo': 'Editar município'
        }
    )


@login_required
def historico_leituras(request, id):
    cisterna = get_object_or_404(
        Cisterna,
        id=id
    )

    leituras = LeituraTelemetria.objects.filter(
        cisterna=cisterna
    ).order_by('-data_hora')

    return render(
        request,
        'monitoramento/historico/lista.html',
        {
            'cisterna': cisterna,
            'leituras': leituras,
        }
    )

@somente_perfis('Administrador do sistema')
def lista_dispositivos(request):

    dispositivos = Dispositivo.objects.select_related(
        'cisterna'
    ).all().order_by('identificacao')

    return render(
        request,
        'monitoramento/dispositivos/lista.html',
        {
            'dispositivos': dispositivos
        }
    )


@somente_perfis('Administrador do sistema')
def criar_dispositivo(request):

    if request.method == 'POST':

        form = DispositivoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_dispositivos')

    else:
        form = DispositivoForm()

    return render(
        request,
        'monitoramento/dispositivos/form.html',
        {
            'form': form,
            'titulo': 'Cadastrar dispositivo'
        }
    )

@csrf_exempt
def receber_leitura(request):

    if request.method != 'POST':
        return JsonResponse(
            {
                'erro': 'Método não permitido.'
            },
            status=405
        )

    try:
        dados = request.POST

        identificacao = dados.get('identificacao')
        nivel = float(dados.get('nivel'))

        if not identificacao:
            return JsonResponse(
                {
                    'erro': 'Identificação do dispositivo não informada.'
                },
                status=400
            )

        dispositivo = Dispositivo.objects.select_related(
            'cisterna'
        ).filter(
            identificacao=identificacao,
            situacao='ativo'
        ).first()

        if not dispositivo:
            return JsonResponse(
                {
                    'erro': 'Dispositivo não encontrado ou está inativo.'
                },
                status=404
            )

        leitura = LeituraTelemetria.objects.create(
            cisterna=dispositivo.cisterna,
            dispositivo=dispositivo,
            nivel=nivel,
            data_hora=timezone.now()
        )

        return JsonResponse(
            {
                'sucesso': True,
                'mensagem': 'Leitura recebida com sucesso.',
                'dispositivo': dispositivo.identificacao,
                'cisterna': dispositivo.cisterna.identificacao,
                'nivel': leitura.nivel
            },
            status=201
        )

    except (TypeError, ValueError):
        return JsonResponse(
            {
                'erro': 'O nível informado é inválido.'
            },
            status=400
        )

def mapa(request):
    cisternas = Cisterna.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )

    dados_cisternas = []

    for cisterna in cisternas:
        dados_cisternas.append({
            'latitude': float(cisterna.latitude),
            'longitude': float(cisterna.longitude),
            'identificacao': cisterna.identificacao,
            'participante': str(cisterna.participante),
            'municipio': str(cisterna.municipio),
            'localidade': str(cisterna.localidade),
            'capacidade': cisterna.capacidade_total,
            'situacao': cisterna.get_situacao_display(),
        })

    return render(
        request,
        'monitoramento/mapa.html',
        {
            'cisternas': dados_cisternas
        }
    )