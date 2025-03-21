from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.utils import Output, QdrantService
from math import ceil

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Please create an endpoint that accepts a query string, e.g., "what happens if I steal 
from the Sept?" and returns a JSON response serialized from the Pydantic Output class.
"""
    
# endpoint to process a query and return the Output object
@app.get("/laws/query")
async def query_laws(query: str = Query(..., description="Ask a question about the laws of Westeros", min_length=1, example="How are disputes between great houses resolved?")) -> Output:
    try:
        # assume longer queries need more context
        k = ceil(len(query) / 50)

        qdrant_service = QdrantService(k)
        result = qdrant_service.query(query)
        return result
    except Exception as e:
        return {"error": str(e)}