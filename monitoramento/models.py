
from django.db import models


class Participante(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    nome = models.CharField(max_length=150)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} - {self.estado}"


class Localidade(models.Model):
    nome = models.CharField(max_length=150)

    municipio = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    endereco = models.CharField(
        max_length=255,
        blank=True
    )

    descricao = models.TextField(
        blank=True
    )

    def __str__(self):
        if self.municipio:
            return f"{self.nome} - {self.municipio}"
        return self.nome


class Cisterna(models.Model):
    SITUACAO_CHOICES = [
        ('normal', 'Normal'),
        ('atencao', 'Atenção'),
        ('critico', 'Crítico'),
        ('sem_dados', 'Sem dados'),
    ]

    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name="cisternas"
    )

    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name="cisternas",
        null=True,
        blank=True
    )

    localidade = models.ForeignKey(
        Localidade,
        on_delete=models.CASCADE,
        related_name="cisternas"
    )

    identificacao = models.CharField(max_length=100)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    capacidade_total = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    situacao = models.CharField(
        max_length=20,
        choices=SITUACAO_CHOICES,
        default='sem_dados'
    )

    imagem = models.ImageField(
        upload_to='cisternas/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.identificacao


class Dispositivo(models.Model):
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('manutencao', 'Em manutenção'),
    ]

    identificacao = models.CharField(
        max_length=100,
        unique=True
    )

    tipo_sensor = models.CharField(max_length=100)

    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="dispositivos"
    )

    data_instalacao = models.DateField()

    situacao = models.CharField(
        max_length=20,
        choices=SITUACAO_CHOICES,
        default='ativo'
    )

    def __str__(self):
        return self.identificacao



class LeituraTelemetria(models.Model):
    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="leituras"
    )

    dispositivo = models.ForeignKey(
        Dispositivo,
        on_delete=models.SET_NULL,
        related_name="leituras",
        null=True,
        blank=True
    )

    nivel = models.FloatField()
    data_hora = models.DateTimeField()

    def __str__(self):
        return f"{self.cisterna} - {self.data_hora}"

    def save(self, *args, **kwargs):
        nova_leitura = self.pk is None

        if not 0 <= self.nivel <= 100:
            raise ValueError("O nível deve estar entre 0 e 100.")

        leitura_anterior = None

        if nova_leitura:
            leitura_anterior = (
                LeituraTelemetria.objects
                .filter(cisterna=self.cisterna)
                .order_by('-data_hora', '-pk')
                .first()
            )

        super().save(*args, **kwargs)

        if self.nivel >= 70:
            nova_situacao = 'normal'
        elif self.nivel >= 30:
            nova_situacao = 'atencao'
        else:
            nova_situacao = 'critico'

        Cisterna.objects.filter(pk=self.cisterna_id).update(
            situacao=nova_situacao
        )

        self.cisterna.situacao = nova_situacao

        if not nova_leitura:
            return

        situacao_anterior = None

        if leitura_anterior:
            if leitura_anterior.nivel >= 70:
                situacao_anterior = 'normal'
            elif leitura_anterior.nivel >= 30:
                situacao_anterior = 'atencao'
            else:
                situacao_anterior = 'critico'

        entrou_em_atencao = (
            nova_situacao == 'atencao'
            and situacao_anterior != 'atencao'
        )

        entrou_em_critico = (
            nova_situacao == 'critico'
            and situacao_anterior != 'critico'
        )

        if entrou_em_atencao or entrou_em_critico:
            tipo_alerta = (
                'critico' if entrou_em_critico else 'atencao'
            )

            alerta = Alerta.objects.create(
                cisterna=self.cisterna,
                tipo=tipo_alerta,
                mensagem=(
                    f"Nível {'crítico' if tipo_alerta == 'critico' else 'de atenção'} "
                    f"de água: {self.nivel:.1f}%."
                ),
                data_hora=self.data_hora
            )

            if tipo_alerta == 'critico':
                from .notificacoes import enviar_email_alerta

                enviar_email_alerta(alerta)



class Alerta(models.Model):
    TIPO_CHOICES = [
        ('atencao', 'Atenção'),
        ('critico', 'Crítico'),
    ]

    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="alertas"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='critico'
    )

    mensagem = models.CharField(max_length=255)
    data_hora = models.DateTimeField()

    resolvido = models.BooleanField(default=False)
    resolvido_em = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.mensagem

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='perfil_municipal'
    )

    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    def __str__(self):
        return self.usuario.username