from flask import Flask, request, jsonify, render_template
import requests
import pyttsx3
import threading
import json

app = Flask(__name__)

engine = pyttsx3.init()
engine.setProperty("rate", 150)

API_TOKEN = "REMOVEDiMmsNuCPBoEualRpgnhCVtgHYblZFPEqcL"
QA_API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
QA_HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Load knowledge base from JSON file
with open("knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)["knowledge_base"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/answer', methods=['POST'])
def get_answer():
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"answer": "Please provide a valid question."})

    # Construct context based on question and knowledge base
    context_data = ""
    for item in knowledge_base:
        context_data += item["context"] + " "

    payload = {"inputs": {"question": question, "context": context_data}}
    try:
        response = requests.post(QA_API_URL, headers=QA_HEADERS, json=payload)
        output = response.json()
        answer = output.get("answer", "No answer found.")
        return jsonify({"answer": answer})
    except requests.exceptions.RequestException as e:
        return jsonify({"answer": f"API Error: {e}"})

speak_lock = threading.Lock()

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"success": False, "error": "No text provided"}), 400

    print(f"Speaking: {text}")

    def speak_text():
        with speak_lock:
            try:
                local_engine = pyttsx3.init()
                local_engine.say(text)
                local_engine.runAndWait()
                local_engine.stop()
            except Exception as e:
                print(f"Speech Error: {e}")

    thread = threading.Thread(target=speak_text)
    thread.start()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)