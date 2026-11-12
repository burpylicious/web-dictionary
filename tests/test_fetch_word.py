import pytest
import requests

from fetch_dictionary_api import BASE_URL, fetch_word, InvalidWordError, WordNotFoundError, DictionaryUnavailableError

# URL to fetch dictionary for the word "run"
WORD_URL = BASE_URL + "run"


# Test to see if invalid word is caught before any request is made
def test_invalid_input_is_rejected_from_start():
    with pytest.raises(InvalidWordError):
        fetch_word("123")


@pytest.mark.parametrize(
    "fake_reply, expected_error",
    [
        ({"status_code": 404}, WordNotFoundError), # if word not found
        ({"status_code": 500}, DictionaryUnavailableError), # if server error
        ({"exc": requests.exceptions.ConnectionError}, DictionaryUnavailableError), # no internet connection
        ({"text": "<html>503</html>"}, DictionaryUnavailableError), # if bad JSON
        ({"json": []}, DictionaryUnavailableError), # if empty list
    ],
    ids=["word not found", "server error", "no internet connection", "bad json", "empty list"],
)


def test_fetch_word_raises_expected_errors(requests_mock, fake_reply, expected_error):
    requests_mock.get(WORD_URL, **fake_reply)
    with pytest.raises(expected_error):
        fetch_word("run")


def test_fetch_word_returns_data_successfully(requests_mock):
    requests_mock.get(WORD_URL, json=[{"word": "run"}])
    assert fetch_word("run") == [{'word': 'run'}]