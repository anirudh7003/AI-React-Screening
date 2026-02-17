import { useState } from "react";
import API from "../api";
import "../App.css";


function Feedback() {
  const [rating, setRating] = useState(1);
  const [comment, setComment] = useState("");

  const submitFeedback = async () => {
    const user_id = localStorage.getItem("user_id");

    try {
      const res = await API.post("/submit-feedback", {
        user_id,
        rating,
        comment
      });

      alert("Emotion detected: " + res.data.detected_emotion);
      setComment("");
    } catch {
      alert("Error submitting feedback");
    }
  };

  return (
    <div className="container">
      <div className="card">
          <h2>Submit Feedback</h2>
          <input type="number" min="1" max="5"
            value={rating}
            onChange={e => setRating(e.target.value)} />
          <br/>
          <textarea
            placeholder="Write your feedback"
            value={comment}
            onChange={e => setComment(e.target.value)}
          />
          <br/>
          <button onClick={submitFeedback}>Submit</button>
    </div>
    </div>
  );
}

export default Feedback;
