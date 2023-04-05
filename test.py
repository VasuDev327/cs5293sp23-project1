# test names
# test dates
# test genders
# test phones
# test address

from redactor import redact_names_fun, redact_date_fun, redact_genders_fun, redact_phone_fun, redact_address_fun

import spacy
import pytest

@pytest.fixture
def nlp():
    return spacy.load("en_core_web_sm")

def test_redact_names_fun(nlp):
    # Arrange
    inp_text = "My name is Vasu Deva Nadha Janapala."
    doc = nlp(inp_text)
    file_tracker = {}

    # Act
    # breakpoint()
    res = redact_names_fun(inp_text, doc, file_tracker)

    # Assert
    assert isinstance(res, str)
    assert file_tracker["names"]["count"] == 4
    assert res == 'My name is ████ ████ █████ ████████.'

def test_redact_date_fun():
    # Arrange
    inp_text = "10/12/2023 is reunion day"
    file_tracker = {}

    # Act
    # breakpoint()
    res = redact_date_fun(inp_text, inp_text, file_tracker)

    # Assert
    assert isinstance(res, str)
    assert file_tracker["dates"]["count"] == 1
    assert res == '██████████ is reunion day'

def test_redact_genders_fun(nlp):
    # Arrange
    inp_text = "There is guy called Ravana. He was a king for Srilanka"
    file_tracker = {}
    doc = nlp(inp_text)
    # Act
    # breakpoint()
    res = redact_genders_fun(inp_text, doc, file_tracker)

    # Assert
    assert isinstance(res, str)
    assert file_tracker["genders"]["count"] == 1
    assert res == 'There is guy called Ravana. ██ was a king for Srilanka'

def test_redact_phone_fun():
    inp_text = "Our office number is 902-992-9021. Alternate number is (919)982-9081"
    file_tracker = {}

    res = redact_phone_fun(inp_text, inp_text, file_tracker)
    # breakpoint()
    assert isinstance(res, str)
    assert res == 'Our office number is ████████████. Alternate number is █████████████'
    assert file_tracker["phones"]["count"] == 2

def test_redact_address_fun(nlp):
    inp_text = "My company is in Newyork, US, 72134"
    file_tracker = {}
    doc = nlp(inp_text)

    res = redact_address_fun(inp_text, doc, file_tracker, inp_text)
    # breakpoint()
    assert isinstance(res, str)
    assert res == 'My company is in ███████, ██, █████'
    assert file_tracker["address"]["count"] == 3
