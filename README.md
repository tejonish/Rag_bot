# 🚀 AI Hiring Copilot

A **LangGraph-powered, agentic, multi-agent AI Hiring Copilot** that evaluates resume–job fit using stateful workflows, conditional routing, semantic matching, and personalized learning roadmaps.

🔗 **Live Demo:** https://tejonish-rag-bot.streamlit.app

📂 **GitHub:** https://github.com/tejonish/Rag_bot

> ⚠️ First load may take ~20–30 seconds due to free-tier cold start.

---

## 🔍 Features

* 📄 Upload resume (PDF)
* 🧠 Extract skills using LLM
* 🤝 Semantic matching with job description
* 🎯 Job fit scoring
* ⚠️ Skill gap detection
* 📚 Personalized learning roadmap (concise & actionable)
* 📊 PDF report generation (HR & Candidate modes)

---

## 🧠 Architecture

### 🔹 LangGraph Workflow

This application uses **LangGraph's StateGraph** to orchestrate a stateful multi-agent workflow with conditional routing based on the candidate's job-fit score.

```text
Resume + Job Description
          │
          ▼
     Extractor Node
          │
          ▼
      Matcher Node
          │
          ▼
      Scorer Node
          │
          ▼
     Score >= 80?
      /         \
    Yes         No
     │           │
     ▼           ▼
 Formatter   Roadmap Node
      \         /
       ▼       ▼
    Final Report
```

### 🔹 Agentic Pipeline

* LLM-based controller dynamically decides execution steps
* Enables flexible, adaptive workflow instead of static pipelines

### 🔹 Multi-Agent System

* **Extractor Agent** → skill extraction
* **Matcher Agent** → semantic similarity matching
* **Scorer Agent** → fit score calculation
* **Roadmap Agent** → learning recommendations

### 🔹 Multi-Model Design

* **LLM (Groq / LLaMA-3)** → reasoning & generation
* **Sentence Transformers** → semantic similarity

---

## 🛠 Tech Stack

**Core**

* Python
* Streamlit

**AI / ML**

* Groq (LLaMA-3)
* Sentence Transformers
* FAISS (vector similarity)

**LLM Orchestration**

* LangGraph (StateGraph)
* LangChain

**PDF Processing**

* PyPDF
* ReportLab

**Utilities**

* python-dotenv


---

## 📁 Project Structure

```plaintext
Rag_bot/
│── app.py
│── rag_core.py
│── requirements.txt
│── Dockerfile
│── README.md
│
├── agents/                     # AI agents
│   ├── controller.py
│   ├── extractor.py
│   ├── matcher_agent.py
│   ├── scorer_agent.py
│   ├── roadmap_agent.py
│   ├── formatter_agent.py
│   └── embedding_model.py
│
├── langgraph_version/          # LangGraph workflow implementation
│   ├── graph_state.py
│   ├── hiring_graph.py
│   ├── llm.py
│   ├── routers.py
│   ├── test_graph.py
│   ├── test_imports.py
│   │
│   └── nodes/
│       ├── extractor_node.py
│       ├── matcher_node.py
│       ├── scorer_node.py
│       ├── roadmap_node.py
│       └── formatter_node.py
│
├── modules/                    # Application modules
│   ├── ats.py
│   ├── candidate.py
│   ├── github.py
│   ├── interview.py
│   ├── jd_analysis.py
│   ├── report.py
│   ├── resume.py
│   └── verification.py
│
├── assets/
└── .gitignore/
```

---

## ▶️ Run Locally

```bash
git clone https://github.com/tejonish/Rag_bot.git
cd Rag_bot

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

---

## ☁️ Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to Streamlit Community Cloud
3. Select repo → `app.py`
4. Add secret:

```toml
GROQ_API_KEY = "your_api_key_here"
```

5. Deploy 🚀

---

## ⚙️ Key Design Decisions

**Why Multi-Model?**

* LLM handles reasoning
* Embedding model improves semantic matching accuracy

**Why Agentic Pipeline?**

* Dynamic step execution
* More flexible than static pipelines

**Why FAISS?**

* Fast in-memory vector search
* Works well in ephemeral cloud environments

---

## 📸 How It Works

```plaintext
Upload Resume → Paste JD → Analyze → Get:
✔ Fit Score
✔ Matching / Missing Skills
✔ Learning Roadmap
```

---

## 🚀 Future Improvements

* Feedback loop for adaptive learning
* Skill normalization layer
* Domain-specific tuning
* UI analytics dashboard

---

## ⚙️ CI Status (GitHub Actions Badge Below)
![CI](https://github.com/tejonish/Rag_bot/actions/workflows/ci.yml/badge.svg)

---

## ⭐ Why this Project?

This project demonstrates:

* System design thinking
* Agentic workflows
* Multi-agent orchestration
* Multi-model AI integration
* Real-world hiring intelligence application
* LangGraph StateGraph orchestration with conditional routing

---

## 🙌 Feedback

Feel free to open issues or suggest improvements!
