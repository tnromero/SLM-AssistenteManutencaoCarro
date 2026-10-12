# SLM Assistente de Manutenção do Carro

Atualizado em: 05/10/2026

## Objetivo e arquitetura

Projeto de estudo de SLM local com Ollama: dados estruturados fornecem os fatos; o modelo interpreta perguntas e gera linguagem natural, com validação factual e fallback determinístico.

- Clean Architecture simplificada, SOLID e injeção de dependências.
- `domain`: conceitos automotivos e vocabulário funcional.
- `application`: serviços, contratos, modelos e contexto da sessão.
- `infrastructure`: regras, Ollama, estratégias híbridas e persistência.
- `presentation`: CLI; dependências montadas no composition root.
- Convenção de diretórios no singular; testes unitários e de integração.

## Roadmap

| Fase | Tema | Escopo principal | Estado |
| --- | --- | --- | --- |
| 1 | Classificação | Intenção, tipo de pergunta e benchmarks | Concluída |
| 2 | Consulta e geração | Consulta estruturada; respostas por regras e Ollama | Concluída |
| 3 | Confiabilidade | Validação factual, fallback e métricas | Concluída |
| 4 | Aplicação | AssistantService, composition root, CLI e testes | Concluída |
| 5 | Robustez | Perguntas desconhecidas, dados ausentes e erros | Concluída |
| 6 | Avaliação de SLM | Qualidade, latência e fallback; comparação de modelos | Concluída |
| 7 | Multi-veículo | Identidade, seleção e troca do veículo ativo | Concluída |
| 8 | Contexto conversacional | Histórico limitado, resolução contextual e testes da sessão | Concluída |
| 9 | Persistência | Salvar e recuperar veículo ativo e histórico em JSON | Concluída |
| 10 | Base de conhecimento | Documentos automotivos e organização das fontes | Concluída |
| 11 | Embeddings e busca semântica | Chunks, embeddings e recuperação em memória | Concluída |
| 12 | RAG | Integrar recuperação documental à geração | Concluída |
| 13 | Banco vetorial | Persistir e consultar embeddings | Concluída |
| 14 | Avaliação do RAG | Recall@K, relevância, chunks, latência e alucinação | Concluída |
| 15 | Tools e MCP | Ferramentas automotivas; contrato na aplicação e MCP na infraestrutura | Planejada |
| 16 | Observabilidade | Logging, falhas e métricas de desempenho | Planejada |

## FASE 14 - Avaliação do RAG

| Avaliação de generalização | Resultado |
| --- | ---: |
| Hit@1 / Recall@1 | 100% / 100% |
| Hit@3 / Recall@3 | 100% / 100% |
| Recuperação média — K=1 | 0,085 s |
| Recuperação média — K=3 | 0,097 s |
| Adequação na revisão manual | 6/6 — 100% |

Recusas incorretas: `pressure-source-paraphrase` e `oil-change-interval-inference`.

```json
    {
      "case_id": "pressure-source-paraphrase",
      "question": "Onde encontro a calibragem recomendada?",
      "answerable": true,
      "expected_answer": "Consultar os dados do veículo selecionado ou a documentação do fabricante.",
      "retrieved_document_ids": [
        "cuidados-pneus",
        "verificacao-oleo"
      ],
      "response": "Não encontrei informações suficientes nos documentos disponíveis.",
      "refused": true,
      "citations_valid": true,
      "retrieval_time": 1.2874858719997064,
      "generation_time": 4.0339131750006345,
      "error": null,
      "refusal_format_valid": true,
      "retrieved_passages": [
        {
          "citation_id": 1,
          "chunk_id": "cuidados-pneus:chunk:0",
          "document_id": "cuidados-pneus",
          "title": "Cuidados com os pneus",
          "content": "# Cuidados com os pneus Documento de estudo do assistente automotivo. Este texto não substitui o manual do veículo. ## Consulta da pressão A pressão indicada deve ser consultada nos dados do veículo selecionado ou na documentação do fabricante. ## Informações diferentes Pressão dos pneus e medida dos pneus são informações diferentes. A medida identifica dimensões do pneu; a pressão indica sua calibragem. ## Limite deste documento Este documento não define valores de pressão nem medidas de pneus. Esses valores devem vir da fonte específica do veículo.",
          "source": "Material de estudo do projeto",
          "score": 0.3527369499206543
        },
        {
          "citation_id": 2,
          "chunk_id": "verificacao-oleo:chunk:0",
          "document_id": "verificacao-oleo",
          "title": "Consulta de informações sobre óleo",
          "content": "# Consulta de informações sobre óleo Documento de estudo do assistente automotivo. Este texto não substitui o manual do veículo. ## Especificação do óleo A especificação do óleo deve ser consultada nos dados do veículo selecionado e na documentação do fabricante. ## Perguntas diferentes A especificação do óleo, o intervalo de troca e o custo do serviço são informações distintas. Conhecer a viscosidade não permite concluir o intervalo de troca nem o custo da manutenção. ## Limite deste documento Este documento não define viscosidade, homologação, quantidade, intervalo de troca ou preço.",
          "source": "Material de estudo do projeto",
          "score": 0.3314296007156372
        }
      ],
      "manual_review": {
        "verdict": "incorrect",
        "notes": "Recusa indevida: o trecho [1] associa pressão à calibragem e indica onde consultar a pressão recomendada; não é necessário fornecer um valor."
      }
    },
    {
      "case_id": "oil-change-interval-inference",
      "question": "Conhecer a viscosidade permite definir o intervalo de troca do óleo?",
      "answerable": true,
      "expected_answer": "Não. Conhecer a viscosidade não permite concluir o intervalo de troca.",
      "retrieved_document_ids": [
        "verificacao-oleo",
        "cuidados-pneus"
      ],
      "response": "Não encontrei informações suficientes nos documentos disponíveis.",
      "refused": true,
      "citations_valid": true,
      "retrieval_time": 0.9049682659997416,
      "generation_time": 3.510652640000444,
      "error": null,
      "refusal_format_valid": true,
      "retrieved_passages": [
        {
          "citation_id": 1,
          "chunk_id": "verificacao-oleo:chunk:0",
          "document_id": "verificacao-oleo",
          "title": "Consulta de informações sobre óleo",
          "content": "# Consulta de informações sobre óleo Documento de estudo do assistente automotivo. Este texto não substitui o manual do veículo. ## Especificação do óleo A especificação do óleo deve ser consultada nos dados do veículo selecionado e na documentação do fabricante. ## Perguntas diferentes A especificação do óleo, o intervalo de troca e o custo do serviço são informações distintas. Conhecer a viscosidade não permite concluir o intervalo de troca nem o custo da manutenção. ## Limite deste documento Este documento não define viscosidade, homologação, quantidade, intervalo de troca ou preço.",
          "source": "Material de estudo do projeto",
          "score": 0.6925121545791626
        },
        {
          "citation_id": 2,
          "chunk_id": "cuidados-pneus:chunk:0",
          "document_id": "cuidados-pneus",
          "title": "Cuidados com os pneus",
          "content": "# Cuidados com os pneus Documento de estudo do assistente automotivo. Este texto não substitui o manual do veículo. ## Consulta da pressão A pressão indicada deve ser consultada nos dados do veículo selecionado ou na documentação do fabricante. ## Informações diferentes Pressão dos pneus e medida dos pneus são informações diferentes. A medida identifica dimensões do pneu; a pressão indica sua calibragem. ## Limite deste documento Este documento não define valores de pressão nem medidas de pneus. Esses valores devem vir da fonte específica do veículo.",
          "source": "Material de estudo do projeto",
          "score": 0.3944787383079529
        }
      ],
      "manual_review": {
        "verdict": "incorrect",
        "notes": "Recusa indevida: o trecho [1] afirma explicitamente que conhecer a viscosidade não permite concluir o intervalo de troca."
      }
    }
```