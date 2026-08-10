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

# 3. Variáveis importantes de produção

Nunca publique o `.env` no GitHub.

Gere uma chave segura:

```bash
openssl rand -hex 32
```

Backend:

```env
APP_ENV=production
SECRET_KEY=COLOQUE_A_CHAVE_GERADA
DATABASE_URL=URL_DO_POSTGRES
CORS_ORIGINS=https://www.seudominio.com.br
FRONTEND_URL=https://www.seudominio.com.br
SHIPPING_FLAT_RATE=19.90
PAYMENT_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
ADMIN_EMAIL=seu-admin@dominio.com.br
ADMIN_PASSWORD=UMA_SENHA_FORTE
```

Frontend:

```env
VITE_API_URL=https://api.seudominio.com.br/api/v1
```

# 4. Cartão real com Stripe

Localmente o projeto usa:

```env
PAYMENT_PROVIDER=mock
```

Assim o cartão é aprovado automaticamente somente para desenvolvimento.

Para produção:

1. crie/configure a conta Stripe;
2. coloque `PAYMENT_PROVIDER=stripe`;
3. configure `STRIPE_SECRET_KEY`;
4. crie um webhook apontando para:

```text
https://SUA-API/api/v1/payments/stripe/webhook
```

5. assine pelo menos o evento `checkout.session.completed`;
6. coloque o segredo do webhook em `STRIPE_WEBHOOK_SECRET`.

Quando o webhook confirma o pagamento, o backend marca o pedido como pago e reduz o estoque. O processo é idempotente: um pedido já pago não baixa estoque novamente.

# 5. Hospedagem recomendada

## Opção recomendada

- Frontend React: Vercel
- API FastAPI: Render Web Service
- Banco: Render PostgreSQL gerenciado
- Código: GitHub

Isso mantém o frontend simples e rápido, enquanto API e banco ficam no mesmo provedor e podem usar conexão privada.

## Deploy do backend no Render

Suba este projeto para um repositório GitHub.

No Render:

1. crie um PostgreSQL;
2. crie um Web Service apontando para o mesmo repositório;
3. configure `Root Directory` como `backend`;
4. use o Dockerfile do diretório `backend`;
5. adicione as variáveis de produção listadas acima;
6. em `DATABASE_URL`, use a URL fornecida pelo PostgreSQL do Render;
7. configure o health check como `/health`.

O backend aceita URLs começando com `postgres://` ou `postgresql://` e converte internamente para o driver `psycopg`.

## Deploy do frontend na Vercel

Crie um novo projeto na Vercel usando o mesmo repositório:

- Root Directory: `frontend`
- Framework: Vite
- Build command: `npm run build`
- Output directory: `dist`

Adicione:

```env
VITE_API_URL=https://URL-DO-BACKEND.onrender.com/api/v1
```

Depois do primeiro deploy da Vercel, volte às variáveis do backend e configure:

```env
CORS_ORIGINS=https://URL-DO-FRONTEND.vercel.app
FRONTEND_URL=https://URL-DO-FRONTEND.vercel.app
```

Faça novo deploy do backend.

# 6. Domínio próprio

Quando tudo estiver funcionando, você pode usar, por exemplo:

```text
www.compia.com.br -> Vercel
api.compia.com.br -> Render
```

Nesse caso atualize:

```env
VITE_API_URL=https://api.compia.com.br/api/v1
CORS_ORIGINS=https://www.compia.com.br
FRONTEND_URL=https://www.compia.com.br
```

# 7. Observações importantes

- O PIX está propositalmente sem integração automática. Pedidos PIX ficam pendentes e podem ser confirmados manualmente no painel administrativo; a confirmação baixa estoque e libera e-books.
- O frete é fixo ou retirada; não existe consulta aos Correios.
- Os URLs de e-books incluídos no `seed` são apenas exemplos. Substitua por links reais protegidos antes de produção.
- Para arquivos privados em produção, o ideal é usar armazenamento de objetos com URLs temporárias, como S3/R2, em vez de links públicos permanentes.
- `create_all()` é suficiente para esta primeira versão acadêmica. Antes de evoluir o banco em produção, adote migrações versionadas, por exemplo Alembic.
