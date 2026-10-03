# SLM Assistente de Manutenção do Carro

## Visão geral

Projeto de estudo voltado ao uso de **Small Language Models (SLMs)** em um assistente de manutenção automotiva.

O objetivo é explorar uma arquitetura híbrida em que o SLM seja responsável pela geração de linguagem natural, enquanto fatos críticos permanecem ancorados em dados estruturados e mecanismos determinísticos.

Princípios do projeto:

- Clean Architecture simplificada
- SOLID
- Injeção de dependências
- Separação entre domínio, aplicação, infraestrutura e apresentação
- Testes unitários e de integração
- Benchmarks de qualidade, latência e fallback
- Uso local de modelos via Ollama
- Evolução incremental, evitando abstrações prematuras

---

# Arquitetura atual

```text
CLI
 ↓
AssistantService
 ├─ IntentClassifier
 ├─ QuestionClassifier
 ├─ VehicleQueryService
 └─ ResponseGenerator
       ↓
   HybridResponseGenerator
       ├─ SLM ResponseGenerator
       ├─ ResponseValidationService
       └─ Rule Based fallback
```

## Componentes principais

### AssistantService

Orquestra o fluxo da aplicação:

1. recebe a pergunta;
2. classifica a intenção;
3. classifica o tipo da pergunta;
4. consulta dados estruturados do veículo;
5. envia um `VehicleAnswer` ao `ResponseGenerator`;
6. retorna a resposta final.

Também trata:

- intents não suportados;
- tipos de pergunta não suportados;
- ausência de dados do veículo.

### VehicleQueryService

Consulta dados estruturados do veículo de acordo com `QuestionType`.

Atualmente suporta, entre outros:

- óleo do motor;
- pressão dos pneus;
- medida dos pneus.

Quando o dado conhecido não está disponível, lança `VehicleDataNotFoundError`.

### HybridResponseGenerator

```text
SLM
 ↓
ResponseValidationService
 ├─ válido   → retorna resposta do SLM
 └─ inválido → fallback determinístico
```

Também executa fallback quando o gerador principal lança exceção.

### ResponseValidationService

Valida fatos presentes na resposta gerada.

Cobertura atual:

- viscosidade de óleo (`5W-40`);
- pressão em PSI;
- pressão em bar;
- medida de pneus;
- múltiplos fatos na mesma resposta;
- normalização simples, como `2,2 bar` e `2.2 bar`.

### FallbackMetrics

Métricas atuais:

- total;
- respostas aceitas do SLM;
- fallbacks;
- fallback rate.

---

# Composition Root

A montagem das dependências permanece centralizada em:

```text
slm_assistentemanutencaocarro/infrastructure/composition.py
```

O `composition.py` sabe **como montar** a aplicação.

O entrypoint apenas inicia o sistema:

```text
main / __init__
 ↓
build_assistant()
 ↓
CLI
```

`Settings()` continua sendo utilizado no composition root para configurações externas.

---

# Benchmarks

Estrutura consolidada:

```text
benchmark/
├── benchmark/
│   ├── intent_classifier_benchmark.py
│   ├── question_classifier_benchmark.py
│   └── response_generator_benchmark.py
├── dataset/
│   ├── intents.csv
│   ├── questions.csv
│   └── responses.csv
├── model/
│   └── benchmark_result.py
├── runner/
│   ├── run_intent_classifier_benchmark.py
│   ├── run_question_classifier_benchmark.py
│   └── run_response_generator_benchmark.py
└── dataset_loader.py
```

## BenchmarkResult

Modelo único para resultados de benchmark.

Métricas atuais:

- model;
- strategy;
- correct;
- total;
- accuracy;
- elapsed;
- average_time;
- fallback_count quando aplicável;
- fallback_rate quando aplicável.

A estratégia é preenchida pelo runner, não pelo benchmark.

```text
ResponseGeneratorBenchmark
→ mede

Runner
→ sabe qual estratégia está sendo executada
```

---

# Fase 6 — Avaliação de SLM

Dataset ampliado para **30 casos**.

Modelos comparados:

- `qwen3:1.7b`
- `llama3.2:1b`

Estratégias:

- Ollama puro;
- Hybrid.

| Modelo | Estratégia | Acurácia | Tempo médio | Fallback |
|---|---|---:|---:|---:|
| qwen3:1.7b | Ollama | 100.00% | 0.466s | — |
| llama3.2:1b | Ollama | 66.67% | 0.372s | — |
| qwen3:1.7b | Hybrid | 100.00% | 0.403s | 0.00% |
| llama3.2:1b | Hybrid | 100.00% | 0.355s | 33.33% |

Principais conclusões:

- `qwen3:1.7b` acertou 30/30 sem fallback;
- `llama3.2:1b` acertou 20/30 sozinho;
- no Hybrid, os 10 erros do `llama3.2:1b` foram recuperados pelo fallback;
- os dois modelos chegaram a 100% de acurácia final no modo Hybrid;
- diferenças pequenas de latência entre puro e Hybrid não devem ser interpretadas como ganho real sem múltiplas execuções;
- o experimento demonstra o trade-off entre modelo menor/mais rápido e maior necessidade de fallback.

Conclusão principal:

```text
um SLM menor pode ser viável quando combinado
com validação factual e fallback determinístico
```

---

# Testes

## Unitários

Cobertura inclui:

- IntentClassifier
- QuestionClassifier
- VehicleQueryService
- ResponseValidationService
- HybridResponseGenerator
- AssistantService

### HybridResponseGenerator

- aceita resposta válida do SLM;
- aciona fallback para resposta inválida;
- aciona fallback quando o SLM lança exceção;
- contabiliza métricas corretamente;
- acumula métricas entre chamadas.

### AssistantService

- executa a orquestração na ordem correta;
- encaminha o `VehicleAnswer` ao `ResponseGenerator`;
- interrompe intents não suportados;
- interrompe question types não suportados;
- trata ausência de dados do veículo.

### VehicleQueryService

- retorna respostas estruturadas para dados conhecidos;
- lança `VehicleDataNotFoundError` quando o dado não está disponível.

## Integração

Cenários cobertos:

1. SLM retorna resposta factual válida;
2. SLM retorna resposta factual inválida e o fallback é usado;
3. SLM lança exceção e o fallback é usado.

Fronteira atual:

```text
AssistantService              REAL
QuestionClassifier            REAL
VehicleQueryService           REAL
JsonVehicleReader             REAL
ResponseValidationService     REAL
HybridResponseGenerator       REAL
RuleBased fallback            REAL
SLM generator                 MOCK
```

Ollama real permanece para benchmark e execução manual.

---

# Estado atual

```text
FASE 1 — Classificação
[✓] IntentClassifier
[✓] QuestionClassifier
[✓] Benchmarks

FASE 2 — Consulta e geração
[✓] VehicleQueryService
[✓] ResponseGenerator
[✓] OllamaResponseGenerator
[✓] RuleBasedResponseGenerator

FASE 3 — Confiabilidade
[✓] ResponseValidationService
[✓] HybridResponseGenerator
[✓] Fallback
[✓] FallbackMetrics
[✓] Validação factual

FASE 4 — Aplicação
[✓] AssistantService
[✓] Composition Root
[✓] CLI
[✓] Testes unitários
[✓] Testes de integração

FASE 5 — Robustez
[✓] Perguntas desconhecidas
[✓] Dados inexistentes
[✓] Tratamento básico de erros de domínio

FASE 6 — Avaliação de SLM
[✓] Dataset ampliado
[✓] Comparação entre modelos
[✓] Qualidade factual
[✓] Latência
[✓] Fallback rate
[✓] BenchmarkResult consolidado
```

---

# Decisão arquitetural — Multi-veículo antes de contexto conversacional

Foi decidido introduzir suporte a múltiplos veículos **antes** de contexto conversacional e persistência.

Motivo: o sistema atual trabalha com um conjunto fixo de dados de veículo. Contexto conversacional será mais útil quando existir um conceito explícito de **veículo ativo na sessão**.

O SLM não precisa ser treinado novamente para cada carro.

```text
Pergunta
 ↓
veículo selecionado
 ↓
dados estruturados daquele veículo
 ↓
VehicleAnswer
 ↓
SLM
```

Os fatos continuam fora do modelo.

---

# FASE 7 — Multi-veículo

Objetivo: permitir que a aplicação consulte diferentes veículos sem trocar código e sem criar um modelo de linguagem específico para cada carro.

```text
[ ] Criar identidade de veículo
[ ] Adaptar fonte de dados para múltiplos veículos
[ ] Consultar veículo pela identidade
[ ] Modelar veículo selecionado
[ ] Adaptar VehicleService / VehicleQueryService
[ ] Adaptar composition root
[ ] Permitir seleção/troca de veículo na CLI
[ ] Criar testes unitários multi-veículo
[ ] Criar testes de integração multi-veículo
[ ] Revisar benchmarks se necessário
```

Princípios:

```text
SLM não conhece arquivo de veículo.

VehicleQueryService não escolhe silenciosamente
um veículo global.

Identidade do veículo é independente do nome
do arquivo onde seus dados estão armazenados.
```

## Fase 7.1 — Identidade do veículo

Primeiro incremento: deixar de tratar o veículo apenas como “o conteúdo de `vehicle.json`” e introduzir identidade explícita.

Exemplo conceitual:

```text
VehicleId
→ t-cross-2022
→ polo-2023
→ nivus-2024
```

Critério de conclusão:

```text
[ ] existe uma identidade independente do arquivo
[ ] dois veículos podem coexistir na fonte de dados
[ ] um veículo pode ser recuperado pela identidade
[ ] nenhum componente usa o nome do arquivo como identidade de negócio
```

---

# FASE 8 — Contexto conversacional

Depois do suporte multi-veículo:

```text
[ ] ConversationContext em memória
[ ] Histórico de mensagens
[ ] Veículo ativo na sessão
[ ] Perguntas dependentes de contexto
[ ] Limite de histórico enviado ao SLM
[ ] Testes de contexto
```

Exemplo futuro:

```text
Usuário: Quero falar sobre meu T-Cross 2022.
Usuário: Qual óleo ele usa?
Usuário: E a pressão dos pneus?
```

---

# FASE 9 — Persistência

Somente após contexto em memória estar funcionando:

```text
[ ] Persistir sessão
[ ] Persistir veículo selecionado
[ ] Persistir histórico
[ ] Recuperar sessão
```

A tecnologia de persistência ainda não foi definida.

---

# Evoluções futuras possíveis

- dataset maior;
- mais tipos de informação automotiva;
- novos SLMs;
- métricas por `QuestionType`;
- motivo do fallback;
- observabilidade;
- recuperação de documentação externa;
- eventual RAG.

RAG, agentes, vector database e LLM-as-a-judge continuam fora do escopo atual até existir necessidade concreta.
