import os
import requests


API_URL = "https://api.openai.com/v1/chat/completions"


def summarize_build_log(log_text, api_key=None, model="gpt-5.5"):
    """
    Summarize a CI/CD build error log using an LLM.
    """

    if not isinstance(log_text, str) or not log_text.strip():
        raise ValueError("Build log cannot be empty")

    api_key = api_key or os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    # Keep the most recent part of a long build log
    log_text = log_text[-12000:]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a CI/CD build failure analysis assistant. "
                    "Explain build errors in simple language. "
                    "Identify the error, possible cause, and suggested fix."
                )
            },
            {
                "role": "user",
                "content": f"Analyze this build log:\n\n{log_text}"
            }
        ]
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    try:
        summary = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise ValueError("Invalid response received from LLM API")

    if not summary:
        raise ValueError("LLM returned an empty summary")

    return summary.strip()