# AI Job Application & Resume Analyzer

An AI-powered web application that compares a resume with a job description and provides an ATS-style match score, matching skills, missing skills, recommended keywords, and improvement suggestions.

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- MySQL
- PyPDF
- Pandas
- NLP/LLM analysis

## Project Structure

```text
AI-Resume-Analyzer/
├── app.py
├── database.py
├── resume_parser.py
├── ai_analyzer.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── database/
    └── schema.sql
```

## 1. Create virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

## 2. Install packages

```bash
pip install -r requirements.txt
```

## 3. Configure environment

Copy `.env.example` to `.env`.

Add your Gemini API key and MySQL credentials:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=resume_analyzer
```

## 4. Create MySQL database

Open MySQL Workbench and run:

```sql
SOURCE path/to/AI-Resume-Analyzer/database/schema.sql;
```

Or open `database/schema.sql`, copy its contents, and execute it in MySQL Workbench.

## 5. Run the application

```bash
streamlit run app.py
```

## Features

- PDF resume upload
- Resume text extraction
- Job description analysis
- Gemini AI comparison
- ATS-style match score
- Matching skills
- Missing skills
- Recommended keywords
- Resume improvement suggestions
- MySQL application history
- Match-score chart

## Important

Never upload `.env` or your Gemini API key to GitHub.
