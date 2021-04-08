# Site - Câmara Municipal de Vereadores

## Instalando

Na raiz do projeto, execute:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
make install
```

## Configurando variáveis de ambiente

Crie um arquivo .env na raiz do projeto e adicione as seguintes linhas:

```toml
FLASK_APP="app:create_app()"
FLASK_ENV="development"
```

## Inicializando o banco de dados

```bash
make db
```

## Testando

```bash
make test
```

## Levantando Servidor de Desenvolvimento

Na raiz do projeto, execute:

```bash
flask run
```

## Acessando àrea administrativa

Usuário: admin@admin
Senha: admin

## Configurando o site

- Alterando o Title: edite o arquivo `templates/public/base.html`. As alterações no `title` desse arquivo serão refletidas em todas as outras páginas(com excessão da página de login).