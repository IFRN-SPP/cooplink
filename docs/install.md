
# Instalação

## Configurando o ambiente

 - Clone o [repositório](https://github.com/IFRN-SPP/cooplink)

```bash
git clone https://github.com/IFRN-SPP/cooplink.git
```

- Crie um ambiente virtual

```bash
python -m venv .venv
```

- Ative o ambiente virtual

_windows_
```powershell
.venv/Scripts/activate
```
_linux, macOs_
```bash
source .venv/bin/activate
```

---

## Configurando sua máquina

- Instale as dependências

```bash
pip install -r requirements.txt
```

- Crie as variáveis de ambiente

```bash
python scripts/env_gen.py
```

> Se necessário, mude as configurações do  arquivo `.env`

- Faça as migrações necessárias

```bash
python manage.py migrate
```

---

## Rodando o servidor

- Execute o arquivo `scripts/setup.py` para configuração inicial

```bash
python scripts/setup.py
```
> ! ATENÇÃO: Você receberá um usuário e senha para entrar no sistema.

- Rode o servidor

```bash
python manage.py runserver
```

- Acesse a aplicação localmente

  - **[localhost:8000/](http://localhost:8000/)**

---
