# Resume RAG Chatbot

A cloud-deployed Retrieval-Augmented Generation (RAG) application that allows users to upload a PDF resume and ask context-aware questions.

## 🚀 Features
- Upload PDF resumes
- Ask natural-language questions
- Context-grounded answers using RAG
- In-memory vector search using FAISS
- Session reset to load a new document
- Deployed on Streamlit Cloud

## 🧠 Architecture
1. PDF text extraction using PyPDF
2. Text chunking with overlap
3. Embeddings via FastEmbed
4. Vector storage using FAISS
5. MMR-based semantic retrieval
6. Answer generation using LLaMA-3 (Groq)
7. Streamlit UI and session handling

## 🛠 Tech Stack
- Python
- LangChain
- FAISS
- FastEmbed
- Groq (LLaMA-3)
- Streamlit

## ⚙️ Design Decisions
**Why FAISS instead of Chroma?**
- Streamlit Cloud uses ephemeral containers
- Persistent databases introduce tenant issues
- Vectors are rebuilt per upload
- FAISS ensures reliability and simplicity

## ▶️ Run Locally
```bash
git clone https://github.com/tejonish/Rag_bot.git
cd Rag_bot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
# Resume RAG Chatbot

[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Streamlit-red?logo=streamlit)](https://tejonish-rag-bot.streamlit.app)

> First load may take ~30 seconds due to free-tier cold start.
