# 🚀 TalentAI — Intelligent Talent Acquisition System

An end-to-end **AI-powered recruitment automation platform** that streamlines candidate sourcing, resume screening, and hiring workflows using **Generative AI, Multi-Agent Systems, and Retrieval-Augmented Generation (RAG)**.

---

## 🌐 Live Demo

🔗 https://talent-acquisition-system-kkpw5w9rk38qnfbydupabt.streamlit.app/

## 📦 Repository

🔗 https://github.com/budhadityaghosh/talent-acquisition-system

---

## 📄 Documentation

* 📎 **Project Report:** [View Full Report](./docs/TalentAI_Report.pdf)

---

# 🧠 Project Overview

TalentAI automates the **entire recruitment lifecycle**, reducing manual effort and eliminating bias through an AI-driven pipeline.

✔ Automated resume screening
✔ Context-aware evaluation using RAG
✔ Multi-agent decision making
✔ Real-time candidate communication

---

# 🎯 Key Features

## 👨‍💼 HR Portal

* Job posting & pipeline trigger
* Candidate dashboard & analytics
* Screening result visualization
* Interview scheduling

## 👩‍💻 Candidate Portal

* Resume upload (PDF parsing)
* AI HR chatbot
* Interview slot booking
* Telegram notifications

## 🤖 AI Pipeline

* Multi-agent architecture using CrewAI
* RAG-based resume screening
* Structured JSON outputs
* Bias filtering system

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
             | Groq LLM                      |
             +---------------+---------------+
                             |
                             v
        +---------------------------------------------+
        |             DATABASE LAYER                  |
        |---------------------------------------------|
        | Supabase (PostgreSQL)                      |
        | ChromaDB (Vector DB for RAG)               |
        +---------------------------------------------+
```

---

## 🧩 Architecture Explanation

### 1. Presentation Layer

* HR Portal (Streamlit dashboard)
* Candidate Portal (application interface)

---

### 2. AI Processing Layer

* **Agent 1:** Candidate sourcing & filtering
* **Agent 2:** Resume screening using RAG
* **Agent 3:** Engagement report generation

---

### 3. Bias Filter

Removes:

* Name
* Gender
* Location
* University

Ensures **fair and unbiased evaluation**

---

### 4. Data Layer

#### Supabase

* jobs
* candidates
* interview_slots
* chat_logs

#### ChromaDB

* Job embeddings
* Resume embeddings

---

### 5. Communication Layer

* Telegram Bot API
* Real-time notifications

---

# 🧠 Generative AI Highlights

* Retrieval-Augmented Generation (RAG)
* Multi-agent orchestration (CrewAI)
* Structured JSON outputs
* Bias filtering pipeline

---

# ⚙️ Tech Stack

| Layer         | Technology     |
| ------------- | -------------- |
| Frontend      | Streamlit      |
| LLM           | Groq (LLaMA 3) |
| Agents        | CrewAI         |
| Database      | Supabase       |
| Vector DB     | ChromaDB       |
| Notifications | Telegram Bot   |
| Parsing       | PyPDF2         |

---

# 🚀 Run Locally

```bash
git clone https://github.com/budhadityaghosh/talent-acquisition-system
cd talent-acquisition-system
pip install -r requirements.txt
streamlit run app.py
```

---

# 📊 Results

* Fully automated hiring pipeline
* Real-time dashboard updates
* Context-aware screening (RAG)
* Bias-free evaluation
* Zero infrastructure cost

---

# 🔮 Future Scope

* LinkedIn integration
* Advanced embeddings
* Multi-round interview system
* Feedback-based model tuning

---

# 👨‍💻 Contributors

* Anik Mandal
* Aryak Pal
* Aswint Guha
* Budhaditya Ghosh

---

# 📌 License

This project is developed for academic purposes under Generative AI coursework.
