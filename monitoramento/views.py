from django.shortcuts import render

from .models import (
    Participante,
    Localidade,
    Cisterna,
    LeituraTelemetria,
    Alerta,
)


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