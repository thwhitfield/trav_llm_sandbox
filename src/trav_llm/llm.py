
from openai import OpenAI
from anthropic import Anthropic
from google import genai

def get_model_response(client, model_name, prompt):
    """
    Generate a text response from OpenAI, Anthropic, or Google AI models.
    
    Args:
        client: The AI client (OpenAI, Anthropic, or genai.Client)
        model_name: The model identifier (e.g., 'gpt-4', 'claude-3-5-sonnet-20241022', 'gemini-2.0-flash-exp')
        prompt: The user prompt string
    
    Returns:
        str: The generated text response
    """
    if isinstance(client, OpenAI):
        response = client.responses.create(
            model=model_name,
            input=prompt
        )
        return response.output_text
    
    elif isinstance(client, Anthropic):
        response = client.messages.create(
            model=model_name,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    elif hasattr(client, 'models'):  # Google genai.Client
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text
    
    else:
        raise ValueError(f"Unsupported client type: {type(client)}")