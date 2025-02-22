import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from src.KOGI.rag import KOGI_FAQ
from src.OSUN.rag import OSUN_FAQ
import openai
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Load OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS for all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class UserQuery(BaseModel):
    user_id: str
    prompt: str


# Initialize Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# Initialize Chatbot
kogifQ = KOGI_FAQ(embeddings)
osunfQ = OSUN_FAQ(embeddings)


@app.get("/")
async def read_root():
    return {"API": "FAQ"}


@app.post("/Osun_FAQ")
async def faq(question: UserQuery):
    try:
        res = osunfQ.chat_function(message=question.prompt, user_id=question.user_id)
        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/Kogi_FAQ")
async def faq(question: UserQuery):
    try:
        res = kogifQ.chat_function(message=question.prompt, user_id=question.user_id)
        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
