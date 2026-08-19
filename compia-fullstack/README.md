# COMPIA Editora — E-commerce Full Stack - https://ufcg-pweb-projeto.vercel.app/

Projeto reconstruído a partir do protótipo HTML/CSS/JS, agora com frontend React, backend FastAPI e PostgreSQL real.

## O que funciona

- cadastro e login de usuários;
- autenticação JWT e senhas com hash Argon2;
- catálogo carregado do PostgreSQL;
- busca, categorias e ordenação;
- detalhes de produto;
- carrinho persistido no navegador;
- checkout validado novamente no backend;
- entrega com frete fixo configurável ou retirada no local;
- pedidos persistidos no banco;
- baixa de estoque ao confirmar pagamento;
- histórico de pedidos na área do cliente;
- download de e-books após pagamento;
- painel administrativo de produtos, pedidos e clientes;
- perfis `admin`, `editor`, `seller` e `customer`;
- cartão preparado para Stripe Checkout real;
- PIX sem gateway: o pedido fica pendente e um admin/vendedor pode confirmar o pagamento manualmente;
- Docker para frontend, backend e PostgreSQL.

## Arquitetura

```text
compia-fullstack/
├── frontend/                 React + Vite
│   └── src/
│       ├── api/              acesso ao backend
│       ├── components/       componentes reutilizáveis
│       ├── contexts/         autenticação e carrinho
│       ├── hooks/            hooks de domínio
│       ├── pages/            páginas da aplicação
│       ├── routes/           proteção de rotas
│       └── utils/            utilitários
├── backend/                  FastAPI
│   └── app/
│       ├── routers/          endpoints HTTP
│       ├── services/         regras de negócio
│       ├── scripts/          criação e seed do banco
│       ├── models.py         entidades SQLAlchemy
│       ├── schemas.py        validação Pydantic
│       ├── security.py       JWT e senha
│       └── db.py             conexão PostgreSQL
└── docker-compose.yml
```

A divisão evita que telas conheçam detalhes do banco ou que componentes precisem fazer `fetch` diretamente. O frontend chama somente os módulos de `api/`, enquanto regras de pedido e pagamento ficam em `services/` no backend.

# 1. Forma mais simples: Docker

Pré-requisito: Docker Desktop.

Na raiz do projeto:

```bash
docker compose up --build
```

Acesse:

- Loja: http://localhost:5173
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- PostgreSQL: localhost:5432

Usuário administrador criado automaticamente:

```text
E-mail: admin@compia.com.br
Senha: Admin123!
```

Troque essa senha antes de qualquer publicação real.

Para encerrar:

```bash
docker compose down
```

Para apagar também os dados locais:

```bash
docker compose down -v
```

# 2. Rodando sem Docker

## Backend

Tenha Python 3.12+ e PostgreSQL instalados. Crie um banco chamado `compia`.

```bash
cd backend
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Depois:

```bash
pip install -r requirements.txt
cp .env.example .env
python -m app.scripts.init_db
python -m app.scripts.seed
uvicorn app.main:app --reload
```

Se o PostgreSQL estiver local, ajuste `DATABASE_URL` no `.env`, por exemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/compia
```

## Frontend

Em outro terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```


