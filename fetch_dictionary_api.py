import requests

BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"


def fetch_word(word):
    """Return API's JSON response using user's inputted word, or None if not found."""
    word = word.strip().lower()

    # Build url for inputted word
    url = f"{BASE_URL}{word}"

    # Make request to Dictionary API and print error message if no data is retreived
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        print("Couldn't establish connection to Dictionary API, check your network.")
        return None

    # If response is not valid (not response 200), then return None
    if response.status_code != 200:
        return None

    # Convert raw text data from Dictionary API into python data structure
    return response.json()


if __name__ == "__main__":
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
    print("Word not found:", fetch_word("asdfghjk"))