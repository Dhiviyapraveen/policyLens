import os
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyBPkBJnRpMu4aMcv_r1z928vEChRdX3WCY"

def explain_text(prompt: str, max_tokens: int = 800):
    if not GEMINI_API_KEY:
        raise RuntimeError('GEMINI_API_KEY not set.')
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    resp = model.generate_content(prompt)
    return getattr(resp, 'text', '') or ''
