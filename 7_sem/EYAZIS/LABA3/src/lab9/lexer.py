from abc import ABC, abstractmethod
from typing import Callable, cast
import nltk
nltk.download('averaged_perceptron_tagger_eng')
from natasha import (
    Doc,
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    MorphVocab,
)

class Lexer(ABC):
    @abstractmethod
    def analyze(self, text: str, on_lemma: Callable[[str], None]) -> None:
        ...


class RussianLexer(Lexer):
    _segmenter = Segmenter()
    _morph_vocab = MorphVocab()
    _emb = NewsEmbedding()
    _morph_tagger = NewsMorphTagger(_emb)

    def analyze(self, text: str, on_lemma: Callable[[str], None]) -> None:
        doc = Doc(text)
        doc.segment(self._segmenter)
        doc.tag_morph(self._morph_tagger)
        for token in doc.tokens: # type: ignore
            token.lemmatize(self._morph_vocab)
            lemma = cast(str, token.lemma)
            if not lemma.isalpha():
                continue
            if lemma:
                on_lemma(lemma.lower())


class EnglishLexer(Lexer):
    def __init__(self):
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/wordnet')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('punkt')
            nltk.download('wordnet')
            nltk.download('averaged_perceptron_tagger')
    
    def analyze(self, text: str, on_lemma: Callable[[str], None]) -> None:
        tokens = nltk.tokenize.word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        for word, pos in pos_tags:
            if not word.isalpha():
                continue
            wordnet_pos = self._nltk_pos_tag_to_wordnet(pos)
            lemma = self.lemmatizer.lemmatize(word.lower(), pos=wordnet_pos)
            on_lemma(lemma)

    @staticmethod
    def _nltk_pos_tag_to_wordnet(tag: str) -> str:
        if tag.startswith('J'):
            return 'a'
        elif tag.startswith('V'):
            return 'v'
        elif tag.startswith('N'):
            return 'n'
        elif tag.startswith('R'):
            return 'r'
        else:
            return 'n'