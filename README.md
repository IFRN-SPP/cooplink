[DJANGO__BADGE]: https://img.shields.io/badge/-Django-0d1117?style=for-the-badge&logo=Django&logoColor=green
[PYTHON__BADGE]: https://img.shields.io/badge/-Python-0d1117?style=for-the-badge&logo=Python
[HTML__BADGE]: https://img.shields.io/badge/-HTML5-0d1117?style=for-the-badge&logo=html5&logoColor
[CSS__BADGE]: https://img.shields.io/badge/-CSS3-0d1117?style=for-the-badge&logo=css3&logoColor=blue
[JAVASCRIPT__BADGE]: https://img.shields.io/badge/-JavaScript-0d1117?style=for-the-badge&logo=javascript&logoColor
[JQUERY__BADGE]: https://img.shields.io/badge/-Jquery-0d1117?style=for-the-badge&logo=jquery&logoColor
[BOOTSTRAP_BADGE]: https://img.shields.io/badge/-Bootstrap-0d1117?style=for-the-badge&logo=bootstrap&logoColor

<h1 align="center" style="font-weight: bold;">CoopLink</h1>

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#tecnologias">Tecnologias</a> •
  <a href="#instalação">Instalação</a> •
  <a href="#colaboradores">Colaboradores</a>
</p>

<p align="center">
  <b></b>
</p>

---

## Sobre

O CoopLink é sistema web criado para o controle administrativo dos pedidos de produtos feitos à cooperativas de agricultura familiar e economia solidária.

O sistema possui as seguintes funciolalidades:

- Login, cadastro e administração de usuários

- Gerencimento de produtos, chamadas públicas, instituições e pedidos de produtos

- Relátorios de pedidos em PDF gerados automaticamente

- Diferentes interfaces para administradores e usuários comuns

---

## Tecnologias

Essas são as tecnologias usadas nesse projeto.

![django][DJANGO__BADGE]
![python][PYTHON__BADGE]
![html][HTML__BADGE]
![css][CSS__BADGE]
![javascript][javascript__BADGE]
![jquery][JQUERY__BADGE]
![bootstrap][BOOTSTRAP_BADGE]

---

## Instalação

### Configurando o ambiente

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

### Configurando sua máquina

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

### Rodando o servidor

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

## Colaboradores

Os mais sinceros agradecimentos para as pessoas que tornaram esse projeto possível. ❤️

### Alunos

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/dvanael" title="Ana Barbosa">
        <img src="https://avatars.githubusercontent.com/dvanael" width="100px;" alt="collaborators pictures"/><br>
        <sub>
          <b>Ana Barbosa 🐋</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/poliana-dev" title="Poliana Pinheiro">
        <img src="https://avatars.githubusercontent.com/poliana-dev" width="100px;" alt="collaborators pictures"/><br>
        <sub>
          <b>Poliana Pinheiro 🐸</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/devwenderson" title="Wenderson Nascimento">
        <img src="https://avatars.githubusercontent.com/devwenderson" width="100px;" alt="collaborators pictures"/><br>
        <sub>
          <b>Wenderson Nascimento 🦆</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

### Orientadores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/dvcirilo" title="Diego Cirilo">
        <img src="https://avatars.githubusercontent.com/dvcirilo" width="100px;" alt="collaborators pictures"/><br>
        <sub>
          <b>Diego Cirilo 🐧</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

---
