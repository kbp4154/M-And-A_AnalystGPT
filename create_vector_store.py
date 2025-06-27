# create_vector_store.py
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger
import os
import fitz

def load_documents():
    pdf_directory = "10k_filings"
    documents = []
    if not os.path.exists(pdf_directory):
        raise ValueError(f"Directory '{pdf_directory}' does not exist.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_directory, filename)
            try:
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text("text")
                    tables = page.get_text("blocks")
                    for block in tables:
                        if block[6] == 0:
                            text += block[4]
                chunks = text_splitter.split_text(text)
                company = filename.split("_")[0].lower()
                for i, chunk in enumerate(chunks):
                    documents.append(Document(
                        page_content=chunk,
                        metadata={"source": filename, "company": company, "chunk": i}
                    ))
                doc.close()
            except Exception as e:
                logger.error(f"Failed to process {filename}: {e}")
    return documents

def create_vector_store():
    logger.info("Creating vector store...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    documents = load_documents()
    if not documents:
        raise ValueError("No documents loaded.")
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local("vector_store")
    logger.info("Vector store created and saved.")

if __name__ == "__main__":
    create_vector_store()