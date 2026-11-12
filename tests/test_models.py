import pytest

from dictionary_models import Definition, Meaning, WordEntry


# Fake API entry with labels, unflattened spaces and missing optional keys
FAKE_API_ENTRY = {
    "word": "run",
    "phonetic": "/ɹʌn/",
    "meanings": [
        {
            "partOfSpeech": "verb",
            "definitions": [
                {
                    "definition": "(intransitive) To move quickly on foot.",
                    "example": "She  runs   every morning.",
                    "synonyms": ["jog", "sprint"],
                },
                {"definition": "To manage or operate."},
            ],
        },
        {
            "partOfSpeech": "noun",
            "definitions": [{"definition": "An act of running."}],
        },
    ],
}

RAW_FIRST_DEFINITION= FAKE_API_ENTRY["meanings"][0]["definitions"][0]
RAW_SECOND_DEFINITION = FAKE_API_ENTRY["meanings"][0]["definitions"][1]


# Test definitions
def test_definition_cleans_text_and_extracts_label():
    first_definition = Definition(RAW_FIRST_DEFINITION)
    assert first_definition.label == "intransitive"
    assert first_definition.text == "To move quickly on foot."
    assert first_definition.example == "She runs every morning."
    assert first_definition.synonyms == ["jog", "sprint"]


def test_definition_has_missing_optional_fields():
    second_definition = Definition(RAW_SECOND_DEFINITION)
    assert second_definition.label == ""
    assert second_definition.example is None   
    assert second_definition.synonyms == []


# Test meaning     
def test_meaning_wraps_each_dictionary_in_definition():
    meaning = Meaning(FAKE_API_ENTRY["meanings"][0])
    assert meaning.part_of_speech == "verb"
    assert len(meaning.definitions) == 2
    assert isinstance(meaning.definitions[0], Definition)


def test_meaning_has_part_of_speech():
    with pytest.raises(KeyError):
        Meaning({"definitions": []})


# Test word entry
def test_word_entry_builds_meanings_and_header():
    entry = WordEntry(FAKE_API_ENTRY)
    assert entry.word == "run"
    assert entry.phonetic == "/ɹʌn/"
    assert len(entry.meanings) == 2
    assert entry.meanings[1].part_of_speech == "noun"
    assert entry.meanings[0].definitions[1].text == "To manage or operate."


def test_word_entry_has_missing_phonetic():
    entry = WordEntry({"word": "run", "meanings": []})
    assert entry.phonetic == ''
    assert entry.meanings == []