import chromadb


def test_persists_vectors_between_clients(tmp_path):
    database_path = str(tmp_path / "vector_db")

    first_client = chromadb.PersistentClient(path=database_path)

    collection = first_client.create_collection(
        name="test-knowledge",
        embedding_function=None,
        configuration={
            "hnsw": {
                "space": "cosine",
            }
        },
    )

    collection.add(
        ids=["pneus:chunk:0"],
        documents=["Consulte os dados do veículo."],
        embeddings=[[1.0, 0.0]],
        metadatas=[
            {
                "document_id": "pneus",
                "title": "Cuidados com os pneus",
                "source": "Material de teste",
                "position": 0,
                "vehicle_scope": "general",
            }
        ],
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

    assert restored_collection.count() == 1
    assert results["ids"] == [["pneus:chunk:0"]]
    assert results["documents"] == [
        ["Consulte os dados do veículo."]
    ]
