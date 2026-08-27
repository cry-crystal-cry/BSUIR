from typing import Optional
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy import sparse

from lexer import Lexer


class Index:
    def __init__(
        self,
        lexer: Lexer,
        *, 
        terms_len: int = 10000, 
        stopwords: Iterable[str] = [],
    ) -> None:
        self.lexer = lexer
        self.terms_len = terms_len
        self.stopwords = set(stopwords)
        self.term_weights: Optional[sparse.csr_matrix] = None
        self.term_freq_matrix: Optional[sparse.csr_matrix] = None
        self.documents_paths: list[Path] = []
        self.terms: dict[str, int] = {}

    def __getitem__(self, id: int) -> Path:
        return self.documents_paths[id]
    
    def __len__(self) -> int:
        return len(self.documents_paths)
    
    def __bool__(self) -> bool:
        return len(self) != 0
    
    def __contains__(self, item: Path) -> bool:
        return item in self.documents_paths
    
    def update_terms(self) -> None:
        terms: dict[str, int] = {}
        document_ids: list[int] = []
        term_ids: list[int] = []

        def on_term(term: str) -> None:
            if not term.isalpha():
                return
            if term in self.stopwords:
                return
            if term not in terms:
                terms[term] = len(terms)
            document_ids.append(i)
            term_ids.append(terms[term])
        
        for i, document_path in enumerate(self.documents_paths):
            with open(document_path, encoding='utf-8') as document_file:
                document_text = document_file.read()
                self.lexer.analyze(document_text, on_term)
        term_freq = sparse.coo_matrix(
            (np.ones_like(term_ids), (document_ids, term_ids))
        ).tocsr()


        doc_freq = np.asarray(term_freq.sign().sum(axis=0)).flatten()
        inv_freq = np.log2(len(self.documents_paths) / doc_freq)
        n = min(self.terms_len, len(terms))
        terms_idx = np.argpartition(inv_freq, -n)[-n:] 
        id_to_term = {idx: term for term, idx in terms.items()}
        inf_terms = [id_to_term[i] for i in terms_idx]
        self.terms = {term: i for i, term in enumerate(inf_terms)}
        self.term_freq_matrix = term_freq[:, terms_idx]
        self.update_weights()
    
    def update_weights(self) -> None:
        doc_freq = np.asarray(self.term_freq_matrix.sign().sum(axis=0)).flatten()
        inv_freq = np.log2(len(self.documents_paths) / doc_freq)
        tfidf_matrix = self.term_freq_matrix.multiply(inv_freq) 
        norms = np.asarray(np.sqrt(tfidf_matrix.power(2).sum(axis=1))).flatten()
        norms[norms == 0] = 1.0
        self.term_weights = sparse.diags(1 / (norms)) @ tfidf_matrix
            
    def add(self, *document_paths: Path) -> None:
        new_documents = list(
            set(map(Path.resolve, document_paths))
            .difference(self.documents_paths)
        )
        if not new_documents:
            return
        self.documents_paths += new_documents
        if not self.terms:
            return
        document_ids: list[int] = []
        term_ids: list[int] = []

        def on_term(term):
            if term not in self.terms:
                return
            document_ids.append(i)
            term_ids.append(self.terms[term])
        
        for i, document_path in enumerate(new_documents):
            with open(document_path, encoding='utf-8') as document_file:
                document_text = document_file.read()
            self.lexer.analyze(document_text, on_term)
        
        new_term_freq = sparse.coo_matrix(
            (np.ones_like(term_ids), (document_ids, term_ids)),
            shape=(len(new_documents), len(self.terms))
        ).tocsr()
        self.term_freq_matrix = sparse.vstack(
            (self.term_freq_matrix, new_term_freq)
        )
        self.update_weights()
