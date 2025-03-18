from fastapi import FastAPI, Query
from app.utils import Output, DocumentService, QdrantService
from math import ceil

app = FastAPI()

"""
Please create an endpoint that accepts a query string, e.g., "what happens if I steal 
from the Sept?" and returns a JSON response serialized from the Pydantic Output class.
"""

@app.get("/")
async def root():
    return {"message": "Hello World"}

# endpoint to get contents of laws.pdf
@app.get("/laws")
async def get_laws():
    try:
        doc_service = DocumentService()
        content = doc_service.get_pdf_contents()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}
    
# endpoint to get sections of laws.pdf
@app.get("/laws/sections")
async def get_laws_sections():
    try:
        doc_service = DocumentService()
        content = doc_service.get_pdf_contents()
        sections = doc_service.extract_laws(content)
        return {"sections": sections}
    except Exception as e:
        return {"error": str(e)}
    
# endpoint to get document objects from laws.pdf
@app.get("/laws/documents")
async def get_laws_documents():
    try:
        doc_service = DocumentService()
        documents = doc_service.create_documents()
        return {"documents": documents}
    except Exception as e:
        return {"error": str(e)}
    
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