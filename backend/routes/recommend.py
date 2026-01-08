from fastapi import APIRouter, HTTPException
from backend.models.schemas import RecommendRequest, RecommendResponse, Tool
from backend.utils.supabase_client import fetch_all_tools
from backend.utils.ai_engine import recommend as recommend_engine
from backend.utils.retrieval import retrieve_tools_for_project
from backend.utils.normalization import normalize_tool

router = APIRouter(prefix='/api', tags=['recommend'])

@router.post('/recommend', response_model=RecommendResponse)
def recommend(req: RecommendRequest):

    # 1️⃣ Retrieve relevant tools via RAG
    retrieved_tools = retrieve_tools_for_project(
        project_description=req.query,
        top_k=req.limit
    )

    # 2️⃣ Safety fallback (Supabase)
    if not retrieved_tools:
        retrieved_tools = fetch_all_tools()

    # 3️⃣ Normalize tools so AI engine doesn't crash
    normalized_tools = [normalize_tool(t) for t in retrieved_tools]

    # 4️⃣ Run existing recommendation engine
    top = recommend_engine(req.query, normalized_tools, req.limit)

    # 5️⃣ Shape response
    normalized = []
    for t in top:
        normalized.append(Tool(
            id=str(t.get('id')) if t.get('id') else None,
            name=t.get('name', ''),
            description=t.get('description', ''),
            category=t.get('category', ''),
            tags=t.get('tags') or [],
            url=t.get('url') or t.get('website'),
            rating=t.get('rating'),
            pricing=t.get('pricing'),
            trending=t.get('trending', False),
            popularity=t.get('popularity', 0),
            reviews=t.get('reviews', [])
        ))

    return RecommendResponse(recommendations=normalized)
