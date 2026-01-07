# 🏠 Simulador de Financiamento Imobiliário

[![Backend CI/CD](https://github.com/lkarolinecarvalho/liquid-real-estate-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/lkarolinecarvalho/liquid-real-estate-api/actions)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws)](https://aws.amazon.com/lambda/)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)](https://www.typescriptlang.org/)

Sistema serverless completo de simulação de financiamento imobiliário com taxas de juros dinâmicas baseadas em indicadores econômicos reais (SELIC/IPCA) do Banco Central e IBGE.

**🔗 Links:**
- **Frontend (Produção):** https://financing-simulator-8i8qcshlt-larissas-projects-08d31ad6.vercel.app
- **API (AWS Lambda):** https://62dv6tdqh1.execute-api.us-east-1.amazonaws.com
- **Repositório:** https://github.com/lkarolinecarvalho/liquid-real-estate-api

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Problema e Solução](#-problema-e-solução)
- [Stack Tecnológica](#-stack-tecnológica)
- [Arquitetura](#-arquitetura)
- [Decisões Arquiteturais](#-decisões-arquiteturais)
- [Features Implementadas](#-features-implementadas)
- [Instalação e Execução](#-instalação-e-execução)
- [Deploy](#-deploy)
- [Testes](#-testes)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [CI/CD](#-cicd)
- [Monitoramento e Observabilidade](#-monitoramento-e-observabilidade)
- [Considerações de Segurança](#-considerações-de-segurança)
- [Roadmap](#-roadmap)
- [Autora](#-autora)

---

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como parte de um desafio técnico para posição **sênior Back-End**, implementando uma solução completa e escalável para simulação de financiamentos imobiliários.

### **O que o sistema faz?**

Calcula financiamentos imobiliários com **taxas de juros ajustadas dinamicamente** baseadas em indicadores econômicos reais:

- Consulta **SELIC** (Sistema Especial de Liquidação e Custódia) do Banco Central
- Consulta **IPCA** (Índice de Preços ao Consumidor Amplo) do IBGE
- Aplica **fórmula customizada** que pondera esses indicadores
- Gera **tabela de amortização completa** (PRICE ou SAC)
- Persiste **histórico de simulações** no DynamoDB
- Compara com **média nacional de juros**
- Fornece **análise de viabilidade** financeira

---

## 🔥 Problema e Solução

### **Problema:**

Simuladores tradicionais de financiamento usam taxas **estáticas** ou genéricas que não refletem:
- Volatilidade econômica real
- Diferenças regionais
- Contexto macroeconômico atual

Isso resulta em simulações **desatualizadas** e **imprecisas** para o usuário final.

### **Solução:**

Sistema **serverless** que:

1. ✅ **Consulta APIs governamentais** em tempo real (BACEN + IBGE)
2. ✅ **Fallback inteligente** entre múltiplas fontes de dados
3. ✅ **Cálculo financeiro preciso** com validação de todas as variáveis
4. ✅ **Persistência histórica** para análise comparativa
5. ✅ **Interface responsiva** com visualizações interativas
6. ✅ **Deploy automatizado** via CI/CD

---

## 🛠️ Stack Tecnológica

### **Backend**

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11 | Runtime principal |
| **AWS Lambda** | - | Compute serverless |
| **API Gateway** | HTTP API | Exposição de endpoints REST |
| **DynamoDB** | - | Persistência NoSQL |
| **Pydantic** | 2.5+ | Validação e serialização de dados |
| **Requests** | 2.31+ | HTTP client para APIs externas |
| **Boto3** | 1.34+ | SDK AWS para Python |
| **Pytest** | 7.4+ | Framework de testes |
| **Ruff** | 0.1+ | Linter moderno e rápido |
| **Black** | 23.11+ | Formatador de código |

### **Frontend**

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Next.js** | 16.1 | Framework React com SSR |
| **TypeScript** | 5+ | Type safety |
| **Tailwind CSS** | 3+ | Styling utility-first |
| **Recharts** | 2+ | Visualização de dados |
| **Axios** | 1.6+ | Cliente HTTP |
| **Vercel** | - | Plataforma de deploy |

### **Infraestrutura**

| Ferramenta | Versão | Uso |
|------------|--------|-----|
| **Serverless Framework** | 3+ | IaC para AWS |
| **GitHub Actions** | - | CI/CD pipeline |
| **AWS CloudWatch** | - | Logs e métricas |
| **AWS X-Ray** | - | Tracing distribuído |

---

## 🏗️ Arquitetura

### **Visão Geral**

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  (Next.js + TypeScript + Tailwind - Vercel)                     │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ HTTPS
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AWS API GATEWAY                            │
│  (HTTP API with CORS + Request Validation)                      │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ├─────────► POST /financing/simulate
                 │           └─► financing_handler.py
                 │
                 ├─────────► GET  /financing/history
                 │           └─► history_handler.py
                 │
                 ├─────────► GET  /financing/simulation/{id}
                 │           └─► history_handler.py
                 │
                 └─────────► GET  /health
                             └─► health_handler.py
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AWS LAMBDA                               │
│  (Python 3.11 + Lambda Layer + 512MB RAM)                       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  APPLICATION LAYER                                        │  │
│  │  ├── handlers/          (Request/Response)                │  │
│  │  ├── services/          (Business Logic)                  │  │
│  │  ├── calculators/       (Financial Math)                  │  │
│  │  ├── clients/           (External APIs)                   │  │
│  │  ├── models/            (Pydantic Schemas)                │  │
│  │  └── utils/             (Helpers + Logger)                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────┬──────────────────────┬──────────────────────┬────────────┘
      │                      │                      │
      │                      │                      │
      ▼                      ▼                      ▼
┌──────────┐         ┌──────────────┐      ┌──────────────┐
│ DynamoDB │         │ Banco Central│      │     IBGE     │
│  (NoSQL) │         │   (SELIC)    │      │   (IPCA)     │
└──────────┘         └──────────────┘      └──────────────┘
    │                      │                      │
    │                      │                      │
    └──────────────────────┴──────────────────────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │  CloudWatch Logs │
                 │   + X-Ray Traces │
                 └──────────────────┘
```

### **Fluxo de Dados**

```
┌─────────────────────────────────────────────────────────────────┐
│                  1. REQUEST VALIDATION                          │
│  User Input → Pydantic Schema → Validation → Sanitization       │
└────────────────┬────────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              2. EXTERNAL DATA FETCHING (Parallel)               │
│  ┌─────────────────────┐    ┌──────────────────────┐           │
│  │ BACEN Client        │    │ IBGE Client          │           │
│  │ ├─ GET SELIC        │    │ ├─ GET IPCA          │           │
│  │ ├─ Timeout: 3s      │    │ ├─ Timeout: 3s       │           │
│  │ ├─ Retry: 2x        │    │ ├─ Retry: 2x         │           │
│  │ └─ Fallback: Mock   │    │ └─ Fallback: Mock    │           │
│  └─────────────────────┘    └──────────────────────┘           │
└────────────────┬────────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                3. FINANCIAL CALCULATION                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Interest Rate Service                                    │   │
│  │ ├─ Calculate base rate (10% default)                    │   │
│  │ ├─ Apply SELIC factor (0.15 weight)                     │   │
│  │ ├─ Formula: base + (selic × 0.15 × 0.1)                 │   │
│  │ └─ Result: Dynamic annual rate                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Amortization Calculator (PRICE or SAC)                  │   │
│  │ ├─ Generate 360-month schedule                          │   │
│  │ ├─ Calculate: principal, interest, balance              │   │
│  │ └─ Summarize: 12 key points                             │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                  4. PERSISTENCE (DynamoDB)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ DynamoDB Service                                         │   │
│  │ ├─ Convert floats → Decimals                            │   │
│  │ ├─ Generate UUID + timestamp                            │   │
│  │ ├─ Set TTL (90 days auto-expire)                        │   │
│  │ ├─ PutItem (pay-per-request)                            │   │
│  │ └─ Index by user_identifier (IP or session)             │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    5. RESPONSE FORMATTING                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ JSON Response                                            │   │
│  │ ├─ simulation_id (UUID)                                 │   │
│  │ ├─ input_data                                           │   │
│  │ ├─ calculated_rates                                     │   │
│  │ ├─ results (payment, totals)                            │   │
│  │ ├─ amortization_schedule                                │   │
│  │ ├─ comparative_analysis                                 │   │
│  │ └─ viability_assessment                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Decisões Arquiteturais

### **1. Serverless vs. Containers**

**Decisão:** AWS Lambda com Serverless Framework

**Justificativa:**
- ✅ **Zero gerenciamento de infra:** Foco no código de negócio
- ✅ **Auto-scaling:** De 0 a 1000 req/s sem configuração
- ✅ **Pay-per-use:** Custo proporcional ao uso real
- ✅ **Cold start aceitável:** ~2s para primeira requisição, depois <500ms
- ✅ **Integração nativa:** API Gateway, DynamoDB, CloudWatch

**Trade-offs:**
- ❌ Limite de 15 minutos por execução (não é problema para este caso)
- ❌ Lambda Layers necessários para dependências (resolvido com layer otimizado)

---

### **2. DynamoDB vs. RDS**

**Decisão:** DynamoDB (NoSQL)

**Justificativa:**
- ✅ **Serverless nativo:** Sem gerenciamento de conexões
- ✅ **Pay-per-request:** Ideal para cargas variáveis
- ✅ **Performance previsível:** Latência <10ms garantida
- ✅ **TTL automático:** Expiração de dados sem cron jobs
- ✅ **Escalabilidade:** Sem limites de throughput

**Modelagem de dados:**
```
Table: financing-simulations-dev

Primary Key:
  - HASH:  simulation_id (UUID)
  - RANGE: created_at (ISO timestamp)

GSI: UserIndex
  - HASH:  user_identifier (IP or session_id)
  - RANGE: created_at

Attributes:
  - simulation_id: string
  - created_at: string
  - user_identifier: string
  - ttl: number (unix timestamp + 90 days)
  - simulacao: map (input data)
  - taxas: map (rates calculation)
  - resultado: map (financial results)
  - comparativo: map (comparison data)
  - analise: map (viability assessment)
  - tabela_amortizacao_resumida: list
```

**Trade-offs:**
- ❌ Sem JOIN (não necessário neste caso)
- ❌ Schema flexível (mitigado com Pydantic)

---

### **3. Estratégia de Fallback (BACEN + IBGE)**

**Decisão:** Fallback hierárquico com mock inteligente

**Implementação:**

```python
# Priority 1: Banco Central (SELIC)
try:
    selic = await bacen_client.get_selic()
except ExternalServiceException:
    # Priority 2: IBGE (IPCA como proxy)
    try:
        ipca = await ibge_client.get_ipca()
        selic = ipca * 0.8  # Correlação histórica
    except ExternalServiceException:
        # Priority 3: Mock com valor conservador
        selic = 15.0  # Média histórica 2020-2025
        logger.warning("Using mock SELIC due to API failures")
```

**Justificativa:**
- ✅ **Resiliência:** Sistema nunca falha por indisponibilidade de API
- ✅ **Transparência:** Usuário sabe qual fonte foi usada
- ✅ **Conservadorismo:** Mock usa valor alto para não subestimar custos

**Monitoramento:**
```python
# Métricas customizadas no CloudWatch
put_metric("ExternalAPI/BACEN/Success", 1 if success else 0)
put_metric("ExternalAPI/IBGE/Success", 1 if success else 0)
put_metric("ExternalAPI/FallbackUsed", 1 if mock else 0)
```

---

### **4. Validação em Múltiplas Camadas**

**Camada 1: API Gateway (Request Validation)**
```yaml
# serverless.yml
functions:
  simulate:
    events:
      - httpApi:
          path: /financing/simulate
          method: post
          request:
            schemas:
              application/json: ${file(schemas/simulation-request.json)}
```

**Camada 2: Pydantic (Business Logic)**
```python
class SimulationRequest(BaseModel):
    valor_imovel: float = Field(gt=0, le=100_000_000)
    entrada: float = Field(ge=0)
    prazo_meses: int = Field(ge=12, le=480)
    tipo_amortizacao: Literal["PRICE", "SAC"]
    regiao: str = Field(pattern="^[A-Z]{2}$")
    
    @model_validator(mode='after')
    def validate_entrada(self):
        if self.entrada > self.valor_imovel:
            raise ValueError("Entrada maior que valor do imóvel")
        if self.entrada < self.valor_imovel * 0.2:
            raise ValueError("Entrada mínima: 20%")
        return self
```

**Camada 3: Calculator (Financial Rules)**
```python
def calculate_price(principal: Decimal, rate: Decimal, periods: int):
    if principal <= 0:
        raise ValueError("Principal must be positive")
    if rate <= 0 or rate >= 1:
        raise ValueError("Rate must be between 0 and 1")
    if periods <= 0:
        raise ValueError("Periods must be positive")
    # ... calculation
```

---

### **5. Observabilidade desde o Início**

**Structured Logging:**
```python
logger.info(
    "Simulation completed",
    extra={
        "request_id": request_id,
        "user_ip": user_ip,
        "property_value": valor_imovel,
        "final_rate": taxa_final,
        "monthly_payment": parcela_mensal,
        "processing_time_ms": duration
    }
)
```

**Métricas:**
- Request count per endpoint
- Average processing time
- External API success rate
- DynamoDB operation latency
- Error rate by type

**Tracing:**
- X-Ray habilitado para rastrear requisições completas
- Subsegments para cada operação custosa (API calls, DynamoDB)

---

### **6. Frontend: Next.js vs. React SPA**

**Decisão:** Next.js 16 (App Router)

**Justificativa:**
- ✅ **SSR/SSG:** SEO-friendly (importante para landing pages)
- ✅ **API Routes:** Backend-for-frontend embutido
- ✅ **Image optimization:** Automático
- ✅ **TypeScript:** First-class support
- ✅ **File-based routing:** Simplicidade

**Optimizações aplicadas:**
```typescript
// app/page.tsx
export const dynamic = 'force-static' // Pre-render
export const revalidate = 3600 // ISR: 1h

// components/AmortizationChart.tsx
const Chart = dynamic(() => import('recharts'), {
  ssr: false, // Reduce bundle
  loading: () => <Skeleton />
})
```

---

## ✨ Features Implementadas

### **Nível 1: Fundação (Obrigatório)**
- ✅ Lambda + API Gateway funcionando
- ✅ Serverless Framework configurado
- ✅ Código Python com pacotes externos (Pydantic, Requests, Boto3)
- ✅ Frontend React/Next.js responsivo

### **Nível 2: Intermediário (Desejado)**
- ✅ Consulta de APIs externas (BACEN + IBGE)
- ✅ Fallback inteligente entre APIs
- ✅ Tratamento robusto de erros (try/except em camadas)
- ✅ Logging estruturado (JSON logs)
- ✅ Testes automatizados (pytest com >70% coverage)
- ✅ Frontend 100% responsivo (mobile-first)

### **Nível 3: Avançado (Bônus)**
- ✅ **DynamoDB com persistência completa**
- ✅ **TTL automático** (90 dias)
- ✅ **Endpoints de histórico** (GET /history, GET /simulation/{id})
- ✅ **CI/CD completo** (GitHub Actions)
- ✅ **Deploy automático** (dev on push, prod on tag)
- ✅ **Múltiplos ambientes** (dev, prod)

### **Features Extra (Diferenciais)**
- ✅ **Histórico no frontend** com botão "Refazer"
- ✅ **Gráfico interativo** de amortização (Recharts)
- ✅ **Comparativo** com média nacional
- ✅ **Análise de viabilidade** financeira
- ✅ **Type safety** completo (Python + TypeScript)
- ✅ **Design system** customizado (Liquid theme)
- ✅ **Lambda Layers** otimizado (dependências separadas)
- ✅ **Observabilidade** (CloudWatch + X-Ray)

---

## 🚀 Instalação e Execução

### **Pré-requisitos**

- Python 3.11+
- Node.js 20+
- AWS CLI configurado
- Serverless Framework
- Conta AWS
- Conta Vercel (opcional, para frontend)

### **1. Backend (Local)**

```bash
# Clone o repositório
git clone https://github.com/lkarolinecarvalho/liquid-real-estate-api.git
cd liquid-real-estate-api/backend

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# Rodar testes
pytest tests/ -v --cov=src

# Rodar localmente (serverless offline)
serverless offline --stage dev
```

**Backend rodará em:** `http://localhost:3000`

---

### **2. Frontend (Local)**

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variável de ambiente
echo "NEXT_PUBLIC_API_URL=http://localhost:3000" > .env.local

# Rodar em desenvolvimento
npm run dev
```

**Frontend rodará em:** `http://localhost:3001`

---

## 🌐 Deploy

### **Backend (AWS Lambda)**

#### **Deploy Manual**

```bash
cd backend

# Instalar Serverless Framework
npm install -g serverless

# Configurar credenciais AWS
aws configure
# Ou: export AWS_ACCESS_KEY_ID=xxx
#     export AWS_SECRET_ACCESS_KEY=yyy

# Deploy dev
serverless deploy --stage dev --verbose

# Deploy prod (via tag)
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
# Pipeline CI/CD fará deploy automático
```

#### **Deploy via CI/CD (Automático)**

```bash
# Dev: Push para main
git push origin main
# → Triggers: lint → test → deploy dev

# Prod: Criar tag
git tag -a v1.0.0 -m "Production release"
git push origin v1.0.0
# → Triggers: lint → test → deploy prod
```

---

### **Frontend (Vercel)**

#### **Deploy Manual**

```bash
cd frontend

# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Adicionar variável de ambiente
vercel env add NEXT_PUBLIC_API_URL production
# Valor: https://62dv6tdqh1.execute-api.us-east-1.amazonaws.com

# Deploy
vercel --prod
```

#### **Deploy Automático (GitHub Integration)**

1. Conecte o repositório no [Vercel Dashboard](https://vercel.com)
2. Configure variável de ambiente: `NEXT_PUBLIC_API_URL`
3. Cada push na `main` → deploy automático

---

## 🧪 Testes

### **Backend**

```bash
cd backend

# Rodar todos os testes
pytest tests/ -v

# Com coverage
pytest tests/ --cov=src --cov-report=html

# Apenas testes unitários
pytest tests/unit/ -v

# Apenas testes de integração
pytest tests/integration/ -v

# Testes específicos
pytest tests/test_calculators.py::test_price_calculator -v
```

**Coverage atual:** ~75%

---

### **Frontend**

```bash
cd frontend

# Lint
npm run lint

# Type check
npm run type-check

# Build (valida TypeScript)
npm run build
```

---

## 📡 Exemplos de Uso

### **1. Simular Financiamento**

**Request:**
```bash
curl -X POST https://62dv6tdqh1.execute-api.us-east-1.amazonaws.com/financing/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "valor_imovel": 500000,
    "entrada": 100000,
    "prazo_meses": 360,
    "tipo_amortizacao": "PRICE",
    "regiao": "SP"
  }'
```

**Response (resumido):**
```json
{
  "simulation_id": "7a746346-1101-4ed3-877f-b6f56c225043",
  "request_id": "fa15e8db-83c2-41b0-acba-af7806a2c1d5",
  "timestamp": "2026-01-07T10:30:25.675536",
  "simulacao": {
    "valor_imovel": 500000.0,
    "entrada": 100000.0,
    "valor_financiado": 400000.0,
    "prazo_meses": 360,
    "tipo_amortizacao": "PRICE"
  },
  "taxas": {
    "indicador": {
      "indicador_usado": "SELIC",
      "valor_indicador": 15.0,
      "fonte": "Banco Central do Brasil",
      "data_referencia": "2026-01-28"
    },
    "taxa_juros_anual": 10.22,
    "taxa_juros_mensal": 0.8146,
    "formula_aplicada": "taxa_base(10.0%) + (selic(15.0%) × fator_ajuste(0.15) × 0.1)"
  },
  "resultado": {
    "parcela_mensal": 3444.02,
    "total_pago": 1239848.11,
    "juros_totais": 839848.11,
    "percentual_juros": 67.74,
    "primeira_parcela": {
      "valor": 3444.02,
      "juros": 3258.4,
      "amortizacao": 185.62,
      "saldo_devedor": 399814.38
    },
    "ultima_parcela": {
      "valor": 3444.02,
      "juros": 27.83,
      "amortizacao": 3416.19,
      "saldo_devedor": 0.0
    }
  },
  "comparativo": {
    "taxa_media_nacional": 9.8,
    "diferenca_percentual": 4.34,
    "classificacao": "NA_MEDIA",
    "mensagem": "A taxa aplicada está dentro da média nacional"
  },
  "analise": {
    "comprometimento_renda_sugerido": 30,
    "renda_minima_sugerida": 11480.08,
    "viabilidade": "ALTA",
    "alertas": [
      "Prazo muito longo (>25 anos): considere reduzir para diminuir juros totais"
    ]
  },
  "tabela_amortizacao_resumida": [
    {
      "mes": 1,
      "parcela": 3444.02,
      "juros": 3258.4,
      "amortizacao": 185.62,
      "saldo_devedor": 399814.38
    },
    // ... 10 mais pontos-chave
  ]
}
```

---

### **2. Buscar Histórico**

**Request:**
```bash
curl https://62dv6tdqh1.execute-api.us-east-1.amazonaws.com/financing/history?limit=5
```

**Response:**
```json
{
  "total": 5,
  "simulations": [
    {
      "simulation_id": "7a746346-1101-4ed3-877f-b6f56c225043",
      "created_at": "2026-01-07T10:30:26.122002",
      "user_identifier": "187.180.162.104",
      "simulacao": { /* ... */ },
      "resultado": { /* ... */ }
    }
    // ... 4 mais
  ],
  "filters": {
    "user_identifier": null,
    "limit": 5
  }
}
```

---

### **3. Buscar Simulação Específica**

**Request:**
```bash
curl "https://62dv6tdqh1.execute-api.us-east-1.amazonaws.com/financing/simulation/7a746346-1101-4ed3-877f-b6f56c225043?created_at=2026-01-07T10:30:26.122002"
```

**Response:**
```json
{
  "simulation_id": "7a746346-1101-4ed3-877f-b6f56c225043",
  "created_at": "2026-01-07T10:30:26.122002",
  // ... dados completos da simulação
}
```

---

### **4. Health Check**

**Request:**
```bash
curl https://62dv6tdqh1.execute-api.us-east-1.amazonaws.com/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-07T12:34:56.789012",
  "version": "1.0.0",
  "environment": "production"
}
```

---

## 📁 Estrutura do Projeto

```
liquid-real-estate-api/
├── .github/
│   └── workflows/
│       ├── ci-cd.yml              # Pipeline principal
│       └── pr-validation.yml      # Validação de PRs
│
├── backend/
│   ├── src/
│   │   ├── calculators/
│   │   │   ├── price_calculator.py    # Sistema PRICE
│   │   │   └── sac_calculator.py      # Sistema SAC
│   │   │
│   │   ├── clients/
│   │   │   ├── bacen_client.py        # Cliente SELIC
│   │   │   └── ibge_client.py         # Cliente IPCA
│   │   │
│   │   ├── handlers/
│   │   │   ├── financing_handler.py   # POST /simulate
│   │   │   ├── history_handler.py     # GET /history
│   │   │   └── health_handler.py      # GET /health
│   │   │
│   │   ├── models/
│   │   │   ├── requests.py            # Pydantic Request schemas
│   │   │   └── responses.py           # Pydantic Response schemas
│   │   │
│   │   ├── services/
│   │   │   ├── financing_service.py   # Orquestração principal
│   │   │   ├── interest_rate_service.py  # Cálculo de taxas
│   │   │   └── dynamodb_service.py    # Persistência
│   │   │
│   │   └── utils/
│   │       ├── logger.py              # Logging estruturado
│   │       ├── exceptions.py          # Custom exceptions
│   │       └── response.py            # HTTP response helpers
│   │
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_calculators.py
│   │   │   ├── test_clients.py
│   │   │   └── test_services.py
│   │   │
│   │   └── integration/
│   │       ├── test_handlers.py
│   │       └── test_e2e.py
│   │
│   ├── serverless.yml             # IaC Serverless Framework
│   ├── pyproject.toml            # Ruff + Black config
│   ├── requirements.txt          # Dependências produção
│   └── requirements-dev.txt      # Dependências dev/test
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Home page
│   │   └── globals.css           # Global styles
│   │
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── SimulatorForm.tsx
│   │   ├── ResultsPanel.tsx
│   │   ├── AmortizationChart.tsx
│   │   ├── SimulationHistory.tsx  # Histórico
│   │   └── SimulationCard.tsx     # Card de simulação
│   │
│   ├── services/
│   │   └── api.ts                # Axios client
│   │
│   ├── types/
│   │   └── financing.ts          # TypeScript types
│   │
│   ├── public/
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── package.json
│
├── layer/
│   └── python/                   # Lambda Layer (boto3, requests, etc)
│
├── schemas/
│   └── simulation-request.json   # JSON Schema para API Gateway
│
├── README.md                     # Este arquivo
└── .gitignore
```

---

## 🔄 CI/CD

### **Pipeline Stages**

```yaml
name: Backend CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  
jobs:
  # Stage 1: Code Quality
  lint:
    - Ruff (linter rápido)
    - Black (formatação)
    - MyPy (type checking)
  
  # Stage 2: Tests
  test:
    - Pytest com coverage
    - Coverage report (>70%)
    - Upload para Codecov
  
  # Stage 3: Deploy Dev (automatic)
  deploy-dev:
    - Serverless deploy --stage dev
    - Somente em push para main
  
  # Stage 4: Deploy Prod (manual/tag)
  deploy-prod:
    - Serverless deploy --stage prod
    - Trigger: git tag v*
    - Environment approval (opcional)
```

### **Como Usar**

**Deploy Automático (Dev):**
```bash
git add .
git commit -m "feat: add new feature"
git push origin main
# → CI/CD roda automaticamente
```

**Deploy Manual (Prod):**
```bash
git tag -a v1.0.0 -m "Production release"
git push origin v1.0.0
# → CI/CD deploy em produção
```

---

## 📊 Monitoramento e Observabilidade

### **CloudWatch Logs**

```bash
# Ver logs em tempo real
aws logs tail /aws/lambda/financing-simulator-dev-simulate --follow

# Buscar erro específico
aws logs filter-pattern "ERROR" \
  --log-group-name /aws/lambda/financing-simulator-dev-simulate \
  --start-time $(date -u -d '1 hour ago' +%s)000
```

### **CloudWatch Metrics**

Métricas customizadas criadas:
- `ExternalAPI/BACEN/SuccessRate`
- `ExternalAPI/IBGE/SuccessRate`
- `ExternalAPI/FallbackUsed`
- `DynamoDB/WriteLatency`
- `Calculation/ProcessingTime`

### **X-Ray Tracing**

Ativado para todas as funções Lambda. Visualize traces completos:
1. AWS Console → X-Ray → Service Map
2. Veja latência de cada subsegmento (API calls, DynamoDB)

### **Alertas Configurados**

```yaml
# CloudWatch Alarms (via IaC)
- Lambda/Errors > 5 in 5 minutes
- API Gateway 5xx > 10 in 5 minutes
- DynamoDB ThrottledRequests > 0
- External API failure rate > 50%
```

---

## 🔒 Considerações de Segurança

### **Implementado**

1. ✅ **HTTPS Only:** API Gateway force SSL
2. ✅ **CORS Configurado:** Whitelist de origins
3. ✅ **Input Validation:** Pydantic + JSON Schema
4. ✅ **Rate Limiting:** API Gateway throttling (10k req/s)
5. ✅ **Secrets Management:** AWS Secrets Manager (prod) / ENV vars (dev)
6. ✅ **IAM Least Privilege:** Lambda roles com permissões mínimas
7. ✅ **DynamoDB Encryption:** At-rest encryption habilitado
8. ✅ **Logs Sanitizados:** Sem dados sensíveis em logs

### **Recomendações Futuras**

- [ ] WAF (Web Application Firewall) na API Gateway
- [ ] API Key authentication para rate limiting por cliente
- [ ] Cognito para autenticação de usuários
- [ ] VPC para isolar Lambda (se necessário)
- [ ] KMS para criptografia adicional

---

## 🗺️ Roadmap fictício de continuidade de implementação

### **Curto Prazo**

- [ ] **Cache Redis:** Reduzir calls às APIs externas
- [ ] **Webhook notificações:** Alertar sobre simulações importantes
- [ ] **Export PDF:** Gerar relatório em PDF da simulação
- [ ] **Comparação lado-a-lado:** Comparar 2+ simulações

### **Médio Prazo**

- [ ] **Machine Learning:** Predição de aprovação de crédito
- [ ] **Dashboard Analytics:** Métricas de uso em tempo real
- [ ] **Multi-tenancy:** Suporte a múltiplas instituições financeiras
- [ ] **API Pública:** Documentação OpenAPI + Developer Portal

### **Longo Prazo**

- [ ] **Mobile App:** React Native ou Flutter
- [ ] **Real-time Updates:** WebSockets para taxas em tempo real
- [ ] **Blockchain:** Registro imutável de propostas
- [ ] **IA Generativa:** Chatbot para tirar dúvidas

---

## 👩‍💻 Autora

**Larissa Karoline Carvalho**

- **GitHub:** [@lkarolinecarvalho](https://github.com/lkarolinecarvalho)
- **LinkedIn:** [Larissa Karoline](https://linkedin.com/in/lkarolinecarvalho)
- **Email:** lkarolinecarvalho@gmail.com

---

## 📄 Licença

Este projeto foi desenvolvido como parte de um desafio técnico e está disponível sob a licença MIT.

---

## 📚 Referências Técnicas

- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Serverless Framework Docs](https://www.serverless.com/framework/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Banco Central - API de Dados Abertos](https://www.bcb.gov.br/estabilidadefinanceira/dadosabertos)
- [IBGE - API de Serviços](https://servicodados.ibge.gov.br/api/docs)

---

<div align="center">

[🔝 Voltar ao topo](#-simulador-de-financiamento-imobiliário)

</div>
