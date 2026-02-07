from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
import os


from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


def extract_full_text(pdf_path: str) -> str:  
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return "\n".join([d.page_content for d in docs])


def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )


def build_rag_chain(pdf_path: str):
  
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=250)
    chunks = splitter.split_documents(docs)

    #embeddings = HuggingFaceEmbeddings(
    #    model_name="sentence-transformers/all-MiniLM-L6-v2"
    #)

    embeddings = FastEmbedEmbeddings()

    db = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8, "fetch_k": 30, "lambda_mult": 0.7}
    )

    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant.
Answer ONLY using the context from the resume.
If not present in context, say: "Not found in the resume."

Important:
- If multiple internships exist in context, include ALL.

Context:
{context}

Question:
{input}

Answer:"""
    )

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

    return rag_chain


def summarize_resume(pdf_path: str) -> str:
    text = extract_full_text(pdf_path)
    llm = get_llm()

    prompt = f"""
You are a professional resume reviewer.
Summarize the resume into clean structured bullet points.

Format:
Headline:
- ...

Education:
- ...

Internships:
- ...

Projects:
- ...

Skills:
- ...

Achievements/Leadership:
- ...

Resume Text:
{text}

Rules:
- Keep it short and crisp
- Include all internships if present
- Do NOT invent anything
"""

    return llm.invoke(prompt).content
