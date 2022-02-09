"""Unittests of scaaml/io/spell_check.py"""

import pytest

from scaaml.io.spell_check import find_misspellings, spell_check_word


def test_find_misspellings_bad():
    """Misspelling to be found."""
    bad_words = ['lorem', 'licence', 'dolor', 'sit', 'amet', '', 'license']
    with pytest.raises(ValueError) as verror:
        find_misspellings(words=bad_words)
    assert 'Unsupported spelling' in str(verror.value)


def test_find_misspellings_with_dictionary():
    dictionary = {
        'licence': 'https://creativecommons.org/licenses/by/4.0/',
        'compression': 'GZIP',
    }
    find_misspellings(words=dictionary.keys())

    dictionary['license'] = 'Wrong spelling'
    with pytest.raises(ValueError) as verror:
        find_misspellings(words=dictionary.keys())
    assert 'Unsupported spelling' in str(verror.value)


def test_find_misspellings_ok():
    """No misspelling."""
    ok_words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', '', 'licence']
    find_misspellings(words=ok_words)


def test_spell_check_word():
    # ok
    spell_check_word(word='licence',
                     supported='licence',
                     unsupported='license',
                     case_sensitive=False)
    # ok
    spell_check_word(word='licence',
                     supported='licence',
                     unsupported='license',
                     case_sensitive=True)
    # ok (case sensitive test)
    spell_check_word(word='license',
                     supported='licence',
                     unsupported='LICENSE',  # Not equal
                     case_sensitive=True)
    with pytest.raises(ValueError) as verror:
        # raise
        spell_check_word(word='license',
                         supported='licence',
                         unsupported='LICENSE',  # Not equal
                         case_sensitive=False)
    assert 'Unsupported spelling' in str(verror.value)