import os
import json
import docx
import pdfplumber
from collections import defaultdict, Counter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import nltk
from nltk.tokenize import word_tokenize
import pymorphy2
from natasha import Segmenter, NewsEmbedding, NewsSyntaxParser, Doc
from striprtf.striprtf import rtf_to_text
from bs4 import BeautifulSoup

# Инициализация NLTK
nltk.download('punkt')

# Инициализация pymorphy2
morph = pymorphy2.MorphAnalyzer()

# Словарь перевода
TAG_TRANSLATIONS = {
    # Морфологические теги (pymorphy2)
    'NOUN': 'существительное', 'ADJF': 'прилагательное (полное)', 'ADJS': 'прилагательное (краткое)',
    'COMP': 'сравнительная степень', 'VERB': 'глагол', 'INFN': 'инфинитив',
    'PRTF': 'причастие (полное)', 'PRTS': 'причастие (краткое)', 'GRND': 'деепричастие',
    'NUMR': 'числительное', 'ADVB': 'наречие', 'NPRO': 'местоимение', 'PRED': 'предикатив',
    'PREP': 'предлог', 'CONJ': 'союз', 'PRCL': 'частица', 'INTJ': 'междометие',
    'masc': 'мужской род', 'femn': 'женский род', 'neut': 'средний род',
    'sing': 'единственное число', 'plur': 'множественное число',
    'nomn': 'именительный падеж', 'gent': 'родительный падеж', 'datv': 'дательный падеж',
    'accs': 'винительный падеж', 'ablt': 'творительный падеж', 'loct': 'предложный падеж',
    'anim': 'одушевлённое', 'inan': 'неодушевлённое', 'pres': 'настоящее время',
    'past': 'прошедшее время', 'futr': 'будущее время', '1per': '1-е лицо', '2per': '2-е лицо', '3per': '3-е лицо',
    'perf': 'совершенный вид', 'impf': 'несовершенный вид', 'indc': 'изъявительное наклонение',
    'impr': 'повелительное наклонение',
    # Синтаксические теги (Natasha, Universal Dependencies)
    'det': 'определитель',
    'case': 'падежная связь',
    'obl': 'косвенное дополнение',
    'amod': 'прилагательное модификатор',
    'punct': 'пунктуация',
    'nsubj': 'именное подлежащее',
    'root': 'корень',
    'obj': 'прямое дополнение',
    'nmod': 'именной модификатор',
    'acl': 'придаточное описание',
    'cc': 'сочинительный союз',
    'conj': 'соединённый элемент',
    'advmod': 'наречный модификатор'
}

class CorpusManager:
    def __init__(self):
        self.corpus = []
        self.word_index = defaultdict(list)  # Индекс для слов
        self.lemma_index = defaultdict(list)  # Индекс для лемм
        self.morph_cache = {}
        # Инициализация Natasha
        self.segmenter = Segmenter()
        self.embedding = NewsEmbedding()
        self.syntax_parser = NewsSyntaxParser(self.embedding)

    def read_txt(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def read_docx(self, filepath):
        doc = docx.Document(filepath)
        return " ".join([para.text for para in doc.paragraphs])

    def read_pdf(self, filepath):
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def read_rtf(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            rtf = f.read()
        return rtf_to_text(rtf)

    def read_html(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        return soup.get_text()

    def tokenize_text(self, text):
        return [word.strip('.,!"«»:;()') for word in word_tokenize(text) if word.isalpha()]

    def add_text(self, text, metadata):
        tokens = self.tokenize_text(text)
        token_data = []
        for i, word in enumerate(tokens):
            if word not in self.morph_cache:
                parsed = morph.parse(word)[0]
                self.morph_cache[word] = {
                    "lemma": parsed.normal_form,
                    "pos": str(parsed.tag.POS),
                    "tags": self.translate_tags(parsed.tag)
                }
            token_info = self.morph_cache[word]
            token_data.append({
                "word": word,
                "lemma": token_info["lemma"],
                "pos": token_info["pos"],
                "tags": token_info["tags"]
            })
            self.word_index[word.lower()].append((len(self.corpus), i))
            self.lemma_index[token_info["lemma"].lower()].append((len(self.corpus), i))

        # Синтаксический анализ с Natasha
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.parse_syntax(self.syntax_parser)
        syntax_data = []
        for sentence in doc.sents:
            # Создаем словарь токенов для быстрого доступа по id
            token_dict = {token.id: token for token in sentence.tokens}
            dependencies = []
            for token in sentence.tokens:
                # Если есть head_id, находим родительский токен
                head = token_dict.get(token.head_id, None)
                head_text = head.text if head else "root"  # Если head_id указывает на корень, используем "root"
                rel_translated = TAG_TRANSLATIONS.get(token.rel, token.rel)
                dependencies.append((token.text, head_text, rel_translated))
            syntax_data.append({
                "sentence": sentence.text,
                "dependencies": dependencies
            })

        self.corpus.append({
            "text": text,
            "tokens": token_data,
            "metadata": metadata,
            "syntax": syntax_data
        })

    def translate_tags(self, tag_str):
        return ', '.join([TAG_TRANSLATIONS.get(part, part) for part in str(tag_str).split(',')])

    def search(self, query, search_type="word"):
        results = []
        index = self.lemma_index if search_type == "lemma" else self.word_index
        for doc_id, token_id in index.get(query.lower(), []):
            doc = self.corpus[doc_id]
            token = doc["tokens"][token_id]
            context = self.get_context(doc, token_id)
            results.append({
                "doc_id": doc_id,
                "metadata": doc["metadata"],
                "word": token["word"],
                "lemma": token["lemma"],
                "pos": token["pos"],
                "tags": token["tags"],
                "context": context
            })
        return results

    def get_context(self, doc, token_id, window=5):
        tokens = [t["word"] for t in doc["tokens"]]
        start = max(0, token_id - window)
        end = min(len(tokens), token_id + window + 1)
        return " ".join(tokens[start:end])

    def get_statistics(self):
        word_freq = Counter()
        lemma_freq = Counter()
        pos_freq = Counter()
        for doc in self.corpus:
            for token in doc["tokens"]:
                word_freq[token["word"]] += 1
                lemma_freq[token["lemma"]] += 1
                pos_freq[token["pos"]] += 1
        return {
            "word_freq": word_freq.most_common(10),
            "lemma_freq": lemma_freq.most_common(10),
            "pos_freq": pos_freq.most_common()
        }

    def get_syntax(self, doc_id):
        if doc_id < len(self.corpus):
            return self.corpus[doc_id]["syntax"]
        return []

    def save_corpus(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.corpus, f, ensure_ascii=False, indent=2)

def add_tooltip(widget, text):
    def show_tooltip(event):
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        tk.Label(tooltip, text=text, background="lightyellow", borderwidth=1, relief="solid").pack()
        widget.tooltip = tooltip
    def hide_tooltip(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

def launch_gui():
    def load_file():
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("Word Documents", "*.docx"), ("PDF files", "*.pdf"),
                       ("RTF files", "*.rtf"), ("HTML files", "*.html")]
        )
        if not filepath:
            return
        try:
            if filepath.endswith('.txt'):
                text = corpus.read_txt(filepath)
            elif filepath.endswith('.docx'):
                text = corpus.read_docx(filepath)
            elif filepath.endswith('.pdf'):
                text = corpus.read_pdf(filepath)
            elif filepath.endswith('.rtf'):
                text = corpus.read_rtf(filepath)
            elif filepath.endswith('.html'):
                text = corpus.read_html(filepath)
            metadata = {
                "title": os.path.basename(filepath),
                "source": "Загруженный файл",
                "date": "2025-05-15",
                "type": "unknown"
            }
            corpus.add_text(text, metadata)
            messagebox.showinfo("Успех", "Текст добавлен в корпус")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def search():
        query = search_entry.get()
        search_type = search_type_var.get()
        results = corpus.search(query, search_type)
        output_box.delete(1.0, tk.END)
        for result in results:
            output_box.insert(tk.END, f"Документ: {result['metadata']['title']}\n")
            output_box.insert(tk.END, f"Слово: {result['word']} (Лемма: {result['lemma']})\n")
            output_box.insert(tk.END, f"Часть речи: {result['pos']}\n")
            output_box.insert(tk.END, f"Теги: {result['tags']}\n")
            output_box.insert(tk.END, f"Контекст: {result['context']}\n\n")

    def show_stats():
        stats = corpus.get_statistics()
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "Топ-10 слов:\n")
        for word, freq in stats["word_freq"]:
            output_box.insert(tk.END, f"{word}: {freq}\n")
        output_box.insert(tk.END, "\nТоп-10 лемм:\n")
        for lemma, freq in stats["lemma_freq"]:
            output_box.insert(tk.END, f"{lemma}: {freq}\n")
        output_box.insert(tk.END, "\nЧасти речи:\n")
        for pos, freq in stats["pos_freq"]:
            output_box.insert(tk.END, f"{pos}: {freq}\n")

    def show_syntax():
        output_box.delete(1.0, tk.END)
        for doc_id, doc in enumerate(corpus.corpus):
            output_box.insert(tk.END, f"Документ: {doc['metadata']['title']}\n")
            for sent_data in corpus.get_syntax(doc_id):
                output_box.insert(tk.END, f"Предложение: {sent_data['sentence']}\n")
                output_box.insert(tk.END, "Зависимости:\n")
                for word, head, rel in sent_data["dependencies"]:
                    output_box.insert(tk.END, f"  {word} -> {head} ({rel})\n")
                output_box.insert(tk.END, "\n")

    def save_corpus():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if filepath:
            corpus.save_corpus(filepath)
            messagebox.showinfo("Успех", f"Корпус сохранён в {filepath}")

    def export_results():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                for doc_id, doc in enumerate(corpus.corpus):
                    f.write(f"Документ: {doc['metadata']['title']}\n")
                    for sent_data in corpus.get_syntax(doc_id):
                        f.write(f"Предложение: {sent_data['sentence']}\n")
                        f.write("Зависимости:\n")
                        for word, head, rel in sent_data["dependencies"]:
                            f.write(f"  {word} -> {head} ({rel})\n")
                        f.write("\n")
            messagebox.showinfo("Успех", f"Результаты сохранены в {filepath}")

    def show_help():
        help_window = tk.Toplevel()
        help_window.title("Справка")
        tk.Label(help_window, text="Инструкция по использованию\n\n"
                                  "1. Загрузите текст через кнопку 'Загрузить текст'.\n"
                                  "2. Выполните поиск по слову или лемме.\n"
                                  "3. Просмотрите статистику или синтаксический анализ.\n"
                                  "4. Сохраните корпус или экспортируйте результаты.").pack(padx=10, pady=10)
        tk.Button(help_window, text="Закрыть", command=help_window.destroy).pack()

    corpus = CorpusManager()

    root = tk.Tk()
    root.title("Корпусный менеджер")
    root.geometry("1000x700")

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill='x')

    load_button = ttk.Button(frame, text="Загрузить текст", command=load_file)
    load_button.pack(side='left', padx=5)
    add_tooltip(load_button, "Загрузить текстовый файл (TXT, DOCX, PDF, RTF, HTML)")

    save_button = ttk.Button(frame, text="Сохранить корпус", command=save_corpus)
    save_button.pack(side='left', padx=5)
    add_tooltip(save_button, "Сохранить корпус в формате JSON")

    stats_button = ttk.Button(frame, text="Показать статистику", command=show_stats)
    stats_button.pack(side='left', padx=5)
    add_tooltip(stats_button, "Показать статистику по словам, леммам и частям речи")

    syntax_button = ttk.Button(frame, text="Показать синтаксис", command=show_syntax)
    syntax_button.pack(side='left', padx=5)
    add_tooltip(syntax_button, "Показать синтаксический анализ (зависимости)")

    export_button = ttk.Button(frame, text="Экспортировать результаты", command=export_results)
    export_button.pack(side='left', padx=5)
    add_tooltip(export_button, "Экспортировать результаты в текстовый файл")

    help_button = ttk.Button(frame, text="Справка", command=show_help)
    help_button.pack(side='left', padx=5)
    add_tooltip(help_button, "Открыть справку по использованию")

    search_frame = ttk.Frame(root)
    search_frame.pack(padx=10, pady=5, fill='x')
    ttk.Label(search_frame, text="Поиск:").pack(side='left')
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side='left', fill='x', expand=True, padx=5)
    search_type_var = tk.StringVar(value="word")
    ttk.Radiobutton(search_frame, text="Слово", variable=search_type_var, value="word").pack(side='left')
    ttk.Radiobutton(search_frame, text="Лемма", variable=search_type_var, value="lemma").pack(side='left')
    ttk.Button(search_frame, text="Искать", command=search).pack(side='left', padx=5)

    output_box = tk.Text(root, wrap='word')
    output_box.pack(expand=True, fill='both', padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()