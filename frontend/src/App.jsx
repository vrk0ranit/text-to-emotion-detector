import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const emojiMap = {
  joy: "😊",
  sadness: "😢",
  anger: "😡",
  fear: "😨",
  surprise: "😲",
  disgust: "🤢",
  neutral: "😐",
  love: "😍",
};

function App() {
  const [text, setText] = useState("");
  const [emotion, setEmotion] = useState("");
  const [emoji, setEmoji] = useState("");
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", { text });
      const label = res.data.label.toLowerCase();
      setEmotion(label);
      setEmoji(emojiMap[label] || "🙂");
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">🧠 Emotion Detector</h1>
        <p className="subtitle">
          Type anything below to detect the emotional tone of your text.
        </p>

        <textarea
          placeholder="Type your thoughts here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={handlePredict} disabled={loading}>
          {loading ? "Analyzing..." : "Detect Emotion"}
        </button>

        {emotion && (
          <div className="result">
            <span className="emoji">{emoji}</span>
            <p className="emotion-text">{emotion.toUpperCase()}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
