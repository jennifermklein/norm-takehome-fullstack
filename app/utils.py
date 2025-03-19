from pydantic import BaseModel
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.core.query_engine import CitationQueryEngine
from dataclasses import dataclass
import os
import re
import pymupdf4llm

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
        content = pymupdf4llm.to_markdown("./docs/laws.pdf")
        sections = self.extract_laws(content)

        # extract and remove document title to use as metadata
        document_title = sections[0]
        sections = sections[1:]

        docs = []

        for section in sections:
            section_number, section_title, section_text = self.extract_section_headings(section)

            # split section into minor sections
            subsection_pattern = r"(?=\n(?:\*\*\d+(\.\d+)*\.\*\*|\d+(\.\d+)*\. ))"
            subsections = re.split(subsection_pattern, section_text)

            current_subsection_number = None
            current_subsection_title = None

            for subsection in subsections:
                if not subsection or not subsection.strip() or subsection.strip().startswith("."):
                    continue

                # if subsection has bolded headings, extract them and do not treat as its own document
                # instead, store the subsection number and title for metadata of subsequent subsections
                if subsection.strip().startswith("**"):
                    current_subsection_number, current_subsection_title, _ = self.extract_section_headings(subsection)
                    continue
                
                docs.append(Document(
                    metadata={"Document_Title": document_title,
                              "Section_Number": section_number,
                              "Section_Title": section_title,
                              "Subsection_Number": current_subsection_number,
                              "Subsection_Title": current_subsection_title},
                    text=subsection
                ))

        return docs
    
    def extract_section_headings(self, text) -> tuple[str, str, str]:
            # Extract section number, assuming it is the first bolded heading
            section_num_start_idx = text.find("**")
            section_num_end_idx = text.find("**", section_num_start_idx + 2)
            section_number = text[section_num_start_idx + 2:section_num_end_idx]

            # extract section title, assuming it is the second bolded heading
            section_title_start_idx = text.find("**", section_num_end_idx + 2)
            section_title_end_idx = text.find("**", section_title_start_idx + 2)
            section_title = text[section_title_start_idx + 2:section_title_end_idx]

            section_text = text[section_title_end_idx + 2:]

            return section_number, section_title, section_text    
        
    def extract_laws(self, text: str) -> list[str]:
        """
        Extracts the major sections of the file, i.e. top level law headings formatted as 1., 2., 3., etc.
        """
        # remove "Citations" section at the end of the document
        citations_idx = text.rfind("**Citations")
        text = text[:citations_idx]
        
        # split text by top heading level
        section_pattern = r"(?=\*\*\d+\.\*\*)"
        sections = re.split(section_pattern, text)

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
            source = f"{source_node.metadata.get('Section_Number')} {source_node.metadata.get('Section_Title')}"
            if source_node.metadata.get('Subsection_Number') is not None:
                source = f"{source}, {source_node.metadata.get('Subsection_Number')} {source_node.metadata.get('Subsection_Title')}"

            citations.append(Citation(
                source=source,
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





