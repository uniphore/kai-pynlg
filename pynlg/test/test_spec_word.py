# encoding: utf-8

"""Test suite of the WordElement class."""

import pytest

from ..spec.word import WordElement
from ..lexicon.category import NOUN, ADJECTIVE, ANY


@pytest.fixture(scope='module')
def word():
    return WordElement(
        base_form='fish',
        category=NOUN,
        id="E123",
        lexicon=None)


@pytest.mark.parametrize("word,other_word", [
    (
        WordElement('beau', ADJECTIVE, "E123", None),
        WordElement('beau', ADJECTIVE, "E123", None),
    ),
    pytest.mark.xfail((
        WordElement('joli', ADJECTIVE, "E1", None),
        WordElement('beau', ADJECTIVE, "E123", None),
    )),
    pytest.mark.xfail((
        WordElement('joli', ADJECTIVE, "E1", None),
        'something',
    ))
])
def test_equality(word, other_word):
    assert word == other_word


def test_default_inflection_variant(word):
    word.default_inflection_variant = 'fish'
    assert word.default_inflection_variant == 'fish'


def test_inflectional_variants(word):
    word.inflectional_variants = ['fish', 'fishes']
    assert word.inflectional_variants == ['fish', 'fishes']


def test_spelling_variants(word):
    word.spelling_variants = [u'clé', u'clef']
    assert word.spelling_variants == [u'clé', u'clef']


def test_default_spelling_variant(word):
    word.default_spelling_variant = u'clé'
    assert word.default_spelling_variant == u'clé'


def test_children(word):
    assert word.children == []


@pytest.mark.parametrize('word,xml', [
    (
        WordElement(
            base_form='beau', category=ADJECTIVE, id="E1", lexicon=None),
        '<word><base>beau</base><category>ADJECTIVE</category><id>E1</id></word>'
    ),
    (
        WordElement(
            base_form='beau', category=ADJECTIVE, id=None, lexicon=None),
        '<word><base>beau</base><category>ADJECTIVE</category></word>'
    ),
    (
        WordElement(base_form='beau', category=ANY, id="E1", lexicon=None),
        '<word><base>beau</base><id>E1</id></word>'
    ),
    (
        WordElement(base_form=None, category=ADJECTIVE, id="E1", lexicon=None),
        '<word><category>ADJECTIVE</category><id>E1</id></word>'
    ),
])
def test_to_xml(word, xml):
    assert word.to_xml() == xml