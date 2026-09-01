from django.db import models


class Participante(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Localidade(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Cisterna(models.Model):
    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name="cisternas"
    )
    localidade = models.ForeignKey(
        Localidade,
        on_delete=models.CASCADE,
        related_name="cisternas"
    )
    identificacao = models.CharField(max_length=100)

    def __str__(self):
        return self.identificacao


class LeituraTelemetria(models.Model):
    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="leituras"
    )
    nivel = models.FloatField()
    data_hora = models.DateTimeField()

    def __str__(self):
        return f"{self.cisterna} - {self.data_hora}"


class Alerta(models.Model):
    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="alertas"
    )
    mensagem = models.CharField(max_length=255)
    data_hora = models.DateTimeField()

    def __str__(self):
        return self.mensagem