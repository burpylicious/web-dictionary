import requests

BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"


def fetch_word(word):
    """Return the API's JSON (a list) for `word`, or None if not found."""
    word = word.strip().lower()

    url = f"{BASE_URL}{word}"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        print("Couldn't establish connection to Dictionary API, check your network.")
        return None

    if response.status_code != 200:
        return None

    return response.json()


if __name__ == "__main__":
    data = fetch_word("  Serendipity ")

    entry = data[0]
    print("entry keys ->", list(entry.keys()))

    meanings = entry["meanings"]
    print("meanings has", len(meanings), "item(s)")

    first_meaning = meanings[0]
    print("first_meaning keys ->", list(first_meaning.keys()))

    definitions = first_meaning["definitions"]
    first_def = definitions[0]
    print("first_def keys ->", list(first_def.keys()))

    print("DEFINITION:", first_def["definition"])

    print("Not found test:", fetch_word("asdfghjk"))