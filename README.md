# AI + React Emotion Feedback System

## Overview

This project is a full-stack web application developed as part of an AI + React screening assessment.

The system allows users to submit platform feedback, automatically detects the emotional sentiment of the feedback using a Machine Learning model, and provides an administrative dashboard to analyze user responses.

---

## Tech Stack

### Frontend
- React.js
- Axios
- React Router DOM

### Backend
- Flask (Python)
- SQLite Database
- REST API Architecture

### Machine Learning
- TF-IDF Vectorization
- Logistic Regression Classifier
- Scikit-learn
- Model persistence using Pickle

---

## Features

### User Module
- User Signup with validation
- Secure Login (password hashing)
- Feedback Submission (rating + comment)
- Real-time Emotion Detection via ML model

### Admin Module
- Static Admin Login (admin / admin123)
- View all user feedback
- Emotion-wise summary count
- Total feedback analytics

---

## Application Workflow

1. User registers an account
2. User logs in
3. User submits feedback
4. Backend processes feedback through trained ML model
5. Emotion label is stored in SQLite database
6. Admin dashboard displays feedback and emotion summary

---

## Machine Learning Pipeline

Emotion detection process:

