"""
AI Code Review Assistant
-------------------------
A Streamlit app that reviews Python code using static analysis
(Pylint + Flake8) combined with an AI model (OpenAI or Gemini)
for deeper bug-finding, suggestions, and best-practice explanations.

Run with:
    streamlit run app.py
"""

import streamlit as st

from src.static_analysis import run_all
from src.ai_reviewer import get_review

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🤖",
    layout="wide",
)

# ----------------------------- Sidebar -----------------------------
st.sidebar.title("⚙️ Settings")

provider = st.sidebar.selectbox("AI Provider", ["OpenAI", "Gemini"])

default_models = {
    "OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
    "Gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
}
model = st.sidebar.selectbox("Model", default_models[provider])

api_key = st.sidebar.text_input(
    f"{provider} API Key",
    type="password",
    help="Your key is used only for this session and is never stored.",
)

st.sidebar.markdown("---")
run_static = st.sidebar.checkbox("Run static analysis (Pylint + Flake8)", value=True)
run_ai = st.sidebar.checkbox("Run AI review", value=True)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Get an API key:\n"
    "- OpenAI: platform.openai.com/api-keys\n"
    "- Gemini: aistudio.google.com/app/apikey"
)

# ----------------------------- Main area -----------------------------
st.title("🤖 AI Code Review Assistant")
st.write(
    "Paste Python code below (or upload a `.py` file) to get static-analysis "
    "results and an AI-powered review covering bugs, improvements, and best practices."
)

col_input, _ = st.columns([1, 0.001])  # keep input full-width but consistent layout

uploaded_file = st.file_uploader("Upload a .py file (optional)", type=["py"])

default_code = '''def add_numbers(a, b):
    result = a+b
    return result

def divide(a, b):
    return a / b

x = add_numbers(5, "3")
print(divide(10, 0))
'''

if uploaded_file is not None:
    code_input = uploaded_file.read().decode("utf-8")
else:
    code_input = st.text_area(
        "Or paste your Python code here",
        value=default_code,
        height=300,
    )

review_clicked = st.button("🔍 Run Review", type="primary")

if review_clicked:
    if not code_input.strip():
        st.warning("Please paste some code or upload a file first.")
        st.stop()

    if run_ai and not api_key:
        st.warning(f"Please enter your {provider} API key in the sidebar to run the AI review, "
                    "or uncheck 'Run AI review'.")
        st.stop()

    st.subheader("📄 Your Code")
    st.code(code_input, language="python")

    static_output_combined = ""

    if run_static:
        st.subheader("🧪 Static Analysis")
        with st.spinner("Running Pylint and Flake8..."):
            results = run_all(code_input)

        tab_pylint, tab_flake8 = st.tabs(["Pylint", "Flake8"])
        with tab_pylint:
            st.code(results["pylint"], language="text")
        with tab_flake8:
            st.code(results["flake8"], language="text")

        static_output_combined = (
            f"PYLINT:\n{results['pylint']}\n\nFLAKE8:\n{results['flake8']}"
        )

    if run_ai:
        st.subheader("🧠 AI Review")
        with st.spinner(f"Asking {provider} ({model}) for a review..."):
            try:
                review_text = get_review(
                    code=code_input,
                    static_output=static_output_combined or "No static analysis was run.",
                    provider=provider,
                    api_key=api_key,
                    model=model,
                )
                st.markdown(review_text)
            except Exception as e:
                st.error(f"AI review failed: {e}")

st.markdown("---")
st.caption("Built with Streamlit · Pylint · Flake8 · OpenAI/Gemini APIs")
