# llm_service.py
"""
This module handles all communication with the external Large Language Model API.
It is responsible for sending requests, handling authentication, and robustly
parsing the model's response.
"""
import os
import requests
from dotenv import load_dotenv

# Best Practice: Load sensitive credentials from a .env file.
load_dotenv()

# --- API Configuration ---
# Using the standardized Chat Completions API endpoint for broad compatibility.
API_URL = "[https://api-inference.huggingface.co/v1/chat/completions](https://api-inference.huggingface.co/v1/chat/completions)"
# The specific model to be used for the interview evaluation.
MODEL_ID = "zai-org/GLM-4.5:novita"
# Securely retrieve the API token from environment variables.
HF_TOKEN = os.getenv("HF_TOKEN")

# Fail-fast: If the token is not configured, the application will stop immediately.
if not HF_TOKEN:
    raise ValueError("Hugging Face API token not found. Please create a .env file and set the HF_TOKEN variable.")

# Standard headers required for authenticated requests to the Hugging Face API.
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def _parse_response(full_response: str) -> str:
    """
    Robustly extracts a JSON object from the LLM's raw output.
    This handles cases where the model includes a <think> block for reasoning
    or wraps the JSON in markdown code fences.

    Args:
        full_response (str): The complete raw text returned by the LLM.

    Returns:
        str: A clean string that is expected to be a JSON object.
    """
    # Print the full response for debugging purposes in the terminal.
    print(f"--- Full LLM Raw Response ---\n{full_response}\n--------------------")

    # First, isolate the part of the response after any <think> block.
    if "</think>" in full_response:
        clean_part = full_response.split("</think>", 1)[-1].strip()
    else:
        clean_part = full_response.strip()

    # Second, surgically extract the JSON object by finding the first '{' and last '}'.
    # This is highly resilient to extra text or markdown formatting around the JSON.
    start_index = clean_part.find('{')
    end_index = clean_part.rfind('}')

    if start_index != -1 and end_index != -1 and end_index > start_index:
        json_string = clean_part[start_index : end_index + 1]
        return json_string
    else:
        # If no JSON object is found, return the cleaned part for error handling.
        print(f"--- Warning: Could not find a valid JSON object in the response part: {clean_part} ---")
        return clean_part

def call_llm(messages: list) -> str:
    """
    Sends a list of messages to the LLM API and returns the parsed response.

    Args:
        messages (list): A list of message dictionaries to send to the model.

    Returns:
        str: The parsed JSON string from the LLM's response.
    """
    print("--- Calling LLM ---")

    payload = {
        "model": MODEL_ID,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.1, # Lower temperature for more predictable, factual JSON output.
    }

    try:
        # Make the API request with a timeout for resilience.
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        # Raise an exception for bad status codes (like 401, 404, 500).
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and result["choices"]:
            full_response_content = result["choices"][0]["message"]["content"]
            # Use the robust parsing function to get the clean JSON.
            json_string = _parse_response(full_response_content)
            print(f"--- Parsed LLM JSON: {json_string} ---")
            return json_string
        else:
            print(f"--- Unexpected LLM Response Format: {result} ---")
            # Return a default error JSON if the format is wrong.
            return '{"is_correct": false, "explanation": "Sorry, I received an unexpected response from the AI."}'

    except requests.exceptions.RequestException as e:
        # Handle network errors, timeouts, etc.
        print(f"--- API Request Failed: {e} ---")
        return '{"is_correct": false, "explanation": "Sorry, I was unable to connect to the evaluation service."}'