# SLM Assistente de Manutenção do Carro

## Visão geral

Este projeto tem como objetivo estudar o uso de **Small Language Models (SLMs)** em uma aplicação de assistência automotiva, combinando geração por modelo local, regras determinísticas, validação factual e fallback.

O projeto foi desenvolvido de forma incremental, com foco em:

- Clean Architecture simplificada
- SOLID
- Injeção de dependências
- Separação entre domínio, aplicação, infraestrutura e apresentação
- Testes unitários e de integração
- Avaliação objetiva de qualidade, latência e fallback
- Uso local de SLM via Ollama

A proposta não é criar uma aplicação de produção completa, mas construir uma base arquitetural clara para estudar os limites e benefícios de SLMs em um fluxo controlado.

---

## Arquitetura atual

Fluxo principal:

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

Responsabilidades principais:

### `AssistantService`

Orquestra o fluxo da aplicação:

1. recebe a pergunta do usuário;
2. classifica a intenção;
3. classifica o tipo de pergunta;
4. consulta os dados estruturados do veículo;
5. envia o `VehicleAnswer` para o `ResponseGenerator`;
6. retorna a resposta final.

O serviço depende apenas das abstrações necessárias e não conhece Ollama, fallback ou detalhes de infraestrutura.

### `VehicleQueryService`

Responsável por consultar os dados do veículo de acordo com o `QuestionType` identificado.

Retorna um `VehicleAnswer`, que contém:

- pergunta original;
- resposta factual esperada.

### `ResponseGenerator`

Porta da aplicação para geração de respostas.

Permite trocar a implementação concreta sem alterar o `AssistantService`.

### `HybridResponseGenerator`

Estratégia híbrida de geração:

```text
SLM
 ↓
ResponseValidationService
 ├─ válido   → resposta do SLM
 └─ inválido → fallback determinístico
```

Também faz fallback quando o gerador principal lança exceção.

### `ResponseValidationService`

Valida a resposta gerada pelo SLM usando fatos extraídos da resposta esperada.

Atualmente cobre valores como:

- viscosidade de óleo, por exemplo `5W-40`;
- pressão em PSI;
- pressão em bar;
- medidas de pneus;
- múltiplos valores factuais na mesma resposta.

Quando não existem fatos estruturados reconhecíveis, utiliza uma validação textual simples.

### `FallbackMetrics`

Mantém métricas do comportamento híbrido:

- total de respostas;
- quantidade resolvida pelo SLM;
- quantidade de fallbacks;
- taxa de fallback.

Exemplo:

```text
Total: 10
SLM: 7
Fallbacks: 3
Fallback rate: 30%
```

---

## Composition Root

A montagem das dependências está centralizada em:

```text
slm_assistentemanutencaocarro/infrastructure/composition.py
```

O `composition.py` é responsável por criar e conectar as implementações concretas.

Exemplo conceitual:

```python
def build_assistant() -> AssistantService:
    settings = Settings()

    intent_classifier = ...
    question_classifier = ...

    vehicle_reader = ...
    vehicle_service = ...
    vehicle_query_service = ...

    slm_generator = ...
    fallback_generator = ...
    response_validator = ...

    response_generator = HybridResponseGenerator(
        response_generator=slm_generator,
        fallback_generator=fallback_generator,
        response_validator=response_validator,
    )

    return AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )
```

O entrypoint da aplicação permanece fino:

```text
main / __init__
 ↓
build_assistant()
 ↓
CLI
```

---

## CLI

A aplicação possui uma interface de linha de comando responsável apenas pela interação com o usuário.

Exemplo de fluxo:

```text
Assistente de Manutenção

> Qual óleo devo usar?

Para esse veículo, utilize óleo 5W-40.

> sair
```

A CLI recebe um `AssistantService` pronto e não instancia dependências diretamente.

---

## Benchmarks

A infraestrutura de benchmark foi reorganizada para separar:

- datasets;
- execução;
- resultado;
- implementação de cada benchmark.

Estrutura:

```text
benchmark/
├── benchmark/
│   ├── intent_classifier_benchmark.py
│   ├── question_classifier_benchmark.py
│   └── response_generator_benchmark.py
│
├── dataset/
│   ├── intents.csv
│   ├── questions.csv
│   └── responses.csv
│
├── model/
│   └── benchmark_result.py
│
├── runner/
│   ├── run_intent_classifier_benchmark.py
│   ├── run_question_classifier_benchmark.py
│   └── run_response_generator_benchmark.py
│
└── dataset_loader.py
```

### `BenchmarkResult`

Padroniza métricas como:

- total de casos;
- acertos;
- acurácia;
- tempo total;
- tempo médio.

### Benchmark do `ResponseGenerator`

O benchmark recebe apenas:

- `ResponseGenerator`;
- `ResponseValidationService`;
- dataset.

Ele não executa classificação de intenção, classificação de pergunta ou consulta ao veículo.

Isso mantém o benchmark focado na responsabilidade que está sendo avaliada.

---

## Testes

### Testes unitários

Foram organizados para testar cada responsabilidade isoladamente.

Principais áreas:

- `IntentClassifier`
- `QuestionClassifier`
- `VehicleQueryService`
- `ResponseValidationService`
- `HybridResponseGenerator`
- `AssistantService`

### `HybridResponseGenerator`

Casos cobertos:

- usa resposta do SLM quando válida;
- usa fallback quando a resposta é factualmente inválida;
- usa fallback quando o SLM lança exceção;
- contabiliza fallback;
- não contabiliza resposta válida como fallback;
- contabiliza fallback em exceção;
- acumula métricas corretamente.

### `AssistantService`

Casos cobertos:

- responde pergunta suportada;
- classifica a pergunta antes de consultar o veículo;
- envia o `VehicleAnswer` ao `ResponseGenerator`;
- interrompe o fluxo quando o intent não é suportado.

### Testes de integração

Fluxo integrado cobre:

1. resposta válida do SLM;
2. resposta factualmente incorreta do SLM com fallback real;
3. exceção do SLM com fallback real.

No teste de integração:

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

O SLM é mockado para manter o teste:

- determinístico;
- rápido;
- independente do Ollama;
- adequado para execução automática.

Ollama real permanece para benchmark e teste manual.

---

## Estado atual do projeto

```text
[✓] IntentClassifier
[✓] QuestionClassifier
[✓] VehicleQueryService
[✓] ResponseGenerator
[✓] ResponseValidationService
[✓] HybridResponseGenerator com fallback

[✓] Benchmark de qualidade do ResponseGenerator
[✓] Benchmark de latência
[✓] Métrica de fallback
[✓] Melhoria da validação factual

[✓] Testes unitários do AssistantService
[✓] Testes de integração do AssistantService
[✓] CLI
[✓] Composition Root
```

---

## Próximas etapas

### 1. Tratamento de perguntas desconhecidas

Objetivo:

evitar que perguntas fora do domínio conhecido avancem indevidamente pelo pipeline.

Exemplos:

```text
"Qual a capital da França?"
"Quem ganhou a Copa?"
"Me conte uma piada."
```

O sistema deve reconhecer que não possui suporte para responder essas perguntas.

Aspectos a definir:

- comportamento para `Intent.OUTRO`;
- comportamento para `QuestionType` desconhecido;
- mensagem padronizada ao usuário;
- testes unitários;
- testes de integração.

### 2. Tratamento de respostas sem dados disponíveis

Exemplo:

```text
Usuário:
Qual o torque do parafuso X?

Base do veículo:
informação inexistente.
```

O sistema não deve fabricar uma resposta.

Possíveis estratégias:

- retornar uma resposta explícita de dado indisponível;
- impedir o envio ao SLM;
- diferenciar `unknown question` de `known question without data`.

### 3. Avaliar qualidade do SLM com dataset maior

Expandir `responses.csv` com:

- diferentes formulações da mesma pergunta;
- respostas factualmente incorretas;
- respostas parcialmente corretas;
- respostas prolixas;
- múltiplos fatos;
- casos ambíguos.

Objetivo:

medir melhor:

- acurácia factual;
- fallback rate;
- latência;
- diferença entre modelos.

### 4. Comparação entre SLMs

Executar o mesmo benchmark com múltiplos modelos.

Exemplos:

```text
qwen3:1.7b
qwen3:4b
outro SLM compatível com o hardware
```

Comparar:

- qualidade;
- latência;
- consumo de recursos;
- taxa de fallback.

### 5. Melhorar observabilidade

Sem criar uma infraestrutura complexa, pode-se futuramente registrar:

- modelo utilizado;
- tempo de inferência;
- resposta aceita/rejeitada;
- motivo do fallback;
- tipo da pergunta;
- taxa de fallback por `QuestionType`.

### 6. Persistência e conversa

Etapa posterior.

Possíveis objetivos:

- histórico da sessão;
- contexto mínimo de conversa;
- referências a perguntas anteriores;
- persistência opcional.

Esta etapa deve ser adicionada apenas quando o fluxo stateless estiver suficientemente estável.

---

## Decisões arquiteturais importantes

### O benchmark não executa todo o pipeline

Cada benchmark mede uma responsabilidade específica.

Isso evita misturar erros de:

- classificação;
- consulta;
- geração;
- validação.

### Ollama não participa dos testes automatizados de integração

Ollama é tratado como infraestrutura externa.

Nos testes automatizados, o `ResponseGenerator` do SLM é mockado.

O modelo real é utilizado em:

- benchmarks;
- testes manuais;
- CLI.

### O fallback é parte do `HybridResponseGenerator`

O `AssistantService` conhece apenas `ResponseGenerator`.

Ele não precisa saber:

- se existe SLM;
- qual modelo está sendo usado;
- se existe fallback;
- como a validação funciona.

### `composition.py` centraliza a montagem

O código de aplicação não instancia implementações concretas.

A composição acontece na borda da aplicação.

### Não introduzir complexidade antecipadamente

Por enquanto, o projeto evita:

- RAG;
- vector database;
- agentes;
- LLM-as-a-judge;
- framework de observabilidade;
- repository de métricas;
- abstrações sem necessidade prática.

Esses elementos só devem ser introduzidos quando houver uma necessidade concreta de estudo.

---

## Roadmap resumido

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
[✓] Tratamento de erros de domínio

FASE 6 — Avaliação de SLM
[ ] Dataset ampliado
[ ] Comparação entre modelos
[ ] Análise de qualidade × latência × fallback

FASE 7 — Evoluções futuras
[ ] Persistência
[ ] Contexto conversacional
[ ] Observabilidade ampliada
```
