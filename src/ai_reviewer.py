"""
AI-powered code review.

Sends the user's code, along with static-analysis findings, to either
OpenAI or Google Gemini and asks for a structured review: bugs,
improvements, and best-practice explanations.
"""

REVIEW_PROMPT_TEMPLATE = """You are an expert Python code reviewer. Review the following code carefully.

Static analysis findings (Pylint/Flake8) are provided for extra context - use them,
but also look beyond them for logic errors, edge cases, security issues, and
design problems that linters can't catch.

Structure your response in Markdown with these exact sections:

## 🐛 Bugs & Issues
List concrete bugs or correctness problems you find. If none, say so.

## 🔧 Suggested Improvements
Concrete, actionable suggestions (performance, readability, structure, naming, etc.)

## 📘 Best Practices
Explain 2-4 relevant Python best practices this code should follow, with brief reasoning.

## ✅ Overall Assessment
A short (2-3 sentence) summary verdict and a quality score out of 10.

--- CODE TO REVIEW ---
```python
{code}
```

--- STATIC ANALYSIS OUTPUT ---
{static_output}
"""


def build_prompt(code: str, static_output: str) -> str:
    return REVIEW_PROMPT_TEMPLATE.format(code=code, static_output=static_output)


def review_with_openai(code: str, static_output: str, api_key: str, model: str = "gpt-4o-mini") -> str:
    """Get a code review from an OpenAI chat model."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("The 'openai' package is not installed. Run: pip install openai") from exc

    client = OpenAI(api_key=api_key)
    prompt = build_prompt(code, static_output)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a meticulous, helpful senior Python engineer performing a code review."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def review_with_gemini(code: str, static_output: str, api_key: str, model: str = "gemini-1.5-flash") -> str:
    """Get a code review from a Google Gemini model."""
    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError(
            "The 'google-generativeai' package is not installed. Run: pip install google-generativeai"
        ) from exc

    genai.configure(api_key=api_key)
    prompt = build_prompt(code, static_output)

    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(prompt)
    return response.text


def get_review(code: str, static_output: str, provider: str, api_key: str, model: str = None) -> str:
    """
    Dispatch to the correct provider.

    provider: "OpenAI" or "Gemini"
    """
    if not api_key:
        raise ValueError("No API key provided.")

    if provider == "OpenAI":
        return review_with_openai(code, static_output, api_key, model or "gpt-4o-mini")
    elif provider == "Gemini":
        return review_with_gemini(code, static_output, api_key, model or "gemini-1.5-flash")
    else:
        raise ValueError(f"Unknown provider: {provider}")
