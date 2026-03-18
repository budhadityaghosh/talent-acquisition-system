# 🚀 TalentAI — Intelligent Talent Acquisition System

An end-to-end **AI-powered recruitment automation platform** that streamlines candidate sourcing, resume screening, and hiring workflows using **Generative AI, Multi-Agent Systems, and Retrieval-Augmented Generation (RAG)**.

---

## 🌐 Live Demo

🔗 https://talent-acquisition-system-kkpw5w9rk38qnfbydupabt.streamlit.app/

## 📦 Repository

🔗 https://github.com/budhadityaghosh/talent-acquisition-system

---

# 🧠 Project Overview

TalentAI is designed to **automate the entire recruitment lifecycle**, reducing manual effort, eliminating bias, and improving decision quality.

The system replaces repetitive HR tasks with an **AI-driven pipeline of autonomous agents**, ensuring:

* Faster candidate screening
* Consistent evaluation
* Bias-free hiring decisions
* Real-time communication with candidates

---

# 🎯 Key Features

## 👨‍💼 HR Portal

* Job posting with duplicate prevention
* Real-time pipeline dashboard
* Candidate database & filtering
* Screening result visualization
* Interview slot management
* Analytics (hiring funnel, score distribution)

## 👩‍💻 Candidate Portal

* Resume upload (PDF parsing)
* AI-powered HR chatbot
* Job application tracking
* Interview slot booking
* Telegram notifications

## 🤖 AI Pipeline (Core System)

* Multi-agent architecture using CrewAI
* Context-aware resume screening (RAG)
* Structured JSON outputs for automation
* Bias filtering before evaluation

---

# 🧱 System Architecture

## 🖼️ Architecture Diagram

```text
+-------------------+        +-------------------+        +----------------------+
|   HR Portal       |        |  Candidate Portal |        |  Telegram Bot System |
|-------------------|        |-------------------|        |----------------------|
| - Post Jobs       |        | - Apply for Job   |        | - Shortlist Alerts   |
| - Run Pipeline    |        | - Upload Resume   |        | - Interview Confirm  |
| - Dashboard       |        | - Chatbot         |        | - Notifications      |
+--------+----------+        +--------+----------+        +----------+-----------+
         |                            |                              |
         |                            |                              |
         +------------+---------------+--------------+---------------+
                      |                              |
                      v                              v
             +-------------------------------+
             |        AI PIPELINE            |
             |-------------------------------|
             | Agent 1: Sourcing             |
             | Agent 2: RAG Screening        |
             | Agent 3: Engagement           |
             | Bias Filter Module            |
             | Groq LLM (Inference Engine)   |
             +---------------+---------------+
                             |
                             v
        +---------------------------------------------+
        |                 DATABASE LAYER              |
        |---------------------------------------------|
        | Supabase (PostgreSQL)                      |
        | - jobs                                     |
        | - candidates                               |
        | - interview_slots                          |
        | - chat_logs                                |
        |                                             |
        | ChromaDB (Vector DB)                        |
        | - job embeddings (RAG context)              |
        | - candidate embeddings                     |
        +---------------------------------------------+
```

---

## 🧩 Architecture Explanation

The system is divided into **five major layers**:

### 1. Presentation Layer

* **HR Portal (Streamlit):** Internal dashboard for recruiters
* **Candidate Portal:** Public interface for applicants

---

### 2. AI Processing Layer (Core Intelligence)

#### 🔹 Agent 1 — Sourcing Specialist

* Scores candidate profiles (0–100)
* Filters unqualified candidates early

#### 🔹 Agent 2 — Screening Expert (RAG)

* Retrieves job context from ChromaDB
* Evaluates resumes against real requirements
* Outputs structured JSON:

  * screening_score
  * skills_matched / missing
  * recommendation

#### 🔹 Agent 3 — Engagement Coordinator

* Generates HR reports
* Identifies top candidates
* Suggests next steps

---

### 3. Bias Filtering Layer

* Removes:

  * Name
  * Gender
  * Location
  * University
* Ensures **fair and unbiased evaluation**

---

### 4. Data Layer

#### 🗄️ Supabase (PostgreSQL)

Stores structured data:

* Jobs
* Candidates
* Interview slots
* Chat logs

#### 🧠 ChromaDB (Vector Database)

* Stores job descriptions as embeddings
* Enables **Retrieval-Augmented Generation (RAG)**

---

### 5. Communication Layer

* Telegram Bot integration
* Real-time:

  * Shortlist notifications
  * Interview confirmations

---

# 🧠 Generative AI Implementation

## 🔍 Retrieval-Augmented Generation (RAG)

* Job descriptions embedded into vector DB
* Retrieved dynamically during screening
* Ensures **context-aware evaluation**

---

## 🤖 Multi-Agent Orchestration

* Built using CrewAI
* Sequential execution pipeline
* Each agent writes to database

---

## 📦 Structured JSON Output

* Machine-readable LLM responses
* Ensures pipeline stability
* Includes fallback handling

---

# ⚙️ Tech Stack

| Layer         | Technology       |
| ------------- | ---------------- |
| Frontend      | Streamlit        |
| LLM API       | Groq (LLaMA 3)   |
| Agents        | CrewAI + LiteLLM |
| Backend DB    | Supabase         |
| Vector DB     | ChromaDB         |
| Notifications | Telegram Bot API |
| Parsing       | PyPDF2           |
| Analytics     | Plotly + Pandas  |

---

# 🚀 How to Run Locally

```bash
git clone https://github.com/budhadityaghosh/talent-acquisition-system
cd talent-acquisition-system
pip install -r requirements.txt
streamlit run app.py
```

---

# 📊 Results

* Fully automated recruitment pipeline
* Real-time dashboard updates
* High accuracy with RAG-based screening
* Bias-free candidate evaluation
* Zero infrastructure cost (free-tier tools)

---

# 🔮 Future Improvements

* LinkedIn integration for real candidates
* Advanced embedding models
* Multi-round interview workflows
* Feedback loop for model improvement

---

# 👨‍💻 Contributors

* Anik Mandal
* Aryak Pal
* Aswint Guha
* Budhaditya Ghosh

---

# 📄 Documentation

📎 Full project report available
(See attached academic report for detailed explanation)

---

# 📌 License

This project is developed for academic purposes under Generative AI coursework.
