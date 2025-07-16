# ApplyAI – Local Resume & Cover Letter Generator (RAG)

ApplyAI is a **local Streamlit application** that uses Retrieval‑Augmented Generation (RAG) with GPT‑4 to generate:
- A **tailored resume**
- A **tailored cover letter**

The system uses:
- A full resume (`context/Resume_Full.md`)
- A set of example cover letters (`context/CoverLetters/*.md`)
- A job posting entered through the UI

It runs locally, stores no data externally, and outputs Markdown files that you can download.

---

## ✨ Features
- ✅ **RAG with FAISS:** retrieves top matching cover letters as context.
- ✅ **LLM‑powered tailoring:** GPT‑4 generates resume and cover letter.
- ✅ **Streamlit UI:** simple form inputs with progress indicators and download buttons.
- ✅ **Local only:** no external storage, everything saved under `outputs/`.

---

## ⚙️ Installation

**Prerequisites:**  
- Python 3.10+
- An OpenAI API key with access to GPT‑4
- [Conda](https://docs.conda.io/en/latest/miniconda.html) or virtualenv

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ApplyAI.git
cd ApplyAI
```

### 2. Create and activate a conda environment (preferred)
```bash
conda create -n applyai python=3.10
conda activate applyai
```

Alternatively, you can use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file in the project root with your API key:
```env
OPENAI_API_KEY=sk-...
```

---

## 🚀 Usage

Run the app:
```bash
streamlit run main.py
```

Example output directory structure:
```
outputs/05_24_2025_research_associate_ab12cd34/
   resume_research_associate_ucb_05_24_2025.md
   cover_letter_research_associate_ucb_05_24_2025.md
```

---

## 🔧 Customization
- Edit `context/Resume_Full.md` with your master resume.
- Add or modify example cover letters under `context/CoverLetters/`.
- Adjust prompts in `app/prompts/prompt_resume.txt` and `app/prompts/prompt_coverletter.txt`.

---