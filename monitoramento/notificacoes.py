from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail


def enviar_email_alerta(alerta):
    destinatarios = list(
        User.objects.filter(
            is_active=True
        )
        .exclude(email='')
        .values_list('email', flat=True)
    )

    if not destinatarios:
        return

    send_mail(
        subject='Alerta crítico - Sistema de Monitoramento',
        message=(
            f'{alerta.mensagem}\n\n'
            f'Cisterna: {alerta.cisterna.identificacao}\n'
            f'Data e hora: {alerta.data_hora.strftime("%d/%m/%Y %H:%M")}\n'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=destinatarios,
        fail_silently=True,
    )