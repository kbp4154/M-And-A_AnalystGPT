# build_vector_store.py

from embeddings.vector_store import load_chunks_from_file, build_and_save_vector_store
from embeddings.embedder import SentenceTransformerEmbeddings

print("📄 Loading chunks...")
documents = load_chunks_from_file()

print("💡 Initializing embedder...")
embeddings = SentenceTransformerEmbeddings()

print("💾 Building & saving vector store...")
build_and_save_vector_store(documents, embeddings)

print("✅ Vector DB ready at ./vector_db/")
