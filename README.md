✨ A&D VAULT — One Platform. Endless Tools.

A&D VAULT is a unified desktop utility hub that brings together Productivity Tools, Professional AI Tools, PDF Utilities, Gaming Tools, and Conversion Tools into one clean, modern dashboard.
It provides a web-styled interface (HTML/CSS/JS) powered by a Python Flask backend that launches your Python scripts—including Tkinter apps and Streamlit applications—with a single click.

🚀 Features
✅ Unified Dashboard

Modern card-based UI

Tool categories for easy navigation

Icons for each tool

Responsive layout

One-click tool launching

✅ Supports All Types of Python Tools

Tkinter GUI applications

Streamlit apps (Cognitive Resume Analyzer – CVSense)

PDF utilities

Productivity utilities

Simple games

Math & conversion tools

✅ Smart Execution System

Automatically chooses the correct interpreter

Supports virtual environments (e.g., .venv for CVSense)

Tools launch without blocking the dashboard

Backend handles environment isolation

🧠 Project Architecture
Frontend

HTML5

CSS3 (responsive grid + cards)

JavaScript (dynamic rendering + API requests)

Backend

Python Flask API

Subprocess tool launcher

Environment-aware execution

Tool Layer

Tkinter tools

Streamlit AI tool

Utility scripts

🛠️ Tools Included
💼 Professional Tools

CVSense — AI Resume Analyzer
Extracts PDF text, computes ATS similarity score, and generates AI-recommended resume improvements.

📄 PDF Tools

PDF Merger — Combine PDFs

PDF Converter — PDF ⇄ DOCX

🔧 Productivity Tools

WPM Typing Test

To-Do List

Alarm Clock

Password Generator

🎮 Gaming Tools

Rock-Paper-Scissors

Coin Toss

Guess the Number

Roulette / Choice Picker

🔢 Conversion Tools

Unit Converter

BMI Calculator

Basic Calculator

🔌 How It Works

User clicks OPEN on a tool card.

JavaScript sends a request to:

/run-tool


Flask decides:

Use system Python?

Use .venv Python?

Is it a Streamlit app?

Flask launches the script via subprocess.Popen()

Your tool opens (Tkinter window or Streamlit browser app).

Dashboard stays active.

🏗️ Installation
1️⃣ Clone the repository
git clone https://github.com/Aahna-Sharma/A-DVault.git

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Start the Flask backend
python server.py

4️⃣ Start the dashboard

Option A — Python server:

python -m http.server 8000


Open:

http://localhost:8000


Option B — VS Code Live Server
Just right-click → Open with Live Server

🔒 Security

Fully offline

No data stored or uploaded

Sensitive keys stored in .env

Backend only runs predefined scripts

🚀 Future Enhancements

Dark mode

Mobile-responsive UI

Cloud-based execution

More AI tools

User login system

Favorites and search bar

PDF Split/Compress

Desktop app version

