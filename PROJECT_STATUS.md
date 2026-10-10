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
| 14 | Avaliação do RAG | Recall@K, relevância, chunks, latência e alucinação | Em andamento |
| 15 | Tools e MCP | Ferramentas automotivas; contrato na aplicação e MCP na infraestrutura | Planejada |
| 16 | Observabilidade | Logging, falhas e métricas de desempenho | Planejada |

## FASE 14 - Avaliação do RAG
