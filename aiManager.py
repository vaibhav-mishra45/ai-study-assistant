from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from geminiService import generate_response
from rich import print
from utils import generate_menu, choose_option, load_data, write_data
from datetime import datetime

console = Console()
QUIZ_SIZE = 5
QUIZ_FILE = 'data/quiz_history.json'

def ai_features():
    panel_title="AI Features"
    panel_subtitle="Welcome to AI Mode"
    table_title="AI Features Menu"
    rows=["Doubt Resolution", "Quiz Generation", "Note Summarization", "Study Plan"]
    back_text="Back"
    generate_menu(panel_title, panel_subtitle, table_title, rows, back_text)

def clean_response(text):
    text = text.replace("**", "")
    text = text.replace("* ", "• ")
    return text

def get_question():
    question = input("Enter your question: ").strip()
    if question == "" or len(question) < 5:
        print("[red]Please enter a valid question.[/red]")
        return None
    return question

def generate_prompt(question):
    
    prompt = f"""
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
    return prompt

def quiz_prompt(topic):
    prompt = f"""
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
    return prompt

def quiz_ans():
    ans_list_user = []
    for i in range (QUIZ_SIZE):
        while True:
            answer = input(f"Enter answer for Question {i+1} (A/B/C/D): ").strip().upper()

            if answer in ["A", "B", "C", "D"]:
                break

            print("[red]Please enter A, B, C or D.[/red]")
        ans_list_user.append(answer)
    return ans_list_user
'''
def find_topic(data, name):
    for subject in data.get('subjects', []):
        if subject.get('name').lower() == name.lower():
            return subject
    return None 
'''   

def quiz_data(topic, score, accuracy):
    data = load_data(QUIZ_FILE)
    quiz_detail = {"topic":topic, "score":score, "total_question":QUIZ_SIZE, "accuracy": accuracy,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "time_taken": "null"}
    data['quizzes'].append(quiz_detail)
    write_data(QUIZ_FILE, data)



def answer_review(ans_list, answer_list_user):
    table = Table(title="Quiz Review")
    table.add_column("Question", justify="center", style="cyan", no_wrap=True)
    table.add_column("Your Answer", justify="center", style="cyan", no_wrap=True)
    table.add_column("Correct Answer", justify="center", style="cyan", no_wrap=True)
    table.add_column("Result", justify="center", style="cyan", no_wrap=True)
    for i in range(QUIZ_SIZE):
        if ans_list[i] == answer_list_user[i]:
            status = "✓"
        else:
            status = "✗"
        table.add_row(str(i+1), answer_list_user[i], ans_list[i], status)
    console.print(table)

def choose_ai_feature():
    while True:
        ai_features()
        sub_option = choose_option(4)
        if sub_option == 0:
            break
        elif sub_option == 1:
            question = get_question()
            if not question:
                print("[red]No valid question provided.[/red]")
                continue
            prompt = generate_prompt(question)
            cleaned_response = clean_response(generate_response(prompt))
            print((Panel(cleaned_response, title="AI Tutor", style="bold green")))
            while input("Press Enter to continue...") != "":
                print("[red]Please press only Enter.[/red]")

        elif sub_option == 2:

            user_input = input("Enter Study Topic: ").strip()

            if not user_input:
                print("[red]No valid topic provided.[/red]")
                continue

            prompt = quiz_prompt(user_input)

            raw_response = generate_response(prompt)
            cleaned_response = clean_response(raw_response)

            topic_parts = cleaned_response.split("TOPIC:")
            if len(topic_parts) != 2:
                print("[red]Unable to parse topic generated by Gemini.[/red]")
                continue

            remaining_response = topic_parts[1].strip()

            extracted_topic, remaining_response = remaining_response.split("Question 1:", 1)
            extracted_topic = extracted_topic.strip()

            quiz_response = "Question 1:" + remaining_response

            quiz_parts = quiz_response.split("ANSWER KEY")
            if len(quiz_parts) != 2:
                print("[red]Unable to parse quiz generated by Gemini.[/red]")
                continue

            quiz_text = quiz_parts[0].strip()

            answer_parts = quiz_parts[1].strip().split("ANSWER LIST")
            if len(answer_parts) != 2:
                print("[red]Unable to parse answer list.[/red]")
                continue

            answer_key = answer_parts[0].strip()
            answer_list = answer_parts[1].strip().split()

            print(Panel(quiz_text, title="AI Tutor", style="bold green"))

            user_answers = quiz_ans()

            score = sum(user == correct for user, correct in zip(user_answers, answer_list))
            accuracy = score / QUIZ_SIZE * 100

            quiz_summary = f"""QUIZ COMPLETED

Topic     : {extracted_topic}
Score     : {score} / {QUIZ_SIZE}
Accuracy  : {accuracy:.0f}%
        """

            print(Panel(quiz_summary, title="AI Tutor", style="bold green"))

            answer_review(answer_list, user_answers)

            quiz_data(extracted_topic, score, accuracy)

            while input("Press Enter to continue...") != "":
                print("[red]Please press only Enter.[/red]")
        elif sub_option == 3:
            generate_response("Note Summarization")
        elif sub_option == 4:
            generate_response("Study Plan")
