import os
import json
from collections import defaultdict
import docx
import pymorphy2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Инициализация морфоанализатора
morph = pymorphy2.MorphAnalyzer()

# Словарь перевода морфологических тегов на русский язык
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
    'impr': 'повелительное наклонение'
}

class DictionaryGenerator:
    def __init__(self):
        self.dictionary = defaultdict(lambda: {
            "основа": "",
            "часть_речи": "",
            "окончания": []
        })

    def read_docx(self, filepath):
        doc = docx.Document(filepath)
        return " ".join([para.text for para in doc.paragraphs])

    def tokenize_text(self, text):
        return [word.strip('.,!"«»:;()') for word in text.split() if word.isalpha()]

    def translate_tags(self, tag_str):
        return ', '.join([TAG_TRANSLATIONS.get(part, part) for part in str(tag_str).split(',')])

    def analyze_tokens(self, tokens):
        for word in tokens:
            parsed = morph.parse(word)[0]
            normal_form = parsed.normal_form
            ending = parsed.word[len(parsed.normal_form):] if parsed.word.startswith(parsed.normal_form) else ""
            record = self.dictionary[normal_form]
            record["основа"] = normal_form
            record["часть_речи"] = TAG_TRANSLATIONS.get(str(parsed.tag.POS), str(parsed.tag.POS))
            record["окончания"].append({
                "окончание": ending,
                "морфология": self.translate_tags(parsed.tag)
            })

    def get_summary(self):
        summary = []
        for lexeme, data in sorted(self.dictionary.items()):
            entry = f"Лексема: {lexeme}\n  Основа: {data['основа']}\n  Часть речи: {data['часть_речи']}\n  Окончания:"
            for ending in data["окончания"]:
                entry += f"\n    - {ending['окончание']} ({ending['морфология']})"
            summary.append(entry)
        return summary

    def save_dictionary(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.dictionary, f, ensure_ascii=False, indent=2)
        return f"Словарь сохранён в {path}"

def launch_gui():
    def load_file():
        filepath = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if not filepath:
            return
        try:
            text = gen.read_docx(filepath)
            tokens = gen.tokenize_text(text)
            gen.analyze_tokens(tokens)
            summary = gen.get_summary()
            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, "\n\n".join(summary))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def save_file():
        filepath = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")])
        if filepath:
            result = gen.save_dictionary(filepath)
            messagebox.showinfo("Успех", result)

    gen = DictionaryGenerator()

    root = tk.Tk()
    root.title("Словарь русского языка")
    root.geometry("800x600")

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill='x')

    ttk.Button(frame, text="Загрузить DOCX", command=load_file).pack(side='left', padx=5)
    ttk.Button(frame, text="Сохранить JSON", command=save_file).pack(side='left', padx=5)

    output_box = tk.Text(root, wrap='word')
    output_box.pack(expand=True, fill='both', padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
