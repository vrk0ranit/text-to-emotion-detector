import os
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later to your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input model
class TextInput(BaseModel):
    text: str

# Load lightweight emotion classification model (smaller + faster)
@app.on_event("startup")
def load_model():
    global emotion_classifier
    # Use a smaller model that fits into Render free tier memory
    emotion_classifier = pipeline(
        "text-classification",
        model="bhadresh-savani/distilbert-base-uncased-emotion",
        return_all_scores=False,
    )

@app.get("/")
def home():
    return {"message": "Emotion Detector API is running 🚀"}

@app.post("/predict")
def predict_emotion(input: TextInput):
    result = emotion_classifier(input.text)[0]
    return {"label": result["label"], "score": round(result["score"], 3)}

# ✅ Use Render’s dynamic port to avoid “No open ports detected” error
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
