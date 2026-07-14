# 🏢 Glassroof Imobiliário

> Um sistema de avaliações transparente para o mercado imobiliário. Saiba o que as pessoas falaram sobre seu próximo lar antes de assinar o contrato.

## 📖 Sobre o Projeto

O **Glassroof Imobiliário** é uma plataforma colaborativa focada no mercado de imóveis. O sistema permite que imobiliárias cadastrem seus portfólios, enquanto usuários podem avaliar e comentar sobre os imóveis.

O objetivo é democratizar o acesso à informação real sobre os imóveis, ajudando futuros moradores a tomarem decisões mais seguras e embasadas.

## 🚀 Tecnologias Utilizadas (Stack)

O projeto foi desenvolvido utilizando uma arquitetura moderna baseada em componentes no Front-end e uma RESTful API orientada a serviços no Back-end.

**Front-end:**
* **React.js**: Biblioteca principal para construção da interface.
* **React Router**: Gerenciamento de rotas e navegação SPA (Single Page Application).

**Back-end:**
* **Python**: Linguagem principal.
* **Flask**: Microframework web para a construção da API.
* **SQLAlchemy**: ORM para comunicação fluida com o banco de dados.
* **Pytest / Unittest**: Framework para garantia de qualidade através de testes unitários.

**Banco de Dados:**
* **MySQL**: Banco de dados relacional.

## 📂 Arquitetura e Disposição de Pastas

O repositório está dividido em duas aplicações principais (Monorepo). O back-end utiliza uma arquitetura em camadas (`Routes` -> `Services` -> `Models`), garantindo o isolamento da regra de negócio.

```text
glassroof-imobiliario/
├── backend/                  # API Flask
│   ├── app/
│   │   ├── __init__.py       # Factory da aplicação Flask
│   │   ├── config.py         # Variáveis de ambiente e configs do BD
│   │   ├── models/           # Modelos do SQLAlchemy (User, Property, Review)
│   │   ├── routes/           # Endpoints (camada de transporte HTTP)
│   │   └── services/         # Regras de negócio puras (isoladas para facilitar testes)
│   ├── tests/                # Suíte de testes unitários e de integração
│   │   ├── test_services/    # Testes das regras de negócio
│   │   └── test_routes/      # Testes dos endpoints da API
│   ├── requirements.txt      # Dependências do Python
│   └── run.py                # Ponto de entrada para rodar o servidor
│
├── frontend/                 # Aplicação React
│   ├── public/               # Arquivos estáticos
│   ├── src/
│   │   ├── assets/           # Imagens e ícones
│   │   ├── components/       # Componentes de UI reutilizáveis
│   │   ├── pages/            # Páginas mapeadas nas rotas
│   │   ├── routes/           # Configuração do React Router
│   │   ├── services/         # Integração com a API Flask (ex: chamadas Axios)
│   │   ├── App.jsx           # Componente raiz
│   │   └── main.jsx          # Ponto de montagem do React
│   └── package.json          # Dependências do Node/React
│
└── README.md                 # Documentação do projeto
```

## 🏗️ Arquitetura do Sistema

### Estilo Arquitetural

O **Glassroof** adota uma **arquitetura em camadas (Layered Architecture)** combinada com princípios de **separação de responsabilidades** e **padrões de design enterprise**. Essa abordagem permite:

- **Escalabilidade horizontal**: Fácil adição de novos serviços
- **Testabilidade**: Componentes isolados e independentes
- **Manutenibilidade**: Código organizado em camadas bem definidas
- **Flexibilidade**: Fácil substituição de componentes

---

### Diagrama C4 - Nível 1: Contexto do Sistema

```
┌──────────────────────────────────────────────────────────────┐
│                     Glassroof System                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                    ┌──────────────────┐    │
│  │              │    HTTP/REST       │                  │    │
│  │  Usuário     │◄──────────────────►│  React Frontend  │    │
│  │   (Browser)  │                    │    (SPA)         │    │
│  └──────────────┘                    └──────────────────┘    │
│                                              │               │
│                                              │ HTTP Requests │
│                                              ▼               │
│                                      ┌──────────────────┐    │
│                                      │  Flask API       │    │
│                                      │  (RESTful)       │    │
│                                      └──────────────────┘    │
│                                              │               │
│                                              │ SQL Queries   │
│                                              ▼               │
│                                      ┌──────────────────┐    │
│                                      │  MySQL Database  │    │
│                                      │  (Relacional)    │    │
│                                      └──────────────────┘    │
│                                                              │
└──────────────────────────────────────────────────────────────┘

Atores:
• Usuários (Visitantes, Inquilinos, Imobiliárias)
• Administrador do Sistema

Sistemas Externos:
• Navegador Web
```

---

### Diagrama C4 - Nível 2: Containers

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        Glassroof Application                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────┐          ┌────────────────────────┐   │
│  │   React Frontend (SPA)          │          │   Browser / Node.js    │   │
│  │  ┌──────────────────────────────┤          │                        │   │
│  │  │ • Home Page                  │          │ • React 18+            │   │
│  │  │ • Property Search & Filter   │          │ • React Router 6       │   │ 
│  │  │ • Property Details           │          │ • Axios (HTTP Client)  │   │
│  │  │ • Reviews Management         │          │ • Material UI / Styled │   │
│  │  │ • User Authentication        │          │                        │   │
│  │  │ • Admin Dashboard            │          │                        │   │
│  │  └──────────────────────────────┤          │                        │   │
│  │            │                    │          │                        │   │
│  │            │ HTTP/JSON          │          │                        │   │
│  │            ▼                    │          │                        │   │
│  └─────────────────────────────────┘          └────────────────────────┘   │
│            │                                                               │
│            │ REST API Calls                                                │
│            ▼                                                               │
│  ┌─────────────────────────────────┐           ┌────────────────────────┐  │
│  │   Flask API (Python)            │           │   Python 3.10+         │  │
│  │  ┌──────────────────────────────┤           │                        │  │
│  │  │ • Routes & Controllers       │           │ • Flask 2.x            │  │
│  │  │ • Authentication Servic      │           │ • SQLAlchemy ORM       │  │
│  │  │ • Property Service           │           │ • Pytest / Unittest    │  │
│  │  │ • Review Service             │           │ • JWT (Auth)           │  │
│  │  │ • User Service               │           │ • CORS Support         │  │
│  │  │ • Search & Filter Logic      │           │                        │  │
│  │  │ • Validation & Error Handler │           │                        │  │
│  │  └──────────────────────────────┤           │                        │  │
│  │            │                    │           │                        │  │
│  │            │ SQL Queries        │           │                        │  │
│  │            ▼                    │           │                        │  │
│  └─────────────────────────────────┘           └────────────────────────┘  │
│            │                                                               │
│            ▼                                                               │
│  ┌─────────────────────────────────┐          ┌────────────────────────┐   │
│  │   MySQL Database                │          │   MySQL 8.0+           │   │
│  │  ┌──────────────────────────────┤          │                        │   │
│  │  │ • Users Table                │          │ • Relational Schema    │   │
│  │  │ • Properties Table           │          │ • Indexes & Triggers   │   │
│  │  │ • Reviews Table              │          │ • Foreign Keys         │   │
│  │  │ • Categories Table           │          │ • Data Integrity       │   │
│  │  │ • Locations Table            │          │                        │   │
│  │  │ • Images Table               │          │                        │   │
│  │  └──────────────────────────────┤          │                        │   │
│  │                                 │          │                        │   │
│  └─────────────────────────────────┘          └────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

### Diagrama C4 - Nível 3: Componentes

#### Backend - Arquitetura em Camadas

```
┌──────────────────────────────────────────────────────────────┐
│                  Flask API (Backend)                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │         CAMADA DE APRESENTAÇÃO (Routes)                 │ │
│  │                                                         │ │
│  │  • /api/auth              (Login, Signup, Logout)       │ │
│  │  • /api/properties        (CRUD de Imóveis)             │ │
│  │  • /api/reviews           (CRUD de Avaliações)          │ │
│  │  • /api/users             (Gerenciamento de Usuários)   │ │
│  │  • /api/search            (Busca e Filtros)             │ │
│  │                                                         │ │
│  │  Responsabilidade: Mapear requisições HTTP para         │ │
│  │  operações de negócio. Validação inicial de entrada.    │ │
│  └─────────────────────────────────────────────────────────┘ │
│              │ Chamadas de Métodos                           │
│              ▼                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │       CAMADA DE NEGÓCIO (Services)                      │ │
│  │                                                         │ │
│  │  • AuthService             (Autenticação & JWT)         │ │
│  │  • PropertyService         (Lógica de Imóveis)          │ │
│  │  • ReviewService           (Lógica de Avaliações)       │ │
│  │  • UserService             (Lógica de Usuários)         │ │
│  │  • SearchService           (Busca & Filtros)            │ │
│  │  • ValidationService       (Regras de Validação)        │ │
│  │                                                         │ │
│  │  Responsabilidade: Implementar as regras de negócio,    │ │
│  │  lógica de validação, cálculos e orquestração de        │ │
│  │  operações complexas. Isoladas para fácil testagem.     │ │
│  └─────────────────────────────────────────────────────────┘ │
│              │ Acesso a Dados                                │
│              ▼                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │      CAMADA DE PERSISTÊNCIA (Models & ORM)              │ │
│  │                                                         │ │
│  │  • User Model              (Tabela users)               │ │
│  │  • Property Model          (Tabela properties)          │ │
│  │  • Review Model            (Tabela reviews)             │ │
│  │  • Category Model          (Tabela categories)          │ │
│  │  • Location Model          (Tabela locations)           │ │
│  │  • Image Model             (Tabela images)              │ │
│  │                                                         │ │
│  │  Responsabilidade: Definir a estrutura de dados,        │ │
│  │  mapear para tabelas do banco de dados (SQLAlchemy ORM).│ │
│  └─────────────────────────────────────────────────────────┘ │
│              │ SQL Queries                                   │
│              ▼                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │         CAMADA DE DADOS (Database)                      │ │
│  │                                                         │ │
│  │         MySQL 8.0+  (Persistent Storage)                │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### Frontend - Arquitetura Baseada em Componentes

```
┌──────────────────────────────────────────────────────────────┐
│                 React Frontend (SPA)                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │           CAMADA DE ROTEAMENTO                          │ │
│  │                                                         │ │
│  │  • React Router v6                                      │ │
│  │  • Proteção de Rotas (PrivateRoute)                     │ │
│  │  • Navegação SPA                                        │ │
│  │                                                         │ │
│  │  Responsabilidade: Mapear URLs para componentes,        │ │
│  │  gerenciar navegação entre páginas sem reload.          │ │
│  └─────────────────────────────────────────────────────────┘ │
│              │ Renderização de Componentes                   │
│              ▼                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │        CAMADA DE APRESENTAÇÃO (Pages & Components)      │ │
│  │                                                         │ │
│  │  Pages:                                                 │ │
│  │  • HomePage              (Listagem e busca de imóveis)  │ │
│  │  • PropertyDetailPage    (Detalhes do imóvel)           │ │
│  │  • LoginPage             (Autenticação)                 │ │
│  │  • RegisterPage          (Cadastro)                     │ │
│  │  • ReviewPage            (Avaliações)                   │ │
│  │  • AdminDashboard        (Painel administrativo)        │ │
│  │                                                         │ │
│  │  Components Reutilizáveis:                              │ │
│  │  • PropertyCard          (Card de imóvel)               │ │
│  │  • ReviewList            (Lista de avaliações)          │ │
│  │  • SearchBar             (Barra de busca)               │ │
│  │  • Navbar                (Navegação principal)          │ │
│  │  • Rating                (Componente de estrelas)       │ │
│  │  • Modal                 (Diálogos)                     │ │
│  │  • Form Elements         (Inputs, Buttons)              │ │
│  │                                                         │ │
│  │  Responsabilidade: Renderizar UI, capturar eventos      │ │
│  │  do usuário, exibir dados. Reutilização máxima.         │ │
│  └─────────────────────────────────────────────────────────┘ │
│              │ Chamadas HTTP                                 │
│              ▼                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │   CAMADA DE INTEGRAÇÃO (Services & API Client)          │ │
│  │                                                         │ │
│  │  • authService           (Autenticação com backend)     │ │
│  │  • propertyService       (Requisições de imóveis)       │ │
│  │  • reviewService         (Requisições de avaliações)    │ │
│  │  • userService           (Requisições de usuários)      │ │
│  │  • searchService         (Busca e filtros)              │ │
│  │  • apiClient (Axios)     (Interceptor HTTP)             │ │
│  │                                                         │ │
│  │  Responsabilidade: Abstrair chamadas HTTP, tratamento   │ │
│  │  de erros, interceptação de requisições (auth tokens).  │ │
│  └─────────────────────────────────────────────────────────┘ │
│              │ HTTP Requests                                 │
│              ▼                                               │
│         Flask API Backend                                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📋 Descrição dos Principais Componentes

### Backend (Flask API)

#### 🔐 **AuthService** (Autenticação)
- **Responsabilidade**: Gerenciar autenticação de usuários, geração e validação de JWT tokens
- **Operações Principais**:
  - Registro de novos usuários
  - Login com validação de credenciais
  - Renovação de tokens
  - Logout e revogação de sessões
- **Dependências**: SQLAlchemy User Model, JWT Library

#### 🏢 **PropertyService** (Gerenciamento de Imóveis)
- **Responsabilidade**: CRUD de imóveis, listagem e filtros avançados
- **Operações Principais**:
  - Criar novo imóvel
  - Atualizar informações de imóvel
  - Deletar imóvel (apenas proprietário)
  - Listar imóveis com paginação
  - Aplicar filtros (localização, preço, tipo)
- **Dependências**: SQLAlchemy Property Model, SearchService

#### ⭐ **ReviewService** (Avaliações e Comentários)
- **Responsabilidade**: Gerenciar avaliações de usuários sobre imóveis
- **Operações Principais**:
  - Criar avaliação para um imóvel
  - Editar avaliação própria
  - Deletar avaliação
  - Calcular média de avaliações
  - Retornar avaliações ordenadas por utilidade
- **Dependências**: SQLAlchemy Review Model, PropertyService

#### 👤 **UserService** (Gerenciamento de Usuários)
- **Responsabilidade**: Operações de perfil de usuário e gerenciamento
- **Operações Principais**:
  - Buscar perfil de usuário
  - Atualizar dados pessoais
  - Gerenciar tipos de usuário (Inquilino, Imobiliária, Admin)
  - Listar histórico de avaliações do usuário
- **Dependências**: SQLAlchemy User Model

#### 🔍 **SearchService** (Busca e Filtros)
- **Responsabilidade**: Implementar lógica de busca avançada e filtros
- **Operações Principais**:
  - Busca por texto (endereço, descrição)
  - Filtro por localização (cidade, bairro)
  - Filtro por faixa de preço
  - Filtro por tipo de imóvel
  - Ordenação (preço, avaliação, data)
  - Paginação de resultados
- **Dependências**: PropertyService, Database Queries

#### ✅ **ValidationService** (Validações)
- **Responsabilidade**: Centralizar regras de validação
- **Operações Principais**:
  - Validar formato de email
  - Validar força de senha
  - Validar dados de imóvel (campos obrigatórios)
  - Validar conteúdo de avaliação
  - Validar permissões de usuário
- **Dependências**: Nenhuma

### Frontend (React SPA)

#### 📄 **HomePage**
- **Responsabilidade**: Exibir lista de imóveis e interface de busca
- **Funcionalidades**:
  - Busca por texto
  - Filtros avançados (localização, preço)
  - Cards de imóveis com resumo
  - Paginação
  - Link para detalhes do imóvel
- **Componentes Utilizados**: SearchBar, PropertyCard, Filter, Pagination

#### 🔎 **PropertyDetailPage**
- **Responsabilidade**: Exibir informações completas de um imóvel
- **Funcionalidades**:
  - Galeria de imagens
  - Informações detalhadas (endereço, preço, descrição)
  - Média de avaliações
  - Lista de avaliações
  - Formulário para adicionar avaliação (se autenticado)
- **Componentes Utilizados**: ImageGallery, ReviewList, ReviewForm, RatingDisplay

#### 🔐 **LoginPage & RegisterPage**
- **Responsabilidade**: Autenticação e registro de usuários
- **Funcionalidades**:
  - Formulário de login com validação
  - Formulário de registro com confirmação de senha
  - Armazenamento de token no localStorage
  - Redirecionamento após sucesso
- **Componentes Utilizados**: Form, Button, ValidationMessages

#### ⭐ **ReviewPage**
- **Responsabilidade**: Interface para criar/editar avaliações
- **Funcionalidades**:
  - Formulário de avaliação com estrelas
  - Campo de comentário
  - Seleção de categoria (se aplicável)
  - Validação antes do envio
  - Feedback de sucesso/erro
- **Componentes Utilizados**: RatingInput, TextArea, SubmitButton

#### 👨‍💼 **AdminDashboard**
- **Responsabilidade**: Painel de controle para administradores
- **Funcionalidades**:
  - Estatísticas do sistema
  - Gerenciamento de usuários
  - Moderação de avaliações
  - Relatórios
- **Componentes Utilizados**: Chart, DataTable, Modal

---

## Fluxos Principais da Aplicação

### Fluxo 1: Busca e Visualização de Imóvel
```
1. Usuário acessa HomePage
2. Sistema carrega lista de imóveis (propertyService.getAll)
3. Usuário aplica filtros/busca (SearchService.search)
4. Sistema exibe PropertyCards filtrados
5. Usuário clica em um imóvel
6. Sistema carrega PropertyDetailPage (propertyService.getById)
7. Carrega avaliações (reviewService.getByProperty)
8. Exibe todas as informações
```

### Fluxo 2: Criação de Avaliação
```
1. Usuário autenticado acessa PropertyDetailPage
2. Clica em "Deixar Avaliação"
3. Abre formulário ReviewForm
4. Usuário preenche estrelas, comentário e categoria
5. Submete formulário
6. Frontend valida dados (ValidationService)
7. Envia POST para /api/reviews (reviewService.create)
8. Backend salva na BD (ReviewService.create)
9. Retorna sucesso
10. Frontend atualiza lista de avaliações
11. Recalcula média de rating
```

### Fluxo 3: Autenticação de Usuário
```
1. Usuário acessa LoginPage
2. Insere email e senha
3. Frontend valida formato (ValidationService)
4. Envia POST para /api/auth/login (authService.login)
5. Backend verifica credenciais
6. Se válido, gera JWT token
7. Frontend armazena token no localStorage
8. Configura header de autorização no Axios
9. Redireciona para HomePage
10. Usuário autenticado pode avaliar imóveis
```

---

## Diagram de Entidades (ER)

```
┌─────────────┐           ┌──────────────┐           ┌─────────────┐
│    Users    │           │ Properties   │           │   Reviews   │
├─────────────┤           ├──────────────┤           ├─────────────┤
│ id (PK)     │◄──────┐   │ id (PK)      │◄──────┐   │ id (PK)     │
│ email       │       │   │ title        │       │   │ rating      │
│ password    │       │1:N│ description  │      1:N  │ comment     │
│ name        │       │   │ price        │       │   │ date        │
│ type        │       │   │ address      │       │   │ user_id(FK) │
│ created_at  │       │   │ location_id  │       │   │ property_id │
└─────────────┘       │   │ user_id (FK) │       │   └─────────────┘
                      │   │ created_at   │       │
                      │   └──────────────┘       │
                      │          │               │
                      │        1:N              1:N
                      │          │               │
                      │   ┌──────────────┐       │
                      │   │   Images     │       │
                      │   ├──────────────┤       │
                      │   │ id (PK)      │       │
                      │   │ url          │       │
                      │   │ property_id  │───────┘
                      │   │ (FK)         │
                      │   └──────────────┘
                      │
                      │   ┌──────────────┐
                      ├──→│  Locations   │
                          ├──────────────┤
                          │ id (PK)      │
                          │ street       │
                          │ number       │
                          │ city         │
                          │ neighborhood │
                          └──────────────┘
```

---

## Diagram de Dados

```
┌──────────────────────────────────────────────────────────┐
│              Frontend (React SPA)                        │
│  ┌───────────────────────────────────────────────────────┤
│  │ localStorage:                                         │
│  │ - authToken (JWT)                                     │
│  │ - user (JSON serializado)                             │
│  │ - preferences (tema, idioma)                          │
│  └───────────────────────────────────────────────────────┤
│         │ HTTP with Bearer Token                         │
│         ▼                                                │
│ ┌────────────────────────────────────────────────────────┐
│ │            Backend (Flask API)                         │
│ │  ┌───────────────────────────────────────────────────┤ │
│ │  │ Session Memory:                                   │ │
│ │  │ - Request context (user_id from JWT)              │ │
│ │  │ - Temporary cache                                 │ │
│ │  └───────────────────────────────────────────────────┤ │
│ │         │ SQL Queries                                │ │
│ │         ▼                                            │ │
│ │  ┌───────────────────────────────────────────────────┐ │
│ │  │      MySQL Database (Persistent)                  │ │
│ │  │                                                   │ │
│ │  │  - users (id, email, password_hash, name, type)   │ │
│ │  │  - properties (id, title, price, user_id, ...)    │ │
│ │  │  - reviews (id, rating, comment, user_id, ...)    │ │
│ │  │  - locations (id, street, city, ...)              │ │
│ │  │  - images (id, url, property_id, ...)             │ │
│ │  │  - categories (id, name, description)             │ │
│ │  │                                                   │ │
│ │  └───────────────────────────────────────────────────┘ │
│ │                                                        │
│ └────────────────────────────────────────────────────────┘
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## ��� Diagrama de Classes

**User**: Usuário da aplicação, que pode ser pessoa ou empresa.

**Property**: Imóvel cadastrado na plataforma, com atributos como endereço e descrição.

**Category**: Categoria de avaliação (vizinhança, localização, etc.).

**Review**: Avaliação feita por um usuário sobre um imóvel, associada a uma categoria específica. Ou então uma avaliação geral do imóvel.

**Location**: Localização do imóvel, com atributos como rua e número.

**Image**: Imagens associadas a um imóvel, com atributos como URL e descrição.


![alt text](util/class_diagram.png)

## ▶️ Como dar Run a Aplicação
### Back-end (Flask API)
1. Navegue até a pasta `backend`:
   ```bash
   cd backend
   ```
2. Suba o banco de dados com o Docker:
   ```bash
   docker compose up -d
   ```   
2. Crie um ambiente virtual e ative-o:
   ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o servidor:
    ```bash
    python run.py
    ```
### Front-end (React)
1. Navegue até a pasta `frontend`:
   ```bash
   cd frontend
   ```
2. Instale as dependências:
    ```bash
    npm install
    ```
3. Faça a build da aplicação:
    ```bash
    npm run build
    ```
4. Inicie a aplicação:
    ```bash
    npm run dev
    ```
