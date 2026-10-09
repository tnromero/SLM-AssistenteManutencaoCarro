import chromadb

from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.infrastructure.knowledge.chroma_chunk_mapper import (
    deserialize_chunk,
    serialize_metadata,
)


def test_persists_vectors_between_clients(tmp_path):
    database_path = str(tmp_path / "vector_db")
    first_client = chromadb.PersistentClient(path=database_path)

    collection = first_client.create_collection(
        name="test-knowledge",
        embedding_function=None,
        configuration={"hnsw": {"space": "cosine"}},
    )

    chunk = KnowledgeChunk(
        id="pneus:chunk:0",
        document_id="pneus",
        title="Cuidados com os pneus",
        content="Consulte os dados do veículo.",
        source="Material de teste",
        position=0,
    )

    collection.add(
        ids=[chunk.id],
        documents=[chunk.content],
        embeddings=[[1.0, 0.0]],
        metadatas=[serialize_metadata(chunk)],
    )

    second_client = chromadb.PersistentClient(path=database_path)
    restored_collection = second_client.get_collection(
        name="test-knowledge",
        embedding_function=None,
    )

    results = restored_collection.query(
        query_embeddings=[[1.0, 0.0]],
        n_results=1,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    assert documents is not None
    assert metadatas is not None

    restored_chunk = deserialize_chunk(
        chunk_id=results["ids"][0][0],
        content=documents[0][0],
        metadata=dict(metadatas[0][0]),
    )

    assert restored_collection.count() == 1
    assert restored_chunk == chunk
