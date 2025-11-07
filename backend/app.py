import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow React frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # later: ["https://your-vercel-site.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face model endpoint + token (set HF_TOKEN in Render → Environment)
HF_API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
HF_TOKEN = os.environ.get("HF_TOKEN")

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Emotion Detector API is live via Hugging Face 🚀"}

@app.post("/predict")
def predict_emotion(input: TextInput):
    if not HF_TOKEN:
        return {"error": "Missing HF_TOKEN environment variable"}

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    resp = requests.post(HF_API_URL, headers=headers, json={"inputs": input.text})
    data = resp.json()

    if isinstance(data, dict) and "error" in data:
        return {"error": data["error"]}

    top = max(data[0], key=lambda x: x["score"])
    return {"label": top["label"], "score": round(top["score"], 3)}

# Correct port binding for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
