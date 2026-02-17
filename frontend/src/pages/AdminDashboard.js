import { useEffect, useState } from "react";
import API from "../api";
import "../App.css";


function AdminDashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    API.get("/admin-dashboard")
      .then(res => setData(res.data));
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div style={{ padding: "40px" }}>
      <h2 style={{ textAlign: "center" }}>Admin Dashboard</h2>
      <h3>Total Feedback: {data.total_feedback}</h3>

      <h3>Emotion Summary:</h3>
      <ul>
        {Object.entries(data.emotion_summary).map(([emotion, count]) => (
          <li key={emotion}>{emotion}: {count}</li>
        ))}
      </ul>

      <h3>All Feedback:</h3>
      <table border="1">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Rating</th>
            <th>Comment</th>
            <th>Emotion</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {data.feedback.map((f, index) => (
            <tr key={index}>
              <td>{f.name}</td>
              <td>{f.email}</td>
              <td>{f.rating}</td>
              <td>{f.comment}</td>
              <td>{f.emotion}</td>
              <td>{f.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminDashboard;
