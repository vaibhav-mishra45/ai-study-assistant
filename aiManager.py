from rich.align import Align
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from geminiService import generate_response
from rich import print

console = Console()

def choose_option(n):
    while True:
        try:
            option = int(input(f"Enter your choice (0-{n}): "))
            if option in range(n + 1):
                return option
            else:
                print(f"[red]Invalid choice. Please enter a number between 0 and {n}.[/red]")
        except ValueError:
            print(f"[red]Invalid input. Please enter a number between 0 and {n}.[/red]")

def ai_features():
    print((Panel(Align.center("AI Features"), subtitle="Welcome to AI Mode", style="bold green")))
    table = Table(title="AI Features Menu")
    table.add_column("Option", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_row("1", "Doubt Resolution")
    table.add_row("2", "Quiz Generation")
    table.add_row("3", "Note Summarization")
    table.add_row("4", "Study Plan")
    table.add_row("0", "Back")

    table = Align.center(table)
    console.print(table)

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
            cleaned_response = generate_response(prompt)
            print((Panel(cleaned_response, title="AI Tutor", style="bold green")))
            while input("Press Enter to continue...") != "":
                print("[red]Please press only Enter.[/red]")

        elif sub_option == 2:
            generate_response("Quiz Generation")
        elif sub_option == 3:
            generate_response("Note Summarization")
        elif sub_option == 4:
            generate_response("Study Plan")
