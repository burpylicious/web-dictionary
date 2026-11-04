import shutil

from fetch_dictionary_api import (fetch_word,InvalidWordError,WordNotFoundError,DictionaryUnavailableError,)
from dictionary_models import WordEntry


def show_entry(entry):
    """Display dictionary panel."""
     # Show word's header label and phonetic
    print("\n" + entry.word, entry.phonetic)
    width = shutil.get_terminal_size(min(width, 60)).columns
     # Print line to stretch to fit user's window
    print("-" * width)

    for meaning in entry.meanings:
         # Display word's part of speech
        print(meaning.part_of_speech)
        for number, definition in enumerate(meaning.definitions, start=1): 
            # Print word's defintion
            print(f"  {number}. {definition.text}")
            # If word has example(s), print example(s)
            if definition.example:
                print(f'     "{definition.example}"')
            # If word has synonym(s), print synonym(s)
            if definition.synonyms:
                # Display synonyms (which is a list) joined with commas
                print("    Synonym(s):", ", ".join(definition.synonyms))
        print()


def main():
    """Prompt for user input and allow them to quit by pressing Enter."""
    print("Type a word, or press Enter to quit.")

    while True:
        word = input("\nWord: ")
        # If input is empty, exit program
        if not word.strip():
            print("Quitting...")
            break

        try:
            data = fetch_word(word)
            entry = WordEntry(data[0])
            # Display full dictionary interface 
            show_entry(entry)
        # Catch errors using custom error classes
        except InvalidWordError as err:
            print("❌", err)
        except WordNotFoundError:
            print(f"❌ Word: '{word}' not found! Try a different word")
        except DictionaryUnavailableError as err:
            print("❌ Dictionary unavailable:", err)


if __name__ == "__main__":
    main()