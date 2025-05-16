from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
import pypdf
import docx2txt
from langchain.text_splitter import RecursiveCharacterTextSplitter

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(collection_name="sport_docs", embedding_function=embedding_function,
                     persist_directory="L:\projects\BSUIR\\6_sem\EYAZIIS")


def process_query(question, chat_history, session_id):
    chain = create_rag_chain()
    print(f"Вопрос: {question}, История: {chat_history}")  # Отладка
    response = chain.invoke({"question": question, "chat_history": chat_history})
    print(f"Ответ: {response}")  # Отладка
    if "вне темы" in response.lower():
        response = "Извините, я могу отвечать только на вопросы, связанные со спортом."
    return response

def index_document(filepath, doc_id):
    if filepath.endswith('.pdf'):
        with open(filepath, 'rb') as f:
            pdf = pypdf.PdfReader(f)
            text = "".join([page.extract_text() or "" for page in pdf.pages])
    elif filepath.endswith('.docx'):
        text = docx2txt.process(filepath)
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    vectorstore.add_texts(texts=chunks, metadatas=[{"doc_id": doc_id} for _ in chunks])


def delete_document_chunks(doc_id):
    vectorstore.delete(metadata={"doc_id": str(doc_id)})


def create_rag_chain():
    llm = Ollama(model="llama3.2", base_url="http://127.0.0.1:11434")
    prompt = ChatPromptTemplate.from_template(
        """Вы - ассистент по спортивной тематике. Ответьте на вопрос, используя только предоставленные документы. Если вопрос вне темы спорта, вежливо откажитесь отвечать. Контекст: {context}\nИстория: {chat_history}\nВопрос: {question}\nОтвет:"""
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Explicitly extract the question for the retriever
    chain = (
            {
                "context": (lambda x: x["question"]) | retriever | format_docs,  # Pass only the question to retriever
                "question": lambda x: x["question"],
                "chat_history": lambda x: x["chat_history"]
            }
            | prompt
            | llm
            | StrOutputParser()
    )
    return chain




