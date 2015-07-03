# encoding: utf-8

"""Defintion of element classes related to words"""

from xml.etree import cElementTree as ET

from .base import NLGElement
from ..lexicon.feature.lexical import (DEFAULT_INFL, DEFAULT_SPELL, INFLECTIONS,
                                       SPELL_VARS, BASE_FORM)
from ..lexicon.feature.internal import BASE_WORD
from ..lexicon.category import ANY
from ..lexicon.lang import ENGLISH, FRENCH
from ..exc import UnhandledLanguage


class WordMixin(object):

    """Class defining the behaviour of a word."""

    @property
    def children(self):
        """A word has no children. Return an empty list."""
        return []

    def __unicode__(self):
        return u"<%s [%s:%s]>" % (
            self.__class__.__name__,
            self.base_form,
            self.category if self.category else u'no category')


class WordElement(WordMixin, NLGElement):

    """Element defining rules and behaviour for a word."""

    def __init__(self, base_form, category, id, lexicon):
        """Create a WordElement with the specified baseForm, category,
        ID and lexicon.

        :param base_form: the base form of WordElement
        :param category: the category of WordElement
        :param id: the ID of word in lexicon
        :param lexicon: the lexicon from witch this WordElement comes from

        """
        super(WordElement, self).__init__(category=category, lexicon=lexicon)
        self.base_form = base_form
        self.id = id

    def __eq__(self, other):
        if isinstance(other, WordElement):
            return (
                self.base_form == other.base_form
                and self.id == other.id
                and self.features == other.features
            )
        return False

    @property
    def default_inflection_variant(self):
        return self.features[DEFAULT_INFL]

    @default_inflection_variant.setter
    def default_inflection_variant(self, variant):
        self.features[DEFAULT_INFL] = variant

    @property
    def inflection_variants(self):
        return self.features[INFLECTIONS]

    @inflection_variants.setter
    def inflection_variants(self, variants):
        if not isinstance(variants, list):
            variants = [variants]
        self.features[INFLECTIONS] = variants

    @property
    def spelling_variants(self):
        return self.features[SPELL_VARS]

    @spelling_variants.setter
    def spelling_variants(self, variant):
        self.features[SPELL_VARS] = variant

    @property
    def default_spelling_variant(self):
        default_spelling = self.features[DEFAULT_SPELL]
        return self.base_form if default_spelling is None else default_spelling

    @default_spelling_variant.setter
    def default_spelling_variant(self, variant):
        self.features[DEFAULT_SPELL] = variant

    @property
    def children(self):
        return []

    def to_xml(self, pretty=False):
        """Export the WordElement to an XML string stucture."""
        word_tree = ET.Element('word')
        if self.base_form is not None:
            base = ET.SubElement(word_tree, 'base')
            base.text = self.base_form
        if self.category != ANY:
            cat = ET.SubElement(word_tree, 'category')
            cat.text = self.category
        if self.id is not None:
            _id = ET.SubElement(word_tree, 'id')
            _id.text = self.id
        return ET.tostring(word_tree, encoding='utf-8')

    def realize_syntax(self):
        if not self.elided:
            # TODO, when InflectedWordElement is implemented
            # infl = InflectedWordElement(word=self, category=None)  # None ??
            # return infl.realize_syntax()
            pass

    def realize_morphology(self):
        if self.default_spelling_variant:
            # TODO when StringElement is implemented
            # return StringElement(param=self.default_spelling_variant,
            # word=None)
            pass


class InflectedWordElement(WordMixin, NLGElement):

    """TODO"""

    _morphology_rules = {
        # TODO: must be real class
        ENGLISH: "NonStaticMorphologyRules",
        # TODO: must be real class
        FRENCH: "MorphologyRulesFrench",
    }

    def __init__(self, word, category=None):
        """Constructs a new inflected word using the argument word as
        the base form.

        Constructing the word also requires a lexical category (such as noun,
        verb).

        :param word: the base form for this inflected word.
        :param category: the lexical category for the word.

        """
        if not category:
            if word:
                #  the inflected word inherits all features from the base word
                #  (moved from WordElement.realise_syntax())
                self.features = word.features.copy()
                self.features[BASE_WORD] = word
                self.features[BASE_FORM] = word.default_spelling
                self.category = self.word.category
            else:
                self.category = ANY

    @property
    def base_word(self):
        return self.features.get(BASE_WORD)

    @base_word.setter
    def base_word(self, word):
        self.features[BASE_WORD] = word

    @property
    def base_form(self):
        return self.features[BASE_FORM]

    @property
    def lexicon(self):
        if self.word:
            return self.base_word.lexicon

    @property
    def morphology_rules(self):
        try:
            return self._morphology_rules[self.language]
        except KeyError:
            raise UnhandledLanguage('The %s language is currently unhandled' % (
                self.language))

    def realize_syntax(self):
        if self.elided or not all(self.lexicon and self.base_form):
            return None