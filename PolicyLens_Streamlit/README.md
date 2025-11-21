# PolicyLens (Streamlit) - Standard Mode

A Streamlit app that explains policy documents in plain language with a professional UI.
This project includes:
- `app.py` — Streamlit application (upload PDF/TXT or paste text, choose tone/length, explain, export).
- `utils/llm_client.py` — lightweight adapter to call an LLM (OpenAI or HuggingFace). You can replace it with your own backend.
- `utils/prompt.py` — prompt builder for explanations.
- `examples/sample_policy.txt` — sample policy to test.
- `requirements.txt` — Python dependencies.
- `assets/logo.png` — placeholder small logo.
- `LICENSE`, `.gitignore`

## Quickstart
1. Create and activate venv:
   - Windows:
     ```ps1
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```
3. Set your API key (optional, if you want remote LLM calls):
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```
5. Open the URL printed by Streamlit (usually http://localhost:8501).

## Notes
- The included `utils/llm_client.py` is a small adapter. If you prefer not to use an external LLM, replace `explain_text` in `app.py` with your own summarizer.
- The "Export as PDF" uses `fpdf`. If you want higher-fidelity exports, replace with `reportlab` or `WeasyPrint`.
