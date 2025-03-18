from pydantic import BaseModel
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.core.query_engine import CitationQueryEngine
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
    def create_documents(self) -> list[Document]:
        """
        This service load a pdf and extracts its contents.
        The method then creates a structured list of Document objects, 
        which are used to load into a Qdrant collection.
        """
        content = self.get_pdf_contents()
        sections = self.extract_laws(content)

        docs = []

        for section in sections:
            section_number = section.split(".")[0]
            section_title = section.split("\n")[1]
            docs.append(Document(
                metadata={"Section": section_number, "Title": section_title},
                text=section
            ))

        return docs
    
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

        # Configure settings with the new API
        Settings.embed_model = OpenAIEmbedding()
        Settings.llm = OpenAI(api_key=key, model="gpt-4")

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vstore
        )

    def load(self, docs = list[Document]):
        self.index.insert_nodes(docs)
    
    def query(self, query_str: str) -> Output:
        """
        This method initializes the query engine, runs the query, and return
        the result as a pydantic Output class. Longer queries will include more citations,
        because self.k is set based on the query length.
        """

        # parse pdf into documents and load into Qdrant
        doc_service = DocumentService()
        documents = doc_service.create_documents()

        self.connect()
        self.load(documents)

        query_engine = CitationQueryEngine.from_args(
            index=self.index,
            similarity_top_k=self.k
        )

        response = query_engine.query(query_str)

        # Extract and format citations from the response
        citations = []
        for source_node in response.source_nodes:
            citations.append(Citation(
                source=f"{source_node.metadata.get('Section')}: {source_node.metadata.get('Title')}",
                text="\n".join(source_node.text.split("\n")[1:])
            ))

        return Output(
            query=query_str,
            response=str(response),
            citations=citations
        )
       

if __name__ == "__main__":
    # Example workflow
    doc_service = DocumentService() # implemented
    docs = doc_service.create_documents() # NOT implemented

    index = QdrantService() # implemented
    index.connect() # implemented
    index.load() # implemented

    index.query("what happens if I steal?") # NOT implemented





