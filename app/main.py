from fastapi import FastAPI, Query
from app.utils import Output, DocumentService

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