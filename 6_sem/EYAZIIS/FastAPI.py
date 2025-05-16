from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import uuid
import os
from database import log_message, get_chat_history, delete_message, add_document, delete_document
from RAG import process_query, index_document, delete_document_chunks

app = FastAPI()


class ChatRequest(BaseModel):
    question: str
    session_id: str
    model: str

@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    history = get_chat_history(session_id)
    response = process_query(request.question, history, session_id)
    print(f"Response from process_query: {response}")
    message_id = log_message(session_id, request.question, response, request.model)
    result = {"answer": response, "session_id": session_id, "message_id": message_id, "model": request.model}
    print(f"Returning: {result}")
    return result
UploadFile
@app.post("/upload")
async def upload_file(file:  = File(...)):
    os.makedirs("uploads", exist_ok=True)
    filepath = os.path.join("uploads", file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())
    doc_id = add_document(file.filename)
    index_document(filepath, doc_id)
    return {"doc_id": doc_id, "filename": file.filename}

@app.delete("/remove_message/{message_id}")
async def remove_message(message_id: int):
    delete_message(message_id)
    return {"status": "success"}

@app.delete("/remove_document/{doc_id}")
async def remove_document(doc_id: int):
    delete_document_chunks(doc_id)
    delete_document(doc_id)
    return {"status": "success"}
