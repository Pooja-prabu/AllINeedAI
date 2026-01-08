try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import VectorParams, Distance

    COLLECTION_NAME = "ai_tools"

    # ✅ Use local persistent Qdrant (no server needed)
    client = QdrantClient(path="./qdrant_data")

    def init_collection(vector_size: int):
        collections = client.get_collections().collections
        if not any(c.name == COLLECTION_NAME for c in collections):
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
except Exception as e:
    # Fallback when qdrant-client is missing
    import json
    from pathlib import Path
    
    print("qdrant-client not available, using stub:", e)

    COLLECTION_NAME = "ai_tools"

    class _StubPoint:
        def __init__(self, point_id, payload):
            self.id = point_id
            self.payload = payload

    class _StubPointsResult:
        def __init__(self, points):
            self.points = points

    class _StubClient:
        def __init__(self):
            self._storage = {}
            self._load_sample_data()

        def _load_sample_data(self):
            """Load sample tools from tools.json to enable fallback search"""
            try:
                data_path = Path(__file__).parent.parent / "data" / "tools.json"
                with open(data_path, 'r', encoding='utf-8') as f:
                    tools = json.load(f)
                self._storage[COLLECTION_NAME] = [(i, t) for i, t in enumerate(tools)]
            except Exception:
                self._storage[COLLECTION_NAME] = []

        def get_collections(self):
            return type("C", (), {"collections": []})()

        def create_collection(self, collection_name: str, vectors_config=None):
            if collection_name not in self._storage:
                self._storage[collection_name] = []

        def upsert(self, collection_name: str, points=None):
            if collection_name not in self._storage:
                self._storage[collection_name] = []
            for p in points or []:
                self._storage[collection_name].append((p.id, p.payload))

        def search(self, collection_name: str, query_vector=None, limit: int = 5):
            items = self._storage.get(collection_name, [])
            results = []
            for point_id, payload in items[:limit]:
                results.append(type("H", (), {"payload": payload})())
            return results

        def query_points(self, collection_name: str, prefetch=None, query=None, limit: int = 5):
            """Support newer Qdrant API - return first N items from storage"""
            items = self._storage.get(collection_name, [])
            points = [_StubPoint(point_id, payload) for point_id, payload in items[:limit]]
            return _StubPointsResult(points)

    client = _StubClient()

    def init_collection(vector_size: int):
        if COLLECTION_NAME not in client._storage:
            client._storage[COLLECTION_NAME] = []
