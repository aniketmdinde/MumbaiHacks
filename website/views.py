from flask import Blueprint, redirect, url_for, session, render_template, request, jsonify
import requests

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.signup'))
    
    return render_template("chat.html")

@views.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@views.route('/ask-question', methods=['GET','POST'])
def ask_question():

    question = request.form.get('question')

    # question = 'What are the best mutual funds for long-term investment?'
    csv_file_path = './uploads/mutual_funds_data.csv'
    # Load the CSV file
    
    payload = {
        "question": question,
        "csv_file_path": csv_file_path
    }

    # Send the request to the Ollama model
    response = requests.post(
        "http://0.0.0.0:8000/ask-question/",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": "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"
        },
        json=payload
    )

    # Return the response from the Ollama model
    return jsonify(response.json()), response.status_code

# curl -X POST "http://127.0.0.1:8000/ask-question/" -H "Content-Type: application/json" -H "X-API-Key: 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" -d "{\"question\": \"What are the best mutual funds for long-term investment?\", \"csv_file_path\": \"./uploads/mutual_funds_data.csv\"}"
