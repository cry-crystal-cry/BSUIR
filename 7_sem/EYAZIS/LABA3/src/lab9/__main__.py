import os, re
from pathlib import Path
from itertools import product
from flask import Flask, render_template, request, send_from_directory
from lexer import RussianLexer, EnglishLexer
from index import Index
from abstractor import SentenceAbstractor, KeywordAbstractor
from openai import OpenAI
import sys
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Настройки
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
UPLOAD_DIR = DATA_DIR / 'uploads'
ABSTRACTS_DIR = DATA_DIR / 'abstracts'
ARTICLES_DIR = DATA_DIR / 'articles'
STOPWORDS_DIR = DATA_DIR / 'stopwords'

THEMES, LANGS = ['art', 'medicine'], ['ru', 'en']

# Инициализация OpenAI клиента
OPENAI_API_KEY = "SECRET"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "SECRET"
client = OpenAI(api_key=OPENAI_API_KEY)

for d in [UPLOAD_DIR, ABSTRACTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Глобальная инициализация индексов
lexers = {'ru': RussianLexer(), 'en': EnglishLexer()}
indexes = {l: {} for l in LANGS}

for l, th in product(LANGS, THEMES):
    sw_path = (STOPWORDS_DIR / l).with_suffix('.txt')
    sw = sw_path.read_text(encoding='utf-8').splitlines() if sw_path.exists() else []
    idx = Index(lexers[l], stopwords=sw)
    idx.add(*(ARTICLES_DIR/th/l).glob('*.txt'))
    idx.update_terms()
    indexes[l][th] = idx

LLM_SUMMARY_PROMPT = {
    'ru': "Напиши реферат ({} предложений) для текста: {}",
    'en': "Write a summary (around {} sentences) for the following text: {}"
}

LLM_KEYWORDS_PROMPT = {
    'ru': "Выдели {} ключевых слов через запятую для текста: {}",
    'en': "Extract {} keywords separated by commas for the following text: {}"
}

def detect_language(text):
    ru = sum(1 for c in text.lower() if 'а' <= c <= 'я')
    en = sum(1 for c in text.lower() if 'a' <= c <= 'z')
    return 'ru' if ru >= en else 'en'

@app.route('/')
def index_page():
    return render_template('index.html', themes=THEMES)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    method = request.form.get('method', 'statistical')
    theme = request.form.get('theme', THEMES[0])

    if not files or files[0].filename == '':
        return render_template('index.html', error="Файлы не выбраны", themes=THEMES)

    results = []
    for file in files:
        path = UPLOAD_DIR / re.sub(r'[^\w\.\-]', '_', file.filename)
        file.save(path)
        text = path.read_text(encoding='utf-8')
        lang = detect_language(text)

        try:
            if method == 'llm':
                if not OPENAI_API_KEY:
                    raise ValueError("Нет API ключа OpenAI")

                # Формируем промпты
                summary_prompt = LLM_SUMMARY_PROMPT[lang].format(5, text)
                keywords_prompt = LLM_KEYWORDS_PROMPT[lang].format(10, text)

                # Запрос к OpenAI для реферата
                summary_resp = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Ты реферируешь текст."},
                        {"role": "user", "content": summary_prompt}
                    ]
                )
                summary = summary_resp.choices[0].message.content

                # Запрос к OpenAI для ключевых слов
                keywords_resp = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Ты выделяешь ключевые слова."},
                        {"role": "user", "content": keywords_prompt}
                    ]
                )
                keywords = keywords_resp.choices[0].message.content

                # 🔧 Защита от проблем с кодировкой
                summary = summary.encode("utf-8", errors="ignore").decode("utf-8")
                keywords = keywords.encode("utf-8", errors="ignore").decode("utf-8")

            else:
                current_idx = indexes[lang][theme]
                sum_tool = SentenceAbstractor('russian' if lang == 'ru' else 'english', current_idx, n=5)
                key_tool = KeywordAbstractor(current_idx, k=10)
                summary, keywords = sum_tool.abstract(text), key_tool.abstract(text)

            abs_fn = f"abs_{path.name}"

            # Формируем итоговый текст
            output_text = (
                f"Language:\n{'Russian' if lang == 'ru' else 'English'}\n\n"
                f"Summary:\n{summary}\n\n"
                f"Keywords: {keywords}"
            )

            # Пишем как байты — исключаем любые ascii попытки
            with open(ABSTRACTS_DIR / abs_fn, 'wb') as f:
                f.write(output_text.encode('utf-8'))

            safe_summary = summary.encode('utf-8', errors='replace').decode('utf-8')
            safe_keywords = keywords.encode('utf-8', errors='replace').decode('utf-8')

            results.append({
                'filename': file.filename,
                'language': lang,
                'summary': safe_summary,
                'keywords': safe_keywords,
                'download': abs_fn
            })


        except Exception as e:
            results.append({'filename': file.filename, 'error': str(e)})

    return render_template('index.html', results=results, themes=THEMES)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(ABSTRACTS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
