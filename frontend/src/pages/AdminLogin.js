import { useState } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";
import "../App.css";


function AdminLogin() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("/admin-login", form);
      navigate("/admin-dashboard");
    } catch {
      alert("Invalid admin login");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Admin Login</h2>
        <form onSubmit={handleSubmit}>
          <input placeholder="Username"
            onChange={e => setForm({...form, username: e.target.value})} />
          <input type="password" placeholder="Password"
            onChange={e => setForm({...form, password: e.target.value})} />
          <button type="submit">Login</button>
        </form>
    </div>
    </div>
  );
}

export default AdminLogin;
