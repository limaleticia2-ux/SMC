# SMC - Monitoramento de Cisternas

Projeto Django para monitoramento de cisternas, com landing page e painel de acompanhamento.

## Requisitos

- Python 3.12 ou superior
- pip

## Como iniciar o projeto

1. Clone ou acesse a pasta do projeto:

```bash
cd SMC
```

2. Crie um ambiente virtual:

```bash
python3 -m venv .venv
```

3. Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

No Windows, use:

```bash
.venv\Scripts\activate
```

4. Instale as dependencias:

```bash
pip install -r requirements.txt
```

5. Aplique as migracoes do banco de dados:

```bash
python manage.py migrate
```

6. Inicie o servidor local:

```bash
python manage.py runserver
```

7. Acesse no navegador:

```text
http://127.0.0.1:8000/
```

## Rotas principais

- `/` - Landing page do SMC
- `/painel/` - Painel de monitoramento
- `/admin/` - Administracao do Django

## Instalar dependencias
```
pip install -r requirements.txt

```

## Comandos uteis

Verificar a configuracao do projeto:

```bash
python manage.py check
```

Criar novas migracoes apos alterar models:

```bash
python manage.py makemigrations
```

Aplicar migracoes pendentes:

```bash
python manage.py migrate
```
