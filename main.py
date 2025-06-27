# main.py
from rag_core.rag_chain import build_rag_chain
from loguru import logger

def main():
    print("🔍 Loading vector database...")
    try:
        rag_chain = build_rag_chain()
        print("✅ Vector store loaded successfully.")
        print("🧠 RAG chain initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize RAG chain: {e}")
        print(f"⚠️ Failed to initialize RAG chain: {e}")
        return

    print("\n💬 Ask any question based on the 10-K filings (type 'exit' to quit)\n")
    while True:
        query = input("❓ Your question: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting...")
            break
        try:
            result = rag_chain.invoke({"query": query})
            print(f"\n📌 Final Answer:\n {result['answer']}")
        except Exception as e:
            logger.error(f"Error during processing: {e}")
            print(f"⚠️ Error during processing: {e}")

if __name__ == "__main__":
    main()