# agent.py
"""
This module contains the core logic for the interview agent.
The ExcelInterviewerAgent class acts as a state machine, managing the flow
of the interview, tracking user progress, and interacting with the LLM service.
"""
import json
import random
from llm_service import call_llm
from prompts import get_evaluation_prompt, get_welcome_prompt, get_conclusion_prompt, get_summary_prompt

class ExcelInterviewerAgent:
    """
    A stateful agent that conducts a mock Excel interview.
    
    Attributes:
        state (str): The current state of the interview (e.g., INTRODUCTION, EVALUATING).
        history (list): A running log of the conversation.
        interview_playlist (list): The specific list of questions for this session.
        current_question_index (int): The index of the current question in the playlist.
        attempts_for_current_question (int): The number of attempts the user has made on the current question.
    """
    def __init__(self, interview_config: dict = {'easy': 2, 'medium': 2, 'hard': 1}):
        """
        Initializes the agent with a specific interview configuration.
        
        Args:
            interview_config (dict): Specifies how many questions of each
                                     difficulty to ask.
        """
        self.state = "INTRODUCTION"
        self.history = []
        self.all_questions = self._load_questions("question_bank.json")
        self.interview_playlist = self._prepare_interview_playlist(interview_config)
        self.current_question_index = 0
        self.attempts_for_current_question = 0

    def _load_questions(self, filepath: str) -> dict:
        """Loads the categorized question bank from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Provides a graceful fallback if the question bank is missing.
            print(f"Error: The file {filepath} was not found.")
            return {"easy": [], "medium": [], "hard": []}

    def _prepare_interview_playlist(self, config: dict) -> list:
        """Creates a random, non-repeating list of questions for the session."""
        playlist = []
        for difficulty, count in config.items():
            if difficulty in self.all_questions:
                available_questions = self.all_questions[difficulty]
                num_to_select = min(count, len(available_questions))
                playlist.extend(random.sample(available_questions, num_to_select))
        
        # Shuffle the final playlist to mix the difficulty levels during the interview.
        random.shuffle(playlist)
        print(f"--- Interview playlist created with {len(playlist)} questions. ---")
        return playlist

    def start_interview(self):
        """Transitions the agent to the asking state and gets the first question."""
        self.state = "ASKING_QUESTION"
        self.get_next_question()

    def get_next_question(self):
        """
        Prepares and appends the next question to the history, or concludes the interview.
        """
        if self.current_question_index >= len(self.interview_playlist):
            self.conclude_interview()
            return

        self.attempts_for_current_question = 0  # Reset attempts for the new question.
        question = self.interview_playlist[self.current_question_index]
        question_text = f"**Question {self.current_question_index + 1} of {len(self.interview_playlist)}:** {question['question_text']}"
        self.history.append({"role": "assistant", "content": question_text})
        self.state = "EVALUATING" # Set state to await user's answer.

    def process_user_response(self, user_input: str) -> dict:
        """
        Processes the user's answer, calls the LLM, and manages the retry/advance logic.

        Args:
            user_input (str): The user's submitted answer.

        Returns:
            dict: A dictionary containing the LLM's feedback and state information for the UI.
        """
        self.history.append({"role": "user", "content": user_input})
        
        if self.state != "EVALUATING":
            return {"role": "assistant", "content": "Let's move to the next question."}

        current_q = self.interview_playlist[self.current_question_index]
        self.attempts_for_current_question += 1
        
        # Call the LLM with the simple prompt. The LLM will either praise or give a hint.
        messages = get_evaluation_prompt(current_q['question_text'], user_input, current_q['correct_formula'])
        llm_response_str = call_llm(messages)
        
        try:
            evaluation = json.loads(llm_response_str)
            feedback = evaluation.get("explanation", "I've noted that.")
            is_correct = evaluation.get("is_correct", False)
        except (json.JSONDecodeError, TypeError):
            feedback = "An error occurred during evaluation. Let's proceed."
            is_correct = False

        self.history.append({"role": "assistant", "content": feedback})
        
        # Handle the interview flow based on the LLM's verdict.
        if is_correct or self.attempts_for_current_question >= 2:
            # Move to the next question if the user is right OR if they've used up their two attempts.
            self.current_question_index += 1
        else:
            # It was the first wrong attempt, and the LLM gave a hint.
            # We do nothing else and wait for the user's second attempt.
            pass
            
        return {"role": "assistant", "content": feedback, "is_correct": is_correct, "attempts": self.attempts_for_current_question}

    def conclude_interview(self):
        """
        Concludes the interview and triggers the generation of the summary report.
        """
        self.state = "CONCLUSION"
        conclusion_message = get_conclusion_prompt()
        self.history.append({"role": "assistant", "content": conclusion_message})
        
        # Generate and append the summary report using the LLM.
        summary_messages = get_summary_prompt(self.history)
        summary_report = call_llm(summary_messages)
        self.history.append({"role": "assistant", "content": f"### Performance Summary\n\n{summary_report}"})