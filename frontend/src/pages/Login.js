import { useState } from "react";
import API from "../api";
import { useNavigate, Link } from "react-router-dom";
import "../App.css";

function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post("/signin", form);
      localStorage.setItem("user_id", res.data.user_id);
      navigate("/feedback");
    } catch {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>User Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            placeholder="Email"
            onChange={e => setForm({...form, email: e.target.value})}
          />
          <input
            type="password"
            placeholder="Password"
            onChange={e => setForm({...form, password: e.target.value})}
          />
          <button type="submit">Login</button>
        </form>

        <Link to="/signup" className="link">Create Account</Link>
        <Link to="/admin" className="link">Admin Login</Link>
      </div>
    </div>
  );
}

export default Login;
