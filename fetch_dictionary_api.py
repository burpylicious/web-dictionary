import string
import requests

BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

class DictionaryError(Exception):
    """Base exception for all subsequent dictionary module errors."""


class InvalidWordError(DictionaryError):
    """Raised when the inputted word cannot be looked up (empty, numbers, symbols)."""


class WordNotFoundError(DictionaryError):
    """Error is raised when the word does not exist in Dictionary API data."""


class DictionaryUnavailableError(DictionaryError):
    """Raised when the API is down, offline, or returns invalid data."""


def is_valid_word(word):
    """Return True if the word is valid to be sent to API, after being cleaned"""
    if not word:
        return False 
    letters_from_word = word.replace("-", "").replace("'", "").replace(" ", "")
    return letters_from_word.isalpha()


def fetch_word(word):
    """Return API's JSON response using user's inputted word."""
    # Strip word of spaces and punctuation, then convert it to lowercase
    word = word.strip(string.whitespace + string.punctuation).lower()

    # Stop early if the input can't be a real word
    if not is_valid_word(word):
        raise InvalidWordError(f"'{word}' is not a valid word.")

    # Build url for inputted word
    url = f"{BASE_URL}{word}"

    # Make request to Dictionary API and raise DictionaryUnavailableError if connection could not be established
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        raise DictionaryUnavailableError("Couldn't establish connection to Dictionary API, check your network.")

    # Raise WordNotFoundError if word is not found
    if response.status_code == 404: 
        raise WordNotFoundError(f"{url} is invalid, no defintions for \"{word}\" could be found")
    # Raise DictionaryUnavailableError if response is not valid (not 200)
    if response.status_code != 200:
        raise DictionaryUnavailableError(f"Dictionary returned status {response.status_code}.")

    # Convert raw text data from Dictionary API into python data structure
    return response.json()


if __name__ == "__main__":
    # Inputted word
    data = fetch_word("  Serendipity ")

    entry = data[0]
    print("entry keys ->", list(entry.keys()))

    # A meaning is the interpretation of the word and/or concept it can convey
    meanings = entry["meanings"]
    print("meanings has", len(meanings), "item(s)")

    first_meaning = meanings[0]
    print("first_meaning keys ->", list(first_meaning.keys()))

    # A definition is a rigid, structured, and standardised explanation of the word's literal meaning
    definitions = first_meaning["definitions"]
    first_def = definitions[0]

    # Print keys of the first definition
    print("first_def keys: ", list(first_def.keys()))

    # Print the actual definition of the word
    print("DEFINITION:", first_def["definition"])

    # Test if word is not found in Dictionary API data
    try:
        fetch_word("asdfghjk")
    except DictionaryError as err:
        print("Not found test:", type(err).__name__, "-", err)

    # Test is_valid_word on words expected to be valid/cleaned
    for w in ["serendipity", "well-being", "don't", "ice cream", "", "123", "hell!o"]:
        print(f"is_valid_word({w!r}): ", is_valid_word(w))

    for w in ["hello!", '"serendipity."', "Hell!o", "   ", "123"]:
        try:
            result = fetch_word(w)
            print(f"fetch_word({w!r}): {result[0]['word']} is a valid word")
        except DictionaryError as err:
            print(f"fetch_word({w!r}): ", type(err).__name__, "-", err)