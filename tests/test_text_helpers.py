from dictionary_models import split_spaces, split_labels
from fetch_dictionary_api import is_valid_word


# Test for splitting spaces
def test_split_spaces_flattened():
    assert split_spaces("I love my spouse.   I love you!") == "I love my spouse. I love you!"


def test_split_spaces_ignores_normal_text():
    assert split_spaces("Strong affection.") == "Strong affection."


# Tests for splitting labels 
def test_split_labels_splits_correctly():
    label, rest = split_labels("(usually transitive) To have a strong affection.")
    assert label == "usually transitive"
    assert rest == "To have a strong affection."


def test_split_labels_without_label():
    assert split_labels("Strong affection.") == ("", "Strong affection.")


def test_split_labels_with_missing_closing_bracket():
    assert split_labels("(this text has no closing bracket") == ("", "(this text has no closing bracket")


# Tests for valid words
def test_is_valid_word_accepts_real_words():
    assert is_valid_word("serendipity") # a normal word
    assert is_valid_word("high-rise") # a word with a hyphen
    assert is_valid_word("cant") # a word with an apostrophe


def test_is_valid_word_rejects_junk_words():
    assert not is_valid_word("") # an empty word
    assert not is_valid_word("$!$*(@_)") # a word full of digits
    assert not is_valid_word("1234") # a word full of number strings
    assert not is_valid_word("ch0-m") # a word with symbols inside it