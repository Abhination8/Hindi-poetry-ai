# 🪔 Hindi Poetry AI

An explainable, self-improving AI system that generates original Hindi poetry inspired by classical, Bhakti, Chhayavaad, and modern poets.

This project combines **RAG (Retrieval-Augmented Generation)**, **user feedback loops**, and **stylistic grounding** to create culturally rich and controllable Hindi poems.

---

## ✨ Features

- 📝 Generate original Hindi poems from prompts
- 🎭 Style control (Bhakti, Modern, Chhayavaad, etc.)
- 📏 Poetic forms: Free Verse, Doha, Chaupai
- 🧠 Poet-inspired RAG (Kabir, Tulsidas, Mahadevi Verma & more)
- 👍 👎 Feedback-driven quality improvement
- 📖 Explainability: see how each poem was created
- 🔗 Shareable poem links
- 💾 Persistent memory (SQLite)

---

## 🧠 Architecture Overview
User Prompt
↓
Poet RAG (JSON knowledge base)
↓
Quality RAG (liked poems)
↓
LLM (GPT-based)
↓
Poem + Explanation
↓
User Feedback → Stored → Improves future poems

---

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** OpenAI GPT (via API)
- **RAG Store:** JSON (Poets) + SQLite (Poems)
- **Database:** SQLite
- **Deployment:** Streamlit Cloud / Render

---

## 🚀 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/Abhination8/Hindi-poetry-ai.git
cd Hindi-poetry-ai

2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Set environment variables
OPENAI_API_KEY=

**🔒 Security & Ethics**
	•	No copyrighted poems are stored or reproduced
	•	Only stylistic abstractions are used
	•	User-generated content remains local to the app

**🔮 Future Enhancements**
	•	Public poem pages
	•	Vector embeddings for poems
	•	Fine-tuning using high-quality outputs
	•	Multi-language support

👤 Author

Abhishek Chaturvedi
Product Manager | 
