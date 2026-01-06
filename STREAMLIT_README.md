# LLM Model Comparison Streamlit App

A simple Streamlit app to compare outputs from different language models side-by-side.

## Features

- **Multi-provider support**: OpenAI, Anthropic, and Google models
- **Batch execution**: Run the same prompt across multiple models at once
- **Side-by-side comparison**: Select specific models to view outputs side-by-side
- **Clean interface**: Easy-to-use sidebar configuration and responsive layout

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Create a `.env` file in the project root with your API keys:
```bash
cp .env.example .env
```

Then edit `.env` and add your actual API keys:
```
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
```

You only need to set the API keys for the providers you want to use.

3. Run the app:
```bash
streamlit run streamlit_app.py
```

## Usage

1. **Enter your prompt** in the sidebar text area
2. **Select models** by checking the boxes under each provider
3. **Click "Run All Selected Models"** to execute
4. **Select models to compare** from the checkboxes in the main area
5. **View side-by-side comparison** of the selected outputs

## Supported Models

### OpenAI
- gpt-4o
- gpt-4o-mini
- gpt-4-turbo
- gpt-3.5-turbo

### Anthropic
- claude-opus-4-5-20251101
- claude-sonnet-4-5-20250929
- claude-3-5-sonnet-20241022
- claude-3-5-haiku-20241022

### Google
- gemini-2.0-flash-exp
- gemini-1.5-pro
- gemini-1.5-flash

## Tips

- You can compare up to all selected models at once
- Responses are cached in session state, so you can re-compare different selections without re-running
- Each run clears previous results
