import os
import requests

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

def explain_with_openai(prompt: str, max_tokens: int = 600):
    # Minimal OpenAI call using Chat Completions API
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY not set.')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}
    payload = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'temperature': 0.2,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    if 'choices' in data and len(data['choices'])>0:
        return data['choices'][0].get('message', {}).get('content', '')
    return str(data)

def explain_with_hf(prompt: str):
    if not HUGGINGFACE_API_TOKEN:
        raise RuntimeError('HUGGINGFACE_API_TOKEN not set.')
    url = 'https://api-inference.huggingface.co/models/google/flan-t5-large'
    headers = {'Authorization': f'Bearer {HUGGINGFACE_API_TOKEN}'}
    payload = {'inputs': prompt, 'options': {'wait_for_model': True}}
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list) and len(data)>0 and 'generated_text' in data[0]:
        return data[0]['generated_text']
    return str(data)

def explain_text(prompt: str):
    # prefer OpenAI, fallback to HF
    if OPENAI_API_KEY:
        return explain_with_openai(prompt)
    if HUGGINGFACE_API_TOKEN:
        return explain_with_hf(prompt)
    # No remote LLM configured — return a placeholder instruction so user can replace with local logic.
    return ('[NO API CONFIGURED] Replace utils/llm_client.explain_text with your own summarizer, '
            'or set OPENAI_API_KEY / HUGGINGFACE_API_TOKEN in environment to enable remote LLM calls.')
