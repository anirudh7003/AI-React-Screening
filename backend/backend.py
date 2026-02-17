import sqlite3
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = "database.db"

# Load ML model
with open("emotion_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# -----------------------
# Database Initialization
# -----------------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            rating INTEGER,
            comment TEXT,
            emotion TEXT,
            timestamp TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

init_db()


# -----------------------
# Helper
# -----------------------

def predict_emotion(text):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)
    return prediction[0]


# -----------------------
# 1. SIGNUP
# -----------------------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400


# -----------------------
# 2. SIGNIN
# -----------------------

@app.route("/signin", methods=["POST"])
def signin():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        return jsonify({"message": "Login successful", "user_id": user[0]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# -----------------------
# 3. SUBMIT FEEDBACK
# -----------------------

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    data = request.json
    user_id = data.get("user_id")
    rating = data.get("rating")
    comment = data.get("comment")

    if not user_id or not comment:
        return jsonify({"error": "Missing fields"}), 400

    emotion = predict_emotion(comment)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (user_id, rating, comment, emotion, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, rating, comment, emotion, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

    return jsonify({"message": "Feedback submitted", "detected_emotion": emotion})


# -----------------------
# 4. ADMIN LOGIN
# -----------------------

@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin123":
        return jsonify({"message": "Admin login successful"})
    else:
        return jsonify({"error": "Invalid admin credentials"}), 401


# -----------------------
# 5. ADMIN DASHBOARD
# -----------------------

@app.route("/admin-dashboard", methods=["GET"])
def admin_dashboard():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.name, users.email, feedback.rating,
               feedback.comment, feedback.emotion, feedback.timestamp
        FROM feedback
        JOIN users ON feedback.user_id = users.id
        ORDER BY feedback.timestamp DESC
    """)

    rows = cursor.fetchall()

    feedback_list = []
    emotion_summary = {}

    for row in rows:
        feedback_data = {
            "name": row[0],
            "email": row[1],
            "rating": row[2],
            "comment": row[3],
            "emotion": row[4],
            "timestamp": row[5]
        }
        feedback_list.append(feedback_data)

        emotion_summary[row[4]] = emotion_summary.get(row[4], 0) + 1

    conn.close()

    return jsonify({
        "total_feedback": len(feedback_list),
        "emotion_summary": emotion_summary,
        "feedback": feedback_list
    })


# -----------------------
# Run Server
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)
