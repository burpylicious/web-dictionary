import shutil
import textwrap

from fetch_dictionary_api import (fetch_word,InvalidWordError,WordNotFoundError,DictionaryUnavailableError,)
from dictionary_models import WordEntry

# Maximum number of definitions to show per section
MAX_DEFINITIONS = 3 

def show_entry(entry):
    """Display dictionary panel."""
     # Show word's header label and phonetic
    print("\n" + entry.word, entry.phonetic)

    # Print line to stretch to fit user's window
    width = min(shutil.get_terminal_size((80, 20)).columns, 80)
    print("-" * width)

    for meaning in entry.meanings:
         # Display word's part of speech
        print(meaning.part_of_speech)

        shown_definitions = meaning.definitions[:MAX_DEFINITIONS]
        # Label definitions starting from 1
        for number, definition in enumerate(shown_definitions, start=1):
            first_start = f"  {number}. "
            other_start = " " * len(first_start)

            # Print label first if word has a label
            if definition.label:
                print(first_start + f"[{definition.label}]")
                # Display definition below label
                first_start = other_start

            # Wrap definiton such that extra lines align with first line
            print(textwrap.fill(definition.text, width=width,
                                initial_indent=first_start,
                                subsequent_indent=other_start))


            # Wrap word example(s) such that extra lines align with first line
            if definition.example:
                print(textwrap.fill(f'"{definition.example}"', width=width,
                                    initial_indent=other_start,
                                    subsequent_indent=other_start))


            # If word has synonym(s), print synonym(s)
            if definition.synonyms:
                # Display synonyms (which is a list) joined with commas
                print(other_start + "Synonym(s): " + ", ".join(definition.synonyms))
    
        # Display number of hidden extra definitions
        hidden = len(meaning.definitions) - len(shown_definitions)
        # Display "more" subtext if there are hidden extra definitions
        if hidden > 0:
            print(f"     + {hidden} more")
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