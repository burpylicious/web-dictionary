from fetch_dictionary_api import fetch_word

class Definition:
    """One definition of the inputted word and its optional example and synonyms."""

    def __init__(self, data):
        # Retrieve one definition dictionary from the Dictionary API
        self.text = data["definition"]
        self.example = data.get("example") # return none if no example can be retrieved from word
        self.synonyms = data.get("synonyms", []) # return an empty list if no synonms can be retreived from word


if __name__ == "__main__":
    # Test fetching inputted word from Dictionary API
    data = fetch_word("serendipity")

    # Manually chain index the inputted word to get its first definition
    first_def_dict = data[0]["meanings"][0]["definitions"][0]

    d = Definition(first_def_dict)

    # Explore data type of definition, and print the inputted word's definition, and example in a sentence and its synonyms (if there is any)
    print(type(d))
    print("text:", d.text)
    print("example:", d.example)
    print("synonyms:", d.synonyms)

    # Test using a fake dictionary, with examples and synonyms
    fake = {
        "definition": "To move quickly on foot.",
        "example": "She runs every morning.",
        "synonyms": ["jog", "sprint"],
    }
    d2 = Definition(fake)
    print("text:", d2.text)
    print("example:", d2.example)
    print("synonyms:", d2.synonyms)