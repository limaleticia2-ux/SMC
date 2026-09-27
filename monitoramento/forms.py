from django import forms
from django.contrib.auth.models import User

from .models import Cisterna


class CisternaForm(forms.ModelForm):

    class Meta:
        model = Cisterna

        fields = [
            'identificacao',
            'municipio',
            'localidade',
            'participante',
            'latitude',
            'longitude',
            'capacidade_total',
            'situacao',
            'imagem',
        ]

        labels = {
            'identificacao': 'Identificação',
            'municipio': 'Município',
            'localidade': 'Localização',
            'participante': 'Participante',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'capacidade_total': 'Capacidade Total (L)',
            'situacao': 'Situação',
            'imagem': 'Imagem da cisterna',
        }

        widgets = {
            'identificacao': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: CISTERNA-001'
                }
            ),

            'latitude': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex.: -5.890000',
                    'step': 'any'
                }
            ),

            'longitude': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex.: -35.270000',
                    'step': 'any'
                }
            ),

            'capacidade_total': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex.: 16000'
                }
            ),

            'imagem': forms.ClearableFileInput(
                attrs={
                    'accept': 'image/*'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['identificacao'].required = True
        self.fields['municipio'].required = True
        self.fields['localidade'].required = True
        self.fields['participante'].required = True
        self.fields['situacao'].required = True


class UsuarioForm(forms.ModelForm):

    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Digite a senha'
            }
        )
    )

    confirmar_senha = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Digite a senha novamente'
            }
        )
    )

    perfil = forms.ChoiceField(
        label='Perfil',
        choices=[
            (
                'Administrador do sistema',
                'Administrador do sistema'
            ),
            (
                'Município',
                'Município'
            ),
            (
                'Operador-técnico',
                'Operador-técnico'
            ),
            (
                'Visualizador',
                'Visualizador'
            ),
        ]
    )

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'perfil',
            'senha',
            'confirmar_senha',
        ]

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de usuário',
            'email': 'E-mail',
        }

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nome'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Sobrenome'
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: joao.silva'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'exemplo@email.com'
                }
            ),
        }

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():

            raise forms.ValidationError(
                'Este nome de usuário já está sendo utilizado.'
            )

        return username

    def clean(self):

        dados = super().clean()

        senha = dados.get('senha')
        confirmar_senha = dados.get('confirmar_senha')

        if (
            senha
            and confirmar_senha
            and senha != confirmar_senha
        ):

            raise forms.ValidationError(
                'As senhas não coincidem.'
            )

        return dados