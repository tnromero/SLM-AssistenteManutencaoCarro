from math import isfinite

import ollama

from slm_assistentemanutencaocarro.application.exception import (
    EmbeddingGenerationError,
)
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)


class OllamaEmbeddingGenerator:
    def __init__(self, model: str = "embeddinggemma:300m"):
        self.model = model

    def embed_query(self, question: str) -> list[float]:
        if not question.strip():
            raise ValueError("A pergunta não pode ser vazia.")

        text = f"task: search result | query: {question}"

        return self._embed([text])[0]

    def embed_documents(
        self,
        chunks: list[KnowledgeChunk],
    ) -> list[list[float]]:
        if not chunks:
            return []

        if any(not chunk.content.strip() for chunk in chunks):
            raise ValueError("Os chunks não podem ter conteúdo vazio.")

        texts = [
            f"title: {chunk.title} | text: {chunk.content}"
            for chunk in chunks
        ]

        return self._embed(texts)

    def _embed(self, texts: list[str]) -> list[list[float]]:
        try:
            response = ollama.embed(
                model=self.model,
                input=texts,
                truncate=False,
            )

            vectors = response.embeddings

            if len(vectors) != len(texts):
                raise ValueError(
                    "Quantidade de embeddings diferente das entradas."
                )

            dimension = len(vectors[0])

            if dimension == 0:
                raise ValueError("Embedding vazio.")

            for vector in vectors:
                if len(vector) != dimension:
                    raise ValueError("Dimensões inconsistentes.")

                if not all(isfinite(value) for value in vector):
                    raise ValueError("Embedding com valores não finitos.")

                if not any(value != 0 for value in vector):
                    raise ValueError("Embedding com vetor nulo.")

            return vectors

        except Exception as exc:
            raise EmbeddingGenerationError(
                "Não foi possível gerar embeddings."
            ) from exc