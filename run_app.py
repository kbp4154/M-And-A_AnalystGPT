# run_app.py

import os
import time
import fitz  # PyMuPDF
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

# Step 1: PDF Preprocessing and Chunking
pdf_files = [
    "amazon_10k_2024.pdf", "Tesla_10k_2024.pdf", "ExxonMobil_10k_2024.pdf",
    "apple_10k_2024.pdf", "Microsoft_10k_2024.pdf", "Alphabet_10k_2024.pdf",
    "JPMorgan_10k_2024.pdf", "Johnson&Johnson_10k_2024.pdf",
    "walmart_10k_2024.pdf", "Pepsico_10k_2024.pdf"
]

all_chunks = []
for pdf_file in pdf_files:
    print(f"Processing {pdf_file}...")
    try:
        doc = fitz.open(pdf_file)
        text = "".join(page.get_text() for page in doc)
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        all_chunks.extend(chunks)
        print(f"Added {len(chunks)} chunks from {pdf_file}")
    except Exception as e:
        print(f"❌ Error processing {pdf_file}: {e}")

print(f"\n✅ Total chunks created: {len(all_chunks)}")
with open("all_chunks.txt", "w", encoding="utf-8") as f:
    for i, chunk in enumerate(all_chunks, 1):
        f.write(f"Chunk {i}: {chunk}\n")
print("📄 Chunks saved to all_chunks.txt")

# Step 2: Load Chunks
with open("all_chunks.txt", "r", encoding="utf-8") as f:
    all_chunks = [line.split(": ", 1)[1].strip() for line in f if line.startswith("Chunk")]

# Step 3: Use first 2000 for now (you can increase to 5000 later)
documents = [Document(page_content=chunk) for chunk in all_chunks[:2000]]
print(f"📄 Loaded {len(documents)} documents")

# Step 4: Embedding class
class SentenceTransformerEmbeddings:
    def __init__(self, model_name="all-MiniLM-L6-v2", use_gpu=False):
        device = "cuda" if use_gpu else "cpu"
        self.model = SentenceTransformer(model_name, device=device)

    def embed_documents(self, texts):
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text):
        return self.model.encode([text], convert_to_numpy=True)[0].tolist()

embeddings = SentenceTransformerEmbeddings(use_gpu=False)

# Step 5: Load or Build FAISS Vector Store
vector_store_path = "faiss_store"
if os.path.exists(os.path.join(vector_store_path, "index.faiss")):
    vector_store = FAISS.load_local(
        vector_store_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("📂 Vector store loaded from disk")
else:
    print("⏳ Creating FAISS vector store...")
    start = time.time()
    vector_store = FAISS.from_documents(documents, embeddings)
    print(f"✅ Vector store created in {time.time() - start:.2f} seconds")
    vector_store.save_local(vector_store_path)
    print(f"💾 Saved to '{vector_store_path}'")

# Step 6: CLI Interface
print("\n🧠 Ask questions (type 'quit' to exit):")
while True:
    query = input("\n🔎 Your query: ")
    if query.lower() == "quit":
        break
    query_embedding = embeddings.embed_query(query)
    results = vector_store.similarity_search_by_vector(query_embedding, k=5)
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:\n{doc.page_content[:300]}...")

# Step 7: (Optional) LangChain Agent
try:
    from langchain.agents import initialize_agent, Tool

    tools = [
        Tool(
            name="Search10K",
            func=lambda q: [doc.page_content for doc in vector_store.similarity_search_by_vector(embeddings.embed_query(q), k=5)],
            description="Search 10-K filings"
        )
    ]

    agent = initialize_agent(tools, embeddings, agent_type="zero-shot-react-description")
    print("\n🤖 Agent ready. Try: `agent.run('Compare Amazon and Microsoft risks')`")
except ImportError:
    print("\n⚠️ LangChain agents not installed. Run: pip install -U langchain-agents")
