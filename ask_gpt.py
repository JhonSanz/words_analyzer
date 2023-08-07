
import argparse
import pyperclip

def difference_between(words):
    message = f"¿Cuál es la diferencia entre {', '.join([word.replace('_', ' ') for word in words])}?"
    print(message)
    pyperclip.copy(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask GPT-3 about the difference between two words.")
    parser.add_argument("palabras", nargs="*", help="Una lista de palabras separadas por coma.")
    args = parser.parse_args()
    difference_between(args.palabras)