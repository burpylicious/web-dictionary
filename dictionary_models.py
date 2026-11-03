from fetch_dictionary_api import fetch_word

class Definition:
    """One definition of the inputted word and its optional example and synonyms."""

    def __init__(self, data):
        # Pull all the neede fields out of the definition dictionary
        self.text = data["definition"]
        self.example = data.get("example") # return none if no example can be retrieved from word
        self.synonyms = data.get("synonyms", []) # return an empty list if no synonyms can be retrieved from word


if __name__ == "__main__":
    # Test fetching inputted word from Dictionary API
    data = fetch_word("serendipity")

    # Manually chain index the inputted word to get its first definition
    first_def_dict = data[0]["meanings"][0]["definitions"][0]

    word_definition = Definition(first_def_dict)

    # Explore data type of definition, and print the inputted word's definition, and example in a sentence and its synonyms (if there is any)
    print(type(word_definition))
    print("text:", word_definition.text)
    print("example:", word_definition.example)
    print("synonyms:", word_definition.synonyms)

    # Test using a fake dictionary, with examples and synonyms
    fake_word_definition = {
        "definition": "To move quickly on foot.",
        "example": "She runs every morning.",
        "synonyms": ["jog", "sprint"],
    }
    word_definition_2 = Definition(fake_word_definition)
    print("text:", word_definition_2.text)
    print("example:", word_definition_2.example)
    print("synonyms:", word_definition_2.synonyms)