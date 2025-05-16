import streamlit as st
import requests
import uuid
from database import init_db, get_sessions, get_chat_history  # Добавлен импорт get_chat_history

st.set_page_config(page_title="Диалоговый ассистент (Спорт)", layout="wide")
st.title("Диалоговый ассистент (Спорт)")

init_db()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "model" not in st.session_state:
    st.session_state.model = "llama3.2"

with st.sidebar:
    st.header("Настройки")
    st.session_state.model = st.selectbox("Выберите модель", ["llama3.2"])
    uploaded_file = st.file_uploader("Загрузить документ", type=["pdf", "docx", "txt"])
    if uploaded_file:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post("http://localhost:8000/upload", files=files)
        if response.status_code == 200:
            st.success(f"Документ {uploaded_file.name} загружен!")
        else:
            st.error(f"Ошибка загрузки: {response.status_code} - {response.text}")

    if st.button("Новая сессия"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    sessions = get_sessions()
    selected_session = st.selectbox("Выбрать сессию", ["Новая"] + sessions)
    if selected_session != "Новая" and selected_session != st.session_state.session_id:
        st.session_state.session_id = selected_session
        history = get_chat_history(selected_session)  # Теперь функция доступна
        st.session_state.messages = history
        st.rerun()

    if st.button("Справка"):
        st.write("""
        **Инструкция:**
        1. Введите запрос в поле ниже и нажмите "Отправить".
        2. Загружайте документы для расширения базы знаний.
        3. Используйте "Новая сессия" для начала нового диалога.
        4. Выберите сессию для просмотра истории.
        5. Нажмите "Удалить" для удаления сообщений ассистента.
        """)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "message_id" in message:
            if st.button("Удалить", key=f"delete_{message['message_id']}"):
                response = requests.delete(f"http://localhost:8000/remove_message/{message['message_id']}")
                if response.status_code == 200:
                    st.session_state.messages = [m for m in st.session_state.messages if
                                                 m.get("message_id") != message["message_id"]]
                    st.rerun()

prompt = st.chat_input("Введите ваш запрос...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post("http://localhost:8000/chat", json={
        "question": prompt,
        "session_id": st.session_state.session_id,
        "model": st.session_state.model
    })
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", "Ошибка: нет ответа от сервера")
        message_id = data.get("message_id", str(uuid.uuid4()))
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "message_id": message_id
        })
        with st.chat_message("assistant"):
            st.markdown(answer)
    else:
        st.error(f"Ошибка: {response.status_code} - {response.text}")

if st.button("Очистить чат"):
    st.session_state.messages = []
    st.rerun()