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

# Словарь перевода тегов
TAG_TRANSLATIONS = {
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
    'impr': 'повелительное наклонение', 'pssv': 'пассивный залог',
    'det': 'определитель', 'case': 'падежная связь', 'obl': 'косвенное дополнение',
    'amod': 'прилагательное модификатор', 'punct': 'пунктуация', 'nsubj': 'именное подлежащее',
    'root': 'корень', 'obj': 'прямое дополнение', 'nmod': 'именной модификатор',
    'acl': 'придаточное описание', 'cc': 'сочинительный союз', 'conj': 'соединённый элемент',
    'advmod': 'наречный модификатор', 'nsubj:pass': 'пассивное подлежащее', 'obl:agent': 'агент в пассиве'
}

# Локальный словарь для эмуляции ConceptNet
LOCAL_CONCEPTNET = {
    "хорошо": [
        {"relation": "Synonym", "target": "прекрасно", "weight": 1.0},
        {"relation": "RelatedTo", "target": "отлично", "weight": 0.8}
    ],
    "сильно": [
        {"relation": "Synonym", "target": "мощно", "weight": 1.0},
        {"relation": "RelatedTo", "target": "интенсивно", "weight": 0.7}
    ],
    "человек": [
        {"relation": "IsA", "target": "существо", "weight": 1.0},
        {"relation": "HasA", "target": "разум", "weight": 0.9}
    ],
    "бить": [
        {"relation": "RelatedTo", "target": "удар", "weight": 1.0},
        {"relation": "Causes", "target": "боль", "weight": 0.6}
    ],
    "очень": [
        {"relation": "Synonym", "target": "крайне", "weight": 1.0},
        {"relation": "RelatedTo", "target": "сильно", "weight": 0.8}
    ]
}

class CorpusManager:
    def __init__(self):
        self.corpus = []
        self.word_index = defaultdict(list)
        self.lemma_index = defaultdict(list)
        self.morph_cache = {}
        self.conceptnet_cache = {}
        self.segmenter = Segmenter()
        self.embedding = NewsEmbedding()
        self.syntax_parser = NewsSyntaxParser(self.embedding)

    def read_txt(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def read_docx(self, filepath):
        doc = docx.Document(filepath)
        return " ".join([para.text for para in doc.paragraphs])

    def read_doc(self, filepath):
        return self.read_docx(filepath)

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

    def get_conceptnet_relations(self, word, lang="ru"):
        if word in self.conceptnet_cache:
            return self.conceptnet_cache[word]
        # Эмуляция ответа ConceptNet с помощью локального словаря
        relations = LOCAL_CONCEPTNET.get(word.lower(), [])
        self.conceptnet_cache[word] = relations
        return relations

    def add_text(self, text, metadata):
        tokens = self.tokenize_text(text)
        token_data = []

        # Синтаксический анализ для контекста
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.parse_syntax(self.syntax_parser)

        # Создаем словарь токенов для быстрого доступа
        token_dict = {}
        for sentence in doc.sents:
            for token in sentence.tokens:
                token_dict[(sentence.start, token.start)] = token

        for i, word in enumerate(tokens):
            # Ищем токен в синтаксическом разборе
            token = None
            for sentence in doc.sents:
                for t in sentence.tokens:
                    if t.text.lower() == word.lower():
                        token = t
                        break
                if token:
                    break

            # Морфологический анализ с учетом синтаксиса
            parses = morph.parse(word)
            parsed = parses[0]
            if token:
                if token.rel == "nsubj":
                    for parse in parses:
                        if "nomn" in str(parse.tag):
                            parsed = parse
                            break
                elif token.rel == "obj":
                    for parse in parses:
                        if "accs" in str(parse.tag):
                            parsed = parse
                            break

            if word not in self.morph_cache:
                self.morph_cache[word] = {
                    "lemma": parsed.normal_form,
                    "pos": str(parsed.tag.POS),
                    "tags": self.translate_tags(parsed.tag),
                    "semantics": self.get_conceptnet_relations(parsed.normal_form)
                }
            token_info = self.morph_cache[word]
            token_data.append({
                "word": word,
                "lemma": token_info["lemma"],
                "pos": token_info["pos"],
                "tags": token_info["tags"],
                "semantics": token_info["semantics"]
            })
            self.word_index[word.lower()].append((len(self.corpus), i))
            self.lemma_index[token_info["lemma"].lower()].append((len(self.corpus), i))

        # Синтаксический и семантический анализ
        syntax_data = []
        for sentence in doc.sents:
            token_dict = {token.id: token for token in sentence.tokens}
            dependencies = []
            semantic_roles = []
            passive = False
            root_token = None
            for token in sentence.tokens:
                if token.rel == "root":
                    root_token = token
                    parsed = morph.parse(token.text)[0]
                    if "pssv" in str(parsed.tag):
                        passive = True
                    break

            for token in sentence.tokens:
                head = token_dict.get(token.head_id, None)
                head_text = head.text if head else "root"
                rel_translated = TAG_TRANSLATIONS.get(token.rel, token.rel)
                dependencies.append((token.text, head_text, rel_translated))

                # Семантические роли
                parsed = morph.parse(token.text)[0]
                if token.rel == "nsubj" and not passive:
                    semantic_roles.append({"word": token.text, "role": "Agent"})
                elif token.rel == "nsubj:pass" and passive:
                    semantic_roles.append({"word": token.text, "role": "Patient"})
                elif token.rel == "obj" and not passive:
                    semantic_roles.append({"word": token.text, "role": "Patient"})
                elif token.rel == "obl:agent" and passive:
                    semantic_roles.append({"word": token.text, "role": "Agent"})
                elif token.rel == "obl":
                    if "Inst" in str(parsed.tag):
                        semantic_roles.append({"word": token.text, "role": "Instrument"})
                    elif "datv" in str(parsed.tag):
                        semantic_roles.append({"word": token.text, "role": "Recipient"})
                    elif "loct" in str(parsed.tag):
                        semantic_roles.append({"word": token.text, "role": "Location"})
                elif token.rel == "iobj":
                    semantic_roles.append({"word": token.text, "role": "Recipient"})

            # Связываем токены предложения с их семантикой
            sentence_tokens = []
            for token in sentence.tokens:
                for t in token_data:
                    if t["word"].lower() == token.text.lower():
                        sentence_tokens.append(t)
                        break

            syntax_data.append({
                "sentence": sentence.text,
                "dependencies": dependencies,
                "semantic_roles": semantic_roles,
                "tokens": sentence_tokens
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
                "semantics": token["semantics"],
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

    def get_semantics(self, doc_id):
        if doc_id < len(self.corpus):
            semantics = []
            for sent_data in self.corpus[doc_id]["syntax"]:
                semantic_entry = {
                    "sentence": sent_data["sentence"],
                    "semantic_roles": sent_data["semantic_roles"],
                    "conceptnet": [
                        {"word": token["word"], "lemma": token["lemma"], "relations": token["semantics"]}
                        for token in sent_data["tokens"]
                        if token["semantics"]
                    ]
                }
                semantics.append(semantic_entry)
            return semantics
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
            filetypes=[("Text files", "*.txt"), ("Word Documents", "*.doc *.docx"),
                       ("PDF files", "*.pdf"), ("RTF files", "*.rtf"), ("HTML files", "*.html")]
        )
        if not filepath:
            return
        try:
            if filepath.endswith('.txt'):
                text = corpus.read_txt(filepath)
            elif filepath.endswith(('.doc', '.docx')):
                text = corpus.read_doc(filepath)
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
        morph_box.delete(1.0, tk.END)
        for result in results:
            morph_box.insert(tk.END, f"Документ: {result['metadata']['title']}\n")
            morph_box.insert(tk.END, f"Слово: {result['word']} (Лемма: {result['lemma']})\n")
            morph_box.insert(tk.END, f"Часть речи: {result['pos']}\n")
            morph_box.insert(tk.END, f"Теги: {result['tags']}\n")
            morph_box.insert(tk.END, f"Контекст: {result['context']}\n\n")

    def show_stats():
        stats = corpus.get_statistics()
        morph_box.delete(1.0, tk.END)
        morph_box.insert(tk.END, "Топ-10 слов:\n")
        for word, freq in stats["word_freq"]:
            morph_box.insert(tk.END, f"{word}: {freq}\n")
        morph_box.insert(tk.END, "\nТоп-10 лемм:\n")
        for lemma, freq in stats["lemma_freq"]:
            morph_box.insert(tk.END, f"{lemma}: {freq}\n")
        morph_box.insert(tk.END, "\nЧасти речи:\n")
        for pos, freq in stats["pos_freq"]:
            morph_box.insert(tk.END, f"{pos}: {freq}\n")

    def show_syntax():
        syntax_box.delete(1.0, tk.END)
        for doc_id, doc in enumerate(corpus.corpus):
            syntax_box.insert(tk.END, f"Документ: {doc['metadata']['title']}\n")
            for sent_data in corpus.get_syntax(doc_id):
                syntax_box.insert(tk.END, f"Предложение: {sent_data['sentence']}\n")
                syntax_box.insert(tk.END, "Зависимости:\n")
                for word, head, rel in sent_data["dependencies"]:
                    syntax_box.insert(tk.END, f"  {word} -> {head} ({rel})\n")
                syntax_box.insert(tk.END, "\n")

    def show_semantics():
        semantics_box.delete(1.0, tk.END)
        for doc_id, doc in enumerate(corpus.corpus):
            semantics_box.insert(tk.END, f"Документ: {doc['metadata']['title']}\n")
            for sent_data in corpus.get_semantics(doc_id):
                semantics_box.insert(tk.END, f"Предложение: {sent_data['sentence']}\n")
                semantics_box.insert(tk.END, "Семантические роли:\n")
                if sent_data["semantic_roles"]:
                    for role in sent_data["semantic_roles"]:
                        semantics_box.insert(tk.END, f"  {role['word']}: {role['role']}\n")
                else:
                    semantics_box.insert(tk.END, "  Нет семантических ролей\n")
                semantics_box.insert(tk.END, "ConceptNet связи:\n")
                if sent_data["conceptnet"]:
                    for item in sent_data["conceptnet"]:
                        semantics_box.insert(tk.END, f"  Слово: {item['word']} (лемма: {item['lemma']})\n")
                        for rel in item["relations"]:
                            semantics_box.insert(tk.END, f"    {rel['relation']} -> {rel['target']} (вес: {rel['weight']})\n")
                else:
                    semantics_box.insert(tk.END, "  Нет данных ConceptNet\n")
                semantics_box.insert(tk.END, "\n")

    def edit_semantics():
        try:
            doc_id = int(doc_id_entry.get())
            sent_idx = int(sent_idx_entry.get())
            role_word = role_word_entry.get()
            role_type = role_type_entry.get()
            if doc_id < len(corpus.corpus) and sent_idx < len(corpus.corpus[doc_id]["syntax"]):
                corpus.corpus[doc_id]["syntax"][sent_idx]["semantic_roles"].append({
                    "word": role_word,
                    "role": role_type
                })
                messagebox.showinfo("Успех", "Роль добавлена")
                show_semantics()
            else:
                messagebox.showerror("Ошибка", "Неверный индекс документа или предложения")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения для ID")

    def edit_dependencies():
        try:
            doc_id = int(doc_id_entry.get())
            sent_idx = int(sent_idx_entry.get())
            word = role_word_entry.get()
            new_head = role_type_entry.get()
            new_rel = new_rel_entry.get()
            if doc_id < len(corpus.corpus) and sent_idx < len(corpus.corpus[doc_id]["syntax"]):
                sentence = corpus.corpus[doc_id]["syntax"][sent_idx]
                for dep in sentence["dependencies"]:
                    if dep[0] == word:
                        dep[1] = new_head
                        dep[2] = new_rel
                        break
                messagebox.showinfo("Успех", "Зависимость обновлена")
                show_syntax()
            else:
                messagebox.showerror("Ошибка", "Неверный индекс документа или предложения")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения для ID")

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
                        f.write("Семантические роли:\n")
                        for role in sent_data["semantic_roles"]:
                            f.write(f"  {role['word']}: {role['role']}\n")
                        f.write("\n")
            messagebox.showinfo("Успех", f"Результаты сохранены в {filepath}")

    def show_help():
        help_window = tk.Toplevel()
        help_window.title("Справка")
        tk.Label(help_window, text="Инструкция по использованию\n\n"
                                  "1. Загрузите текст через кнопку 'Загрузить текст'.\n"
                                  "2. Выполните поиск по слову или лемме на вкладке 'Морфология'.\n"
                                  "3. Просмотрите статистику, синтаксический или семантический анализ на соответствующих вкладках.\n"
                                  "4. Отредактируйте семантические роли или зависимости через форму.\n"
                                  "5. Сохраните корпус или экспортируйте результаты.").pack(padx=10, pady=10)
        tk.Button(help_window, text="Закрыть", command=help_window.destroy).pack()

    corpus = CorpusManager()

    root = tk.Tk()
    root.title("Семантико-синтаксический анализатор")
    root.geometry("1000x700")

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill='x')

    load_button = ttk.Button(frame, text="Загрузить текст", command=load_file)
    load_button.pack(side='left', padx=5)
    add_tooltip(load_button, "Загрузить текстовый файл (TXT, DOC, DOCX, PDF, RTF, HTML)")

    save_button = ttk.Button(frame, text="Сохранить корпус", command=save_corpus)
    save_button.pack(side='left', padx=5)
    add_tooltip(save_button, "Сохранить корпус в формате JSON")

    stats_button = ttk.Button(frame, text="Показать статистику", command=show_stats)
    stats_button.pack(side='left', padx=5)
    add_tooltip(stats_button, "Показать статистику по словам, леммам и частям речи")

    syntax_button = ttk.Button(frame, text="Показать синтаксис", command=show_syntax)
    syntax_button.pack(side='left', padx=5)
    add_tooltip(syntax_button, "Показать синтаксический анализ (зависимости)")

    semantics_button = ttk.Button(frame, text="Показать семантику", command=show_semantics)
    semantics_button.pack(side='left', padx=5)
    add_tooltip(semantics_button, "Показать семантические роли и связи ConceptNet")

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

    edit_frame = ttk.Frame(root)
    edit_frame.pack(padx=10, pady=5, fill='x')
    ttk.Label(edit_frame, text="Редактировать данные:").pack(side='left')
    ttk.Label(edit_frame, text="ID документа:").pack(side='left')
    doc_id_entry = ttk.Entry(edit_frame, width=5)
    doc_id_entry.pack(side='left', padx=5)
    ttk.Label(edit_frame, text="ID предложения:").pack(side='left')
    sent_idx_entry = ttk.Entry(edit_frame, width=5)
    sent_idx_entry.pack(side='left', padx=5)
    ttk.Label(edit_frame, text="Слово:").pack(side='left')
    role_word_entry = ttk.Entry(edit_frame, width=10)
    role_word_entry.pack(side='left', padx=5)
    ttk.Label(edit_frame, text="Роль/Голова:").pack(side='left')
    role_type_entry = ttk.Entry(edit_frame, width=10)
    role_type_entry.pack(side='left', padx=5)
    ttk.Label(edit_frame, text="Новая связь:").pack(side='left')
    new_rel_entry = ttk.Entry(edit_frame, width=10)
    new_rel_entry.pack(side='left', padx=5)
    ttk.Button(edit_frame, text="Добавить роль", command=edit_semantics).pack(side='left', padx=5)
    ttk.Button(edit_frame, text="Изменить зависимость", command=edit_dependencies).pack(side='left', padx=5)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)

    morph_frame = ttk.Frame(notebook)
    syntax_frame = ttk.Frame(notebook)
    semantics_frame = ttk.Frame(notebook)
    notebook.add(morph_frame, text="Морфология")
    notebook.add(syntax_frame, text="Синтаксис")
    notebook.add(semantics_frame, text="Семантика")

    morph_box = tk.Text(morph_frame, wrap='word')
    morph_box.pack(expand=True, fill='both')
    syntax_box = tk.Text(syntax_frame, wrap='word')
    syntax_box.pack(expand=True, fill='both')
    semantics_box = tk.Text(semantics_frame, wrap='word')
    semantics_box.pack(expand=True, fill='both')

    root.mainloop()

if __name__ == "__main__":
    launch_gui()