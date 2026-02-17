import { useState } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";
import "../App.css";


function Signup() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("/signup", form);
      alert("Signup successful");
      navigate("/");
    } catch (err) {
      alert("Error signing up");
    }
  };

  return (
   <div className="container">
      <div className="card">
        <h2>Signup</h2>
        <form onSubmit={handleSubmit}>
          <input placeholder="Name"
            onChange={e => setForm({...form, name: e.target.value})} />
          <input placeholder="Email"
            onChange={e => setForm({...form, email: e.target.value})} />
          <input type="password" placeholder="Password"
            onChange={e => setForm({...form, password: e.target.value})} />
          <button type="submit">Register</button>
        </form>
    </div>
    </div>
  );
}

export default Signup;
