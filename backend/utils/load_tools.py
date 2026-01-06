import json
from pathlib import Path
from backend.utils.embeddings import embed_text
from backend.utils.qdrant_store import client, init_collection, COLLECTION_NAME
from qdrant_client.models import PointStruct

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "tools.json"

def load_tools():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        tools = json.load(f)

    sample_embedding = embed_text("sample")
    init_collection(len(sample_embedding))

    points = []
    for idx, tool in enumerate(tools):
        vector = embed_text(tool["description"])
        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload=tool
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

if __name__ == "__main__":
    load_tools()
    print("Tools loaded into Qdrant")
