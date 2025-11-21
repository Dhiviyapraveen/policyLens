def build_prompt(policy_text: str, tone: str = 'Professional', length: str = 'Medium') -> str:
    header = ("You are an expert at explaining legal and policy documents in clear, non-technical language.\n\n")
    instructions = f"Tone: {tone}. Desired length: {length}. Provide: 1) short summary, 2) key points, 3) clause-by-clause breakdown, 4) risks/impacts, 5) recommended actions. Keep the output structured with headings.\n\n"
    prompt = header + instructions + "Policy:\n" + policy_text + "\n\nExplanation:\n"
    return prompt
