from fetch_dictionary_api import fetch_word

def split_spaces(text):
    """Squash runs of spaces into single spaces."""
    return " ".join(text.split())


def split_labels(text):
    """Split text and returns (label, rest). label is "" when the text has no brackets or parentheses."""

    if not text.startswith("("):
        return "", text
    close = text.find(")")
    if close == -1:
        return "", text
    label = text[1:close]
    rest = text[close+1:].strip()
    return label, rest

class Definition:
    """One definition of the inputted word and its optional example and synonyms."""

    def __init__(self, data):
        """Pull all the needed fields out of the definition dictionary"""
        # Split labels for word definition
        text = split_spaces(data["definition"])
        self.label, self.text = split_labels(text)

        # Split example if word has example
        example = data.get("example")
        if example:
            self.example = split_spaces(example)
        else:
            self.example = None

        self.synonyms = data.get("synonyms", []) # return an empty list if no synonyms can be retrieved from word


class Meaning: 
    """One part of speech of a word and all its definitions."""

    def __init__(self, data):
        self.part_of_speech = data["partOfSpeech"]

        self.definitions = []
        # Loop over raw dictionary from API response
        for definition_dict in data["definitions"]: 
            self.definitions.append(Definition(definition_dict))


class WordEntry:
    """Stores the header (.word and phonetic), and the word's meanings."""

    def __init__(self, data):
        self.word = data["word"]
        self.phonetic = data.get("phonetic", "")

        self.meanings = [] 
        for meaning_dict in data["meanings"]:
            self.meanings.append(Meaning(meaning_dict)) 


if __name__ == "__main__":
    # Fetch inputted word's raw dictionary data
    data = fetch_word("serendipity")

    # Build the word's entry header (.word and phonetcs)
    entry = WordEntry(data[0])
    print(entry.word, entry.phonetic)

    # Loop through each Meaning, followed by each Definition
    for meaning in entry.meanings: 
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
                print("    Synonym(s): none")
                
    # Test split_labels and split_spaces
    print(split_labels("(usually transitive) To have a strong affection."))
    print(split_labels("Strong affection."))
    print(split_spaces("I love my spouse.   I love you!"))