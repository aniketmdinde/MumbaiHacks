from flask import Blueprint, redirect, url_for, session, render_template, request, jsonify
import requests

views = Blueprint('views', __name__)

def format_bot_response(response_text):
    # Add <br> after each colon
    formatted_text = response_text.replace(":", ":<br>")
    # Add <br> after each comma
    formatted_text = formatted_text.replace(",", ",<br>")
    return formatted_text


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

    # question = request.form.get('question') or request.json.get('question')

    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question not provided"}), 400


    csv_file_path = './uploads/mutual_funds_data.csv'

    
    payload = {
        "question": question,
        "csv_file_path": csv_file_path
    }

    response = requests.post(
        "http://127.0.0.1:8000/ask-question",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": "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"
        },
        json=payload
    )

    # bot_response = response.json()
    # return render_template("main.html", bot_response=bot_response)

    bot_response = response.json().get("answer", "No response received")

    bot_response = format_bot_response(bot_response)

    # Return JSON response for frontend to display
    return jsonify({"answer": bot_response})


# curl -X POST "http://127.0.0.1:8000/ask-question/" -H "Content-Type: application/json" -H "X-API-Key: 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" -d "{\"question\": \"What are the best mutual funds for long-term investment?\", \"csv_file_path\": \"./uploads/mutual_funds_data.csv\"}"
