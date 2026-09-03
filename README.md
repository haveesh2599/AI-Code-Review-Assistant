# 🤖 AI Code Review Assistant

A Streamlit app that reviews Python code by combining:
- **Static analysis** — Pylint + Flake8 (style, errors, code smells)
- **AI review** — OpenAI or Gemini (bugs, design suggestions, best practices, in plain English)

## Project Structure

```
ai-code-review-assistant/
├── app.py                  # Streamlit UI (entry point)
├── requirements.txt
├── src/
│   ├── static_analysis.py  # Pylint / Flake8 runners
│   └── ai_reviewer.py      # OpenAI / Gemini review logic
└── README.md
```

## Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get an API key** for whichever provider you want to use:
   - OpenAI: https://platform.openai.com/api-keys
   - Gemini: https://aistudio.google.com/app/apikey

   You don't need both — pick one in the app's sidebar.

## Run the app

```bash
streamlit run app.py
```

This opens the app in your browser (usually at `http://localhost:8501`).

## How to use it

1. Choose a provider (OpenAI or Gemini) and paste your API key in the sidebar.
   (The key is only kept in memory for your session — it's never saved to disk.)
2. Paste Python code into the text box, or upload a `.py` file.
3. Click **Run Review**.
4. You'll get:
   - Raw Pylint and Flake8 output (in tabs)
   - An AI-generated review with **Bugs**, **Suggested Improvements**, **Best Practices**, and an **Overall Assessment** with a score out of 10.

## Ideas for extending this project

- **Caching**: cache AI responses by code hash so re-running the same snippet doesn't re-spend tokens.
- **Diff mode**: let users paste "before" and "after" code and review just the changes.
- **GitHub integration**: pull a file directly from a GitHub URL or PR.
- **History**: store past reviews in SQLite so users can look back at them.
- **Batch mode**: upload a whole folder/zip and review every `.py` file in it.
- **Custom rules**: let users write their own "house style" prompt add-ons (e.g. "always flag missing type hints").
- **Severity scoring**: parse the AI's bug list into a structured table with severity levels.

## Notes

- Static analysis runs locally and needs no API key — it works even without AI configured.
- If Pylint/Flake8 aren't installed, `pip install -r requirements.txt` will fix that.
- Keep API keys out of source control — never commit a real key. A `.env` file is not required since keys are entered in the UI, but you can wire one up with `python-dotenv` if you'd rather not paste it each time.
