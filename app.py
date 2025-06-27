# app.py
import streamlit as st
from rag_core.rag_chain import build_rag_chain
from loguru import logger

st.title("M&A Analyst GPT")
st.write("Real-time analysis of 2024 10-K filings for M&A professionals")

try:
    rag_chain = build_rag_chain()
    st.success("Vector store and RAG chain initialized.")
except Exception as e:
    st.error(f"Failed to initialize RAG chain: {e}")
    logger.error(f"Failed to initialize RAG chain: {e}")
    st.stop()

query = st.text_input("Enter your question (e.g., 'What is Coca-Cola’s net income in 2024?')")
if st.button("Submit"):
    if query:
        with st.spinner("Processing..."):
            try:
                result = rag_chain.invoke({"query": query})
                st.write("**Query:**")
                st.write(result["query"])
                st.write("**Answer:**")
                st.write(result["answer"])
            except Exception as e:
                st.error(f"Error processing query: {e}")
                logger.error(f"Error during processing: {e}")
    else:
        st.warning("Please enter a question.")