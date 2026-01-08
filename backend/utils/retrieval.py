from backend.utils.qdrant_store import client, COLLECTION_NAME
from backend.utils.embeddings import embed_text

def retrieve_tools_for_project(project_description: str, top_k: int = 5):
    query_vector = embed_text(project_description)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[],
        query=query_vector,
        limit=top_k
    )

    tools = []
    for hit in results.points:
        payload = hit.payload or {}
        payload["id"] = str(hit.id)
        tools.append(payload)

    return tools
