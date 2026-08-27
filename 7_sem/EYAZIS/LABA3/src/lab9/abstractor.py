from abc import ABC, abstractmethod
import nltk
import numpy as np
import requests
from index import Index

class Abstractor(ABC):
    @abstractmethod
    def abstract(self, text: str) -> str:
        """Принимает текст строкой и возвращает реферат"""
        ...

class SentenceAbstractor(Abstractor):
    def __init__(
        self,
        language: str,
        index: Index,
        n=10
    ) -> None:
        self.index = index    
        self.language = language
        self.n = n

    def abstract(self, text: str) -> str:
        if not text.strip():
            return ""

        # Разбираем текст на предложения и параграфы
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        psentences = [
            nltk.sent_tokenize(p, language=self.language) 
            for p in paragraphs
        ]
        sentences = sum(psentences, [])
        if not sentences:
            return ""

        # 1. Считаем веса слов для всего входного текста (TF-IDF)
        # Нам нужно знать, как часто слова из текста встречаются в глобальном индексе
        text_vector = self._get_vector(text)
        max_tf = text_vector.max()
        
        # Считаем IDF на основе глобальной матрицы индекса
        doc_freq = np.asarray(self.index.term_freq_matrix.sign().sum(axis=0)).flatten()
        # +1 для сглаживания, если индекс пустой
        idf = np.log2((len(self.index) + 1) / (doc_freq + 1e-8))
        
        if max_tf == 0:
            word_weights = np.zeros_like(idf)
        else:
            tf_norm = 0.5 * (1 + text_vector / max_tf)
            word_weights = tf_norm * idf

        # 2. Считаем веса предложений
        tfidf_scores = []
        for s in sentences:
            s_vector = self._get_vector(s)
            # Вес предложения — скалярное произведение частот его слов на веса слов текста
            tfidf_scores.append(s_vector @ word_weights)

        # 3. Позиционные веса
        posp = np.array(sum(([self.pos(p, i) for i in range(len(p))] for p in psentences), []))
        posd = np.array([self.pos(sentences, i) for i in range(len(sentences))])

        sentences_weights = posp * posd * np.array(tfidf_scores)

        # 4. Отбор лучших предложений
        n_to_pick = min(len(sentences), self.n)
        if n_to_pick == 0:
            return ""
            
        indices = np.argpartition(sentences_weights, -n_to_pick)[-n_to_pick:]
        # Сортируем по порядку появления в тексте для связности
        indices = np.sort(indices)
        
        return ' '.join(sentences[i] for i in indices)

    def _get_vector(self, text: str) -> np.ndarray:
        """Превращает строку в вектор частот термов на основе словаря индекса"""
        vector = np.zeros(len(self.index.terms))
        def on_term(term: str) -> None:
            t = term.lower()
            if t in self.index.stopwords or not t.isalpha():
                return
            if t in self.index.terms:
                vector[self.index.terms[t]] += 1
        self.index.lexer.analyze(text, on_term)
        return vector

    def pos(self, text: list[str], idx: int) -> float:
        d = sum(len(s) for s in text)
        if d == 0: return 0
        bd = sum(len(s) for s in text[:idx])
        return 1 - bd / d

class KeywordAbstractor(Abstractor):
    def __init__(self, index: Index, k: int = 10):
        self.index = index    
        self.idx_to_term = {idx: term for term, idx in self.index.terms.items()}
        self.k = k

    def abstract(self, text: str) -> str:
        # Считаем частоты слов в переданном тексте
        vector = np.zeros(len(self.index.terms))
        def on_term(term: str) -> None:
            t = term.lower()
            if t in self.index.terms:
                vector[self.index.terms[t]] += 1
        self.index.lexer.analyze(text, on_term)

        max_tf = vector.max()
        if max_tf == 0:
            return ""

        # Берем глобальный IDF из индекса
        doc_freq = np.asarray(self.index.term_freq_matrix.sign().sum(axis=0)).flatten()
        idf = np.log2((len(self.index) + 1) / (doc_freq + 1e-8))

        tf_norm = 0.5 * (1 + vector / max_tf)
        weights = tf_norm * idf

        n_to_pick = min(self.k, len(self.index.terms))
        if n_to_pick == 0:
            return ""

        top_indices = np.argpartition(weights, -n_to_pick)[-n_to_pick:]
        # Сортируем по убыванию веса
        top_indices = top_indices[np.argsort(-weights[top_indices])]

        keywords = [self.idx_to_term[i] for i in top_indices if weights[i] > 0]
        return ", ".join(keywords)

class LLMAbstractor(Abstractor):
    def __init__(
        self,
        prompt_template: str,
        api_key: str,
        url="https://api.groq.com/openai/v1/chat/completions",
        n=10
    ) -> None:
        self.prompt_template = prompt_template
        self.url = url
        self.api_key = api_key
        self.n = n

    def abstract(self, text: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Теперь просто подставляем аргумент text напрямую в промпт
        data = {
            "model": "openai/gpt-oss-120b",
            "messages": [
                {
                    "role": "user", 
                    "content": self.prompt_template.format(self.n, text)
                }
            ]
        }
        try:
            response = requests.post(self.url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                raise RuntimeError(f"Ошибка сервиса: {response.status_code} {response.text}")
        except Exception as e:
            raise RuntimeError(f"Не удалось связаться с LLM: {e}")