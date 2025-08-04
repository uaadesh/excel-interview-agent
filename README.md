````markdown
# Excellytix AI: The AI-Powered Excel Mock Interviewer

An intelligent, conversational agent designed to automate the initial screening process for roles requiring advanced Microsoft Excel proficiency. This project serves as a Proof-of-Concept for an AI-driven solution to reduce hiring bottlenecks and ensure consistent, high-quality candidate evaluation.

**Live Demo Link:** [To be added after deployment]

---

## 📝 Overview

In today's data-driven landscape, proficiency in Excel is a critical skill for roles in Finance, Operations, and Analytics. However, manually screening candidates for these skills is time-consuming and often inconsistent. Excellytix AI was built to solve this problem.

This application simulates a real mock interview where a candidate is asked a series of questions with varying difficulty. An AI agent evaluates their answers, provides intelligent feedback and hints, and generates a comprehensive performance summary at the end, streamlining the technical screening process.

## ✨ Key Features

* **🤖 Conversational AI Agent:** A stateful agent that manages a multi-turn interview flow.
* **🧠 Intelligent Evaluation:** Utilizes a powerful Large Language Model (LLM) to intelligently assess user answers, understanding the function beyond exact string matches.
* **💡 Adaptive Hint System:** Provides a gentle hint on the first incorrect attempt, allowing candidates a second chance.
* **📊 Dynamic Question Bank:** Serves a random mix of easy, medium, and hard questions for a unique interview experience every time.
* **📄 Automated Performance Summary:** Generates a qualitative performance report at the conclusion of the interview, highlighting strengths and areas for improvement.

## 🛠️ Technology Stack

* **Frontend:** [Streamlit](https://streamlit.io/) - For building the interactive chat interface rapidly in Python.
* **Core Logic:** Python 3.10+
* **LLM Provider:** [Hugging Face Inference API](https://huggingface.co/inference-api) - To access powerful open-source language models.
* **Key Libraries:**
    * `requests` - For making API calls to the LLM.
    * `python-dotenv` - For managing environment variables securely.

## 🚀 Setup and Installation

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

* Python 3.10 or higher
* Git
* A Hugging Face account and an API Token (with "read" permissions).

### 2. Clone the Repository

```bash
git clone https://github.com/uaadesh/excel-interview-agent.git
cd excellytix-ai
````

### 3\. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

  * **Create the environment:**
    ```bash
    python -m venv venv
    ```
  * **Activate the environment:**
      * On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
      * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

### 4\. Install Dependencies

Install all the required libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5\. Configure Environment Variables

Create a file named `.env` in the root of the project directory. This file will hold your secret API key.

1.  Create the file (if it doesn't exist).
2.  Open the `.env` file and add your Hugging Face token:
    ```
    HF_TOKEN="hf_YourSecretTokenHere"
    ```

## ▶️ How to Run the Application

Once the setup is complete, you can run the Streamlit application with a single command:

```bash
streamlit run app.py
```

This will open a new tab in your web browser with the application running locally.

## 📂 Project Structure

```
/excellytix-ai
├── .env                 # Stores secret API keys (not committed to Git)
├── .gitignore           # Specifies files for Git to ignore
├── README.md            # This file
├── agent.py             # Contains the core ExcelInterviewerAgent class (the "brain")
├── app.py               # The main Streamlit application file (the UI)
├── llm_service.py       # Handles all communication with the Hugging Face API
├── prompts.py           # Contains all prompt engineering templates for the LLM
├── question_bank.json   # The database of interview questions
└── requirements.txt     # List of Python dependencies
```

```
```