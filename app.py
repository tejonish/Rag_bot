import streamlit as st
import tempfile
import os
import shutil

from rag_core import build_rag_chain, summarize_resume


st.set_page_config(page_title="RAG Resume Bot", page_icon="🤖", layout="centered")

st.title("🤖 RAG Chatbot (LangChain + Llama3)")
st.caption("Upload PDF and ask questions. It answers using document context (RAG).")


def reset_vectordb():
    """Delete chroma_db to rebuild embeddings cleanly."""
    if os.path.exists("chroma_db"):
        shutil.rmtree("chroma_db")


pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

# optional reset button
if st.button("🔁 Reset Vector DB (if answers look wrong)"):
    reset_vectordb()
    st.success("Vector DB reset ✅ Upload PDF again.")

if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        temp_path = tmp.name

    st.success("PDF uploaded ✅ Building vector DB... (first time takes few seconds)")
    rag_chain = build_rag_chain(temp_path)

    st.markdown("---")
    question = st.text_input("Ask a question", placeholder="Example: Summarize my resume")

    if st.button("Ask"):
        if question.strip() == "":
            st.warning("Type a question first.")
        else:
            q = question.lower().strip()

            # ✅ Resume summary mode (no retrieval bias)
            if "summarize" in q and "resume" in q:
                with st.spinner("Summarizing full resume..."):
                    answer = summarize_resume(temp_path)

                st.markdown("## ✅ Resume Summary")
                st.write(answer)

            # ✅ RAG Q&A mode
            else:
                with st.spinner("Thinking..."):
                    result = rag_chain.invoke({"input": question})

                st.markdown("## ✅ Answer")
                st.write(result["answer"])

                with st.expander("Show chunks used"):
                    for i, doc in enumerate(result["context"], start=1):
                        st.markdown(f"### Chunk {i}")
                        st.write(doc.page_content)
