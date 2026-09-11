import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google import genai

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize Gemini Client (set your API key in environment variables)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
client = genai.Client(api_key=GEMINI_API_KEY)

# Start a chat session
chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "system_instruction": (
            "You are JARVIS, a highly intelligent voice assistant. "
            "Keep answers concise, conversational, and direct, suitable for text-to-speech."
        )
    }
)

class QueryRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_endpoint(data: QueryRequest):
    try:
        response = chat.send_message(data.prompt)
        return JSONResponse({"reply": response.text})
    except Exception as e:
        return JSONResponse({"reply": f"An error occurred: {str(e)}"}, status_code=500)