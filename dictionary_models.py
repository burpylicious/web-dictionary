from fetch_dictionary_api import fetch_word

class Definition:
    """One definition of the inputted word and its optional example and synonyms."""

    def __init__(self, data):
        # Pull all the needed fields out of the definition dictionary
        self.text = data["definition"]
        self.example = data.get("example") # return none if no example can be retrieved from word
        self.synonyms = data.get("synonyms", []) # return an empty list if no synonyms can be retrieved from word


class Meaning: 
    """One part of speech of a word and all its definitions."""

    def __init__(self, data):
        self.part_of_speech = data.get("partOfSpeech")

        self.definitions = []
        # Loop over raw dictionary from API response
        for definition_dict in data["definitions"]: 
            self.definitions.append(Definition(definition_dict))


if __name__ == "__main__":
    # Fetch inputted word's raw dictionary data
    data = fetch_word("serendipity")

    # Instantiate a Meaning object
    meaning = Meaning(data[0]["meanings"][0])
    print(meaning.part_of_speech)

    # Loop through each Definition object stored inside the Meaning object
    for definition in meaning.definitions:
        print("  -", definition.text)
        # Display example of inputted word if it has an example, else state none
        if definition.example:
            print("    Example(s):", definition.example)
        else:
            print("    Example(s): none")

        # Display synonyms of inputted word if it has a synonym, else state none
        if definition.synonyms:
            print("    Synonym(s):", ", ".join(definition.synonyms))
        else:
            print("    Example(s): none")