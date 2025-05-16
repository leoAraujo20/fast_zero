# Fast Zero

Projeto de aprendizado baseado no curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/estavel/) do Eduardo Mendes.

## Funcionalidades

- Cadastro, listagem, atualização e remoção de usuários
- CRUD de tarefas (todos) associadas a usuários
- Autenticação e autorização via JWT
- Filtros e paginação para listagem de tarefas
- Testes automatizados com pytest
- Migrations com Alembic
- Pronto para Docker

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/fast-zero.git
   cd fast-zero
   ```

2. Instale as dependências:
   ```sh
   poetry install
   ```

3. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   DATABASE_URL=sqlite+aiosqlite:///./database.db
   SECRET_KEY=sua_chave_secreta
   ALGORITHM=HS256
   ACESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Rode as migrações:
   ```sh
   poetry run alembic upgrade head
   ```

5. Inicie o servidor:
   ```sh
   poetry run uvicorn fast_zero.app:app --reload
   ```

## Testes

Execute todos os testes com cobertura:
```sh
poetry run task test
```

## Docker

Para rodar com Docker Compose:
```sh
docker-compose up --build
```

## Endpoints

- `POST /users` — Cria usuário
- `GET /users` — Lista usuários
- `PUT /users/{id}` — Atualiza usuário
- `DELETE /users/{id}` — Remove usuário
- `POST /auth/token` — Gera token JWT
- `POST /auth/refresh_token` — Renova token JWT
- `POST /todos` — Cria tarefa
- `GET /todos` — Lista tarefas (com filtros)
- `PATCH /todos/{id}` — Atualiza tarefa
- `DELETE /todos/{id}` — Remove tarefa
