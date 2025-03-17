from pydantic import BaseModel
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Document, VectorStoreIndex, ServiceContext
import fitz # PyMuPDF
from dataclasses import dataclass
import os
import re

key = os.environ['OPENAI_API_KEY']

@dataclass
class Input:
    query: str
    file_path: str

@dataclass
class Citation:
    source: str
    text: str

class Output(BaseModel):
    query: str
    response: str
    citations: list[Citation]

class DocumentService:

    """
    Update this service to load the pdf and extract its contents.
    The example code below will help with the data structured required
    when using the QdrantService.load() method below. Note: for this
    exercise, ignore the subtle difference between llama-index's 
    Document and Node classes (i.e, treat them as interchangeable).

    # example code
    def create_documents() -> list[Document]:

        docs = [
            Document(
                metadata={"Section": "Law 1"},
                text="Theft is punishable by hanging",
            ),
            Document(
                metadata={"Section": "Law 2"},
                text="Tax evasion is punishable by banishment.",
            ),
        ]

        return docs

     """
    
   # get pdf contents as a string
    def get_pdf_contents(self, file_path: str = "./docs/laws.pdf") -> str:
        """Extract text from a PDF file."""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
        
    # Split the text into major sections
    def extract_laws(self, text: str) -> list[str]:
        # remove "Citations" section at the end of the document
        # find last occurence of "Citations"
        citations_idx = text.rfind("Citations")
        text = text[:citations_idx]
        
        # split text by top heading level, e.g. 1., 2., 3., etc.
        pattern = r"(?=\n\d+\.\n)"
        sections = re.split(pattern, text)
        # remove first section, which is the title
        sections = sections[1:]

        # remove empty sections and line breaks
        sections = [section.strip() for section in sections if section.strip()]

        return sections

class QdrantService:
    def __init__(self, k: int = 2):
        self.index = None
        self.k = k
    
    def connect(self) -> None:
        client = qdrant_client.QdrantClient(location=":memory:")
                
        vstore = QdrantVectorStore(client=client, collection_name='temp')

        service_context = ServiceContext.from_defaults(
            embed_model=OpenAIEmbedding(),
            llm=OpenAI(api_key=key, model="gpt-4")
            )

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vstore, 
            service_context=service_context
            )

    def load(self, docs = list[Document]):
        self.index.insert_nodes(docs)
    
    def query(self, query_str: str) -> Output:

        """
        This method needs to initialize the query engine, run the query, and return
        the result as a pydantic Output class. This is what will be returned as
        JSON via the FastAPI endpount. Fee free to do this however you'd like, but
        a its worth noting that the llama-index package has a CitationQueryEngine...

        Also, be sure to make use of self.k (the number of vectors to return based
        on semantic similarity).

        # Example output object
        citations = [
            Citation(source="Law 1", text="Theft is punishable by hanging"),
            Citation(source="Law 2", text="Tax evasion is punishable by banishment."),
        ]

        output = Output(
            query=query_str, 
            response=response_text, 
            citations=citations
            )
        
        return output

        """
       

if __name__ == "__main__":
    # Example workflow
    doc_serivce = DocumentService() # implemented
    docs = doc_serivce.create_documents() # NOT implemented

    index = QdrantService() # implemented
    index.connect() # implemented
    index.load() # implemented

    index.query("what happens if I steal?") # NOT implemented





