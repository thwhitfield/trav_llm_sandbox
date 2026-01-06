import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from google import genai
from src.trav_llm.llm import get_model_response

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LLM Model Comparison",
    page_icon="🤖",
    layout="wide"
)

# Initialize clients
@st.cache_resource
def get_clients():
    """Initialize API clients with caching"""
    clients = {}

    # OpenAI
    if os.getenv("OPENAI_API_KEY"):
        clients["openai"] = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Anthropic
    if os.getenv("ANTHROPIC_API_KEY"):
        clients["anthropic"] = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Google
    if os.getenv("GEMINI_API_KEY"):
        clients["google"] = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    return clients

# Define available models
MODELS = {
    "OpenAI": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo"
    ],
    "Anthropic": [
        "claude-opus-4-5-20251101",
        "claude-sonnet-4-5-20250929",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022"
    ],
    "Google": [
        "gemini-2.0-flash-exp",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]
}

# Map providers to client keys
PROVIDER_CLIENT_MAP = {
    "OpenAI": "openai",
    "Anthropic": "anthropic",
    "Google": "google"
}

def main():
    st.title("🤖 LLM Model Comparison Tool")
    st.markdown("Compare outputs from different language models side-by-side")

    # Initialize session state
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "selected_for_comparison" not in st.session_state:
        st.session_state.selected_for_comparison = []

    clients = get_clients()

    # Check if any API keys are configured
    if not clients:
        st.error("⚠️ No API keys found. Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, and/or GEMINI_API_KEY environment variables.")
        st.stop()

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")

        # Prompt input
        prompt = st.text_area(
            "Enter your prompt:",
            placeholder="Write a haiku about coding...",
            height=150
        )

        st.divider()

        # Model selection
        st.subheader("Select Models to Run")
        selected_models = []

        for provider, models in MODELS.items():
            client_key = PROVIDER_CLIENT_MAP[provider]
            if client_key in clients:
                with st.expander(f"**{provider}**", expanded=True):
                    for model in models:
                        if st.checkbox(model, key=f"select_{model}"):
                            selected_models.append((provider, model))

        st.divider()

        # Run button
        run_button = st.button("🚀 Run All Selected Models", type="primary", use_container_width=True)

        if run_button:
            if not prompt.strip():
                st.error("Please enter a prompt")
            elif not selected_models:
                st.error("Please select at least one model")
            else:
                st.session_state.responses = {}
                st.session_state.selected_for_comparison = []

                with st.spinner("Running models..."):
                    for provider, model in selected_models:
                        client_key = PROVIDER_CLIENT_MAP[provider]
                        try:
                            response = get_model_response(
                                clients[client_key],
                                model,
                                prompt
                            )
                            st.session_state.responses[model] = {
                                "provider": provider,
                                "response": response,
                                "prompt": prompt
                            }
                        except Exception as e:
                            st.session_state.responses[model] = {
                                "provider": provider,
                                "response": f"Error: {str(e)}",
                                "prompt": prompt
                            }

                st.success(f"✅ Completed {len(selected_models)} model runs!")
                st.rerun()

    # Main content area
    if not st.session_state.responses:
        st.info("👈 Configure your prompt and select models in the sidebar to get started")
    else:
        # Display current prompt
        st.subheader("Current Prompt")
        first_response = next(iter(st.session_state.responses.values()))
        st.code(first_response["prompt"], language=None)

        st.divider()

        # Comparison selection
        st.subheader("Select Models to Compare")

        # Create columns for checkboxes
        cols = st.columns(min(len(st.session_state.responses), 4))
        for idx, model_name in enumerate(st.session_state.responses.keys()):
            with cols[idx % len(cols)]:
                if st.checkbox(
                    f"{model_name}",
                    key=f"compare_{model_name}",
                    value=model_name in st.session_state.selected_for_comparison
                ):
                    if model_name not in st.session_state.selected_for_comparison:
                        st.session_state.selected_for_comparison.append(model_name)
                else:
                    if model_name in st.session_state.selected_for_comparison:
                        st.session_state.selected_for_comparison.remove(model_name)

        st.divider()

        # Display responses
        if st.session_state.selected_for_comparison:
            st.subheader("Side-by-Side Comparison")

            # Create columns for side-by-side comparison
            num_selected = len(st.session_state.selected_for_comparison)
            cols = st.columns(num_selected)

            for idx, model_name in enumerate(st.session_state.selected_for_comparison):
                with cols[idx]:
                    data = st.session_state.responses[model_name]
                    st.markdown(f"### {model_name}")
                    st.caption(f"Provider: {data['provider']}")

                    # Display response in a container
                    with st.container(border=True):
                        st.markdown(data["response"])
        else:
            st.info("Select models above to view side-by-side comparison")

            # Show all responses in expandable sections
            st.subheader("All Responses")
            for model_name, data in st.session_state.responses.items():
                with st.expander(f"**{model_name}** ({data['provider']})"):
                    st.markdown(data["response"])

if __name__ == "__main__":
    main()
