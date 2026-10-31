"""
AI service functions adapted from the existing aiManager.py and geminiService.py.
Provides Gemini API integration for Django views.
"""

import os
import re
from datetime import datetime
from django.conf import settings
from google import genai

from study.models import Quiz
from cryptoManager import canonicalize_quiz, sign_data
from database import fetch_one


# ─── Gemini client ───────────────────────────────────────────────────
_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = settings.GEMINI_API_KEY
        _client = genai.Client(api_key=api_key)
    return _client


def generate_response(prompt):
    """Send a prompt to Gemini and return the text response."""
    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return (
            f"Unable to connect to Gemini: {e}. "
            "Please check your internet connection or try again later."
        )


# ─── Text helpers ────────────────────────────────────────────────────

def clean_response(text):
    """Strip Markdown bold / bullet markers (matches existing clean_response)."""
    text = text.replace("**", "")
    text = text.replace("* ", "• ")
    return text


# ─── Prompt builders (reused verbatim from aiManager.py) ─────────────

QUIZ_SIZE = 5


def doubt_prompt(question):
    return f"""
    You are an expert AI tutor.

    Rules:
    - Respond in plain text only.
    - Never use Markdown.
    - Never use LaTeX.
    - Do not use **bold**, *, _, #, or backticks.
    - Do not use Markdown bullet lists.
    - For lists, use numbers like:
    1.
    2.
    3.
    - Write mathematical formulas using plain ASCII.
    - Explain concepts step by step.
    - Use simple English.
    - Keep the answer concise.
    - End with a short summary.

    Student Question:
    {question}
    """


def quiz_prompt(topic):
    return f"""
You are an expert AI tutor.

Task:
1. Identify the actual study topic from the user's input.
2. Generate a quiz based only on the extracted study topic.

Rules:
- Respond in plain text only.
- Never use Markdown.
- Never use LaTeX.
- Do not use bold, italics, or special formatting.
- Use simple English.
- Generate exactly 5 multiple-choice questions.
- Each question must have exactly four options labeled A, B, C, and D.
- Only one option should be correct.
- Do NOT reveal the correct answer after each question.
- Start every question with "Question X:" where X is the question number.
- Leave one blank line between consecutive questions.

Topic Extraction Rules:
- The user's input may contain extra words or instructions.
- Extract only the intended study topic.
- Ignore phrases such as:
    - "generate quiz on"
    - "quiz on"
    - "give me a quiz on"
    - "make a quiz on"
    - "advanced quiz on"
    - "please generate a quiz on"
    - or any similar wording.
- If the user enters only a valid study topic, use it directly.
- Return the extracted topic exactly in the following format:

TOPIC: <Extracted Topic>

Examples:
Input: generate quiz on recursion
Output: TOPIC: Recursion

Input: quiz on bayes theorem
Output: TOPIC: Bayes Theorem

Input: matrix multiplication
Output: TOPIC: Matrix Multiplication

Input: advanced quiz on binary trees
Output: TOPIC: Binary Trees

Quiz Format:

Question 1:
...

A.
B.
C.
D.

Question 2:
...

Question 3:
...

Question 4:
...

Question 5:
...

After all questions, print exactly:

ANSWER KEY

followed by:

1. B
2. D
3. A
4. C
5. B

Then print exactly:

ANSWER LIST

B D A C B

Important:
- If the user's input is not a meaningful academic or study topic, do NOT generate a quiz.
- Instead, politely explain that the input is not suitable for quiz generation and ask the user to enter a valid study topic.
- Do not invent questions for unrelated or nonsensical inputs.
- Do not include any text before "TOPIC:" or after "ANSWER LIST".

User Input:
{topic}
"""


def note_summary_prompt(note):
    return f'''You are an expert AI tutor.

Task:
Summarize the student's study note.

Rules:
- Plain text only.
- No Markdown.
- No LaTeX.
- Keep important concepts.
- Keep formulas in ASCII.
- Use simple English.
- Use bullet points when appropriate.
- Keep the summary concise.
- Do not add information that is not present in the note.

Study Note:

{note}'''


def study_plan_prompt(goal, duration, study_hours):
    return f"""
You are an expert study mentor.

Create a personalized study plan.

Student Goal:
{goal}

Duration:
{duration} weeks

Daily Study Time:
{study_hours} hours

Rules:

- Respond in plain text only.
- Never use Markdown.
- Never use LaTeX.
- Use simple English.
- Organize the study plan week by week.
- Mention important milestones.
- Suggest revision time.
- Suggest practice sessions.
- Suggest mock tests where appropriate.
- Keep the schedule realistic.
- End with motivational advice.
"""


# ─── High-level feature functions ────────────────────────────────────

def resolve_doubt(question):
    """Return an AI-generated answer to a student question."""
    prompt = doubt_prompt(question)
    return clean_response(generate_response(prompt))


def generate_quiz(topic_input):
    """
    Generate a quiz from Gemini and parse it.

    Returns a dict with keys:
        extracted_topic, quiz_text, answer_list, error
    """
    prompt = quiz_prompt(topic_input)
    raw = generate_response(prompt)
    cleaned = clean_response(raw)

    result = {
        "extracted_topic": None,
        "quiz_text": None,
        "questions": [],
        "answer_list": [],
        "error": None,
    }

    # Parse TOPIC:
    topic_parts = cleaned.split("TOPIC:")
    if len(topic_parts) != 2:
        result["error"] = "Unable to parse topic from AI response."
        return result

    remaining = topic_parts[1].strip()

    try:
        extracted_topic, remaining = remaining.split("Question 1:", 1)
    except ValueError:
        result["error"] = "Unable to parse quiz from AI response."
        return result

    result["extracted_topic"] = extracted_topic.strip()

    quiz_response = "Question 1:" + remaining
    quiz_parts = quiz_response.split("ANSWER KEY")
    if len(quiz_parts) != 2:
        result["error"] = "Unable to parse quiz from AI response."
        return result

    result["quiz_text"] = quiz_parts[0].strip()

    # Parse individual questions
    questions = []
    q_blocks = re.split(r'Question\s+\d+:', result["quiz_text"])
    for block in q_blocks[1:]:  # skip first empty element
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if lines:
            q_text = lines[0]
            options = []
            for line in lines[1:]:
                if re.match(r'^[A-D][\.\)]', line):
                    options.append(line)
            questions.append({"question": q_text, "options": options})
    result["questions"] = questions

    answer_parts = quiz_parts[1].strip().split("ANSWER LIST")
    if len(answer_parts) != 2:
        result["error"] = "Unable to parse answer list."
        return result

    result["answer_list"] = answer_parts[1].strip().split()
    return result


def save_quiz_result(topic_id, score, accuracy):
    """Save quiz result with ECDSA signature (reuses storageManager.save_quiz)."""
    from storageManager import save_quiz
    completed_at = datetime.now()

    # Get the next auto_increment ID
    row = fetch_one(
        "SELECT AUTO_INCREMENT FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'quizzes'"
    )
    next_id = row["AUTO_INCREMENT"]

    canonical_bytes = canonicalize_quiz(
        quiz_id=next_id,
        topic_id=topic_id,
        score=score,
        total_questions=QUIZ_SIZE,
        accuracy=accuracy,
        time_taken_seconds=None,
        completed_at=completed_at,
    )
    signature = sign_data(canonical_bytes)

    save_quiz(
        topic_id=topic_id,
        score=score,
        total_questions=QUIZ_SIZE,
        accuracy=accuracy,
        time_taken_seconds=None,
        completed_at=completed_at,
        signature=signature,
    )


def summarize_note(note_content):
    """Return a summary of a note via Gemini."""
    prompt = note_summary_prompt(note_content)
    return clean_response(generate_response(prompt))


def generate_study_plan(goal, duration, study_hours):
    """Return a study plan via Gemini."""
    prompt = study_plan_prompt(goal, duration, study_hours)
    return clean_response(generate_response(prompt))
