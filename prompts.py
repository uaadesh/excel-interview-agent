# prompts.py
"""
This module centralizes all prompt engineering for the application.
It contains functions that generate structured prompts for the LLM
to perform specific tasks like evaluation, summarization, and greeting.
"""

def get_welcome_prompt(total_questions: int) -> str:
    """
    Generates the initial welcome message for the user.

    Args:
        total_questions (int): The total number of questions in the interview playlist.

    Returns:
        str: A formatted welcome message.
    """
    return (f"Welcome to the Excellytix AI Mock Interview! The interview will consist of "
            f"{total_questions} questions. Please press 'Start Interview' when you are ready.")


def get_evaluation_prompt(question: str, user_answer: str, correct_answer: str) -> list:
    """
    Creates a robust prompt instructing the LLM to intelligently decide between
    praising a correct answer or providing a hint for an incorrect one.

    Args:
        question (str): The question asked to the user.
        user_answer (str): The user's submitted answer.
        correct_answer (str): The reference correct answer for the LLM.

    Returns:
        list: A list of message dictionaries formatted for the Chat Completions API.
    """
    system_message = {
        "role": "system",
        "content": """You are an expert Excel interviewer named Excellytix AI. Your persona is helpful and encouraging. Your primary goal is to evaluate a candidate's answer and provide one of two responses based on its correctness.

1.  **Analyze the user's answer.** Intelligently determine if it is functionally correct. It does not need to be an exact match.
2.  **If the answer is correct:** Your JSON response MUST be `{"is_correct": true, "explanation": "<Your words of praise and positive feedback on why their answer is a good one.>"}`.
3.  **If the answer is incorrect:** Your JSON response MUST be `{"is_correct": false, "explanation": "<A gentle, encouraging hint to guide the user toward the solution. DO NOT reveal the full answer in the hint.>"}`.
4.  **You must follow the thinking and formatting rules:**
    - First, reason step-by-step inside a `<think>` block.
    - After the `<think>` block, respond with ONLY the valid JSON object.
    - Do not wrap the JSON object in Markdown code blocks like ```json."""
    }

    user_message = {
        "role": "user",
        "content": f"""Please evaluate the following candidate response. Remember to respond with praise if correct, or a hint if incorrect.

- The interview question was: "{question}"
- For your reference, a correct answer is: "{correct_answer}"
- The candidate's submitted answer is: "{user_answer}"

Begin your thinking process now."""
    }
    
    return [system_message, user_message]

def get_summary_prompt(history: list) -> list:
    """
    Creates a prompt to summarize the entire interview transcript.

    Args:
        history (list): The list of all chat messages from the interview.

    Returns:
        list: A list of message dictionaries formatted for the Chat Completions API.
    """
    transcript = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    
    return [{
        "role": "system",
        "content": "You are a senior hiring manager. Your task is to write a concise performance summary based on an interview transcript. Identify key strengths and areas for development. Address the candidate directly in your summary. Be encouraging but professional."
    }, {
        "role": "user",
        "content": f"Please generate a performance summary based on the following transcript:\n\n{transcript}"
    }]

def get_conclusion_prompt() -> str:
    """
    Generates the concluding message before the summary report.

    Returns:
        str: A short conclusion message.
    """
    return "That was the last question! Thank you for completing the interview. Generating your performance summary now..."