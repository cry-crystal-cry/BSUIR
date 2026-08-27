import os
import re
import requests
import json
from pathlib import Path

WIT_SERVER_TOKEN = "EJ452T5JCCUFLERFU4IUJO3VTJVH7GKV"
API_URL = "https://api.wit.ai/utterances"

DIRECTORY_PATH = "concept"

INTENT = "about_entity"
ENTITY = "rrel_entity:rrel_entity"


def extract_entities_from_scs(file_path):
    """
    Извлекает все сущности из SCS файла по шаблону nrel_main_idtf: [сущность]
    Возвращает список сущностей
    """
    entities = []
    pattern = r'=> nrel_main_idtf:\s*\[([^\]]+)\]'

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            matches = re.findall(pattern, content)
            entities.extend(matches)
    except Exception as e:
        print(f"Ошибка чтения файла {file_path}: {e}")

    return entities


def generate_question(entity):
    """
    Формирует вопрос из сущности
    """
    return f"Что такое {entity}?"


def extract_entity_from_question(text):
    """
    Выводит сущность — слово/фразу после 'Что такое ...'
    """
    m = re.search(r"Что такое\s+(.+)[\?\.]?$", text, re.IGNORECASE)
    if not m:
        return None

    raw_entity = m.group(1)
    clean_entity = re.sub(r"[\?\.]+$", "", raw_entity).strip()
    return clean_entity


def send_utterance(text):
    entity_value = extract_entity_from_question(text)
    if not entity_value:
        print(f"SKIP (не удалось извлечь) → {text}")
        return None

    start_pos = text.lower().find(entity_value.lower())

    if start_pos == -1:
        print(f"SKIP (сущность не найдена в строке) → {text}")
        return None

    end_pos = start_pos + len(entity_value)
    body_text = text[start_pos:end_pos]

    payload = [{
        "text": text,
        "intent": INTENT,
        "entities": [
            {
                "entity": ENTITY,
                "start": start_pos,
                "end": end_pos,
                "body": body_text,
                "entities": []
            }
        ],
        "traits": []
    }]

    headers = {
        "Authorization": f"Bearer {WIT_SERVER_TOKEN}",
    }

    return requests.post(API_URL, headers=headers, json=payload)


def process_directory(directory_path):
    """
    Обрабатывает все SCS файлы в директории и отправляет вопросы в Wit.ai
    """
    directory = Path(directory_path)

    if not directory.exists() or not directory.is_dir():
        print(f"Директория {directory_path} не существует или не является директорией")
        return

    # Находим все файлы с расширением .scs
    scs_files = list(directory.glob("**/*.scs"))

    if not scs_files:
        print(f"Файлы с расширением .scs не найдены в директории {directory_path}")
        return

    print(f"Найдено {len(scs_files)} SCS файлов")

    all_questions = []

    # Извлекаем сущности из всех файлов
    for scs_file in scs_files:
        entities = extract_entities_from_scs(scs_file)
        if entities:
            print(f"Файл: {scs_file.name} - найдено сущностей: {len(entities)}")
            for entity in entities:
                question = generate_question(entity.strip())
                all_questions.append(question)

    if not all_questions:
        print("Не найдено сущностей для обработки")
        return

    print(f"\nВсего сформировано вопросов: {len(all_questions)}\n")

    # Отправляем вопросы в Wit.ai
    for i, question in enumerate(all_questions, 1):
        print(f"Отправка вопроса {i}/{len(all_questions)}: {question}")

        res = send_utterance(question)

        if res is None:
            continue

        if res.status_code == 200:
            print(f"✓ Успешно отправлено → {question}")
        else:
            print(f"✗ ОШИБКА {res.status_code} → {question}")
            try:
                error_json = res.json()
                print(f"   Ответ сервера: {json.dumps(error_json, ensure_ascii=False)}")
            except:
                print(f"   Текст ответа: {res.text}")
        print()


def main():
    """
    Основная функция
    """
    process_directory(DIRECTORY_PATH)


if __name__ == "__main__":
    main()