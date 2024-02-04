import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    """
    Loads the knowledge base from a JSON file.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    dict: The loaded knowledge base.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Le fichier knowledge_base.json n'a pas été trouvé.")
        return {}
    except json.JSONDecodeError:
        print("Erreur de formatage dans knowledge_base.json.")
        return {}

def save_knowledge_base(file_path: str, data: dict):
    """
    Saves the knowledge base to a JSON file.

    Args:
    file_path (str): The path to the JSON file.
    data (dict): The knowledge base to save.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """
    Finds the best match for a user's question from a list of questions.

    Args:
    user_question (str): The user's question.
    questions (list[str]): The list of available questions.

    Returns:
    str | None: The best matching question or None if no match is found.
    """
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """
    Retrieves the answer for a given question from the knowledge base.

    Args:
    question (str): The question to find the answer for.
    knowledge_base (dict): The knowledge base.

    Returns:
    str | None: The answer to the question or None if not found.
    """
    for x in knowledge_base["questions"]:
        if x["question"] == question:
            return x["answer"]

def chat_bot():
    """
    Main function to run the chat bot.
    """
    knowledge_base = load_knowledge_base('knowledge_base.json')

    if not knowledge_base:
        return

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            break

        best_match = find_best_match(user_input, [x["question"] for x in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'ChatBot: {answer}')
        else:
            print('ChatBot: I do not know the answer. May you teach me?')
            new_answer = input('Type the answer or type "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('ChatBot: Thank you! Thanks to you I learned something new!')

if __name__ == '__main__':
    chat_bot()