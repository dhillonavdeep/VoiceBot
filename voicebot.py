import requests
import speech_recognition as sr
import pyttsx3
import keyboard
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Hugging Face API Configuration
API_TOKEN = os.getenv("HUGGINGFACE_TOKEN")  # Replace with your actual API token
QA_API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
QA_HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Knowledge Base (Context)
context_data = """
    {
        "context": "Navdeep, an enthusiastic individual with a solid background in Programming and Data Science. He is committed to applying technical expertise, driving innovation, and contributing to the success of projects and initiatives.",
        "label": "NAME"
    },
    {
        "context": "Navdeep's Summary: Navdeep is an enthusiastic individual with a solid background in Programming and Data Science. He is committed to applying technical expertise, driving innovation, and contributing to the success of projects and initiatives.",
        "label": "Summary"
    },
    {
        "context": "Navdeep's Work Experience: Navdeep worked as a Software Developer intern at Qanalyx Technocrats Private Limited from May 3, 2022, to August 1, 2022. During this time, he collaborated on software projects, aided in feature design and implementation, maintained code integrity using version control and best coding practices, and assisted seniors in the design and implementation of features and functionality.",
        "label": "Work Experience"
    },
    {
        "context": "Navdeep's Education: Navdeep holds a BSc in Programming and Data Science from the Indian Institute of Technology, Madras (2020-2024), with a specialization in Data Science and programming. He also has a specialization in Information Technology from Guru Jambheshwar University of Science and Technology.",
        "label": "Education"
    },
    {
        "context": "Navdeep's Projects: Navdeep developed a Movie Sentiment Prediction project using Scikit-learn, Pandas, NumPy, TF-IDF, and word embeddings. He also enhanced the Seek Portal with Generative AI features using Gemma:2b, Flask, HTML, Jinja, and JavaScript. Additionally, he created a full-stack music application with Flask backend, Vue.js frontend, Celery, Redis, SMTP, Bootstrap, Jinja2, Flask-SQLAlchemy, and SQLite. Other projects include a Ticket Booking System and a Sales and Inventory Management System.",
        "label": "Projects"
    },
    {
        "context": "Navdeep's Skills: Java, Python, Scikit-learn, Machine Learning, Deep Learning, NLP, Bash, Vue.js, HTML, CSS, SQL, SQLite, Flask, Data Structures & Algorithms, Linux.",
        "label": "Skills"
    },
    {
        "context": "Navdeep's Location: Navdeep studied at the Indian Institute of Technology, Madras.",
        "label": "Location"
    },
    {
        "context": "Navdeep's Graduation Year: Navdeep graduated from the Indian Institute of Technology, Madras in 2024.",
        "label": "Graduation Year"
    },
    {
        "context": "Navdeep's Internship Duration: Navdeep's internship at Qanalyx Technocrats Private Limited lasted from May 3, 2022, to August 1, 2022.",
        "label": "Internship Duration"
    },
    {
        "context": "Navdeep's AI tools: Navdeep used Gemma:2b model for lecture-based Q&A and coding hints in the Seek Portal project.",
        "label": "AI tools"
    },
    {
        "context": "Navdeep's Database Skills: Navdeep used Flask-SQLAlchemy and SQLite for database management in the Music Application project.",
        "label": "Database Skills"
    },
    {
        "context": "Navdeep's Backend Tools: Navdeep used Flask for backend development.",
        "label": "Backend Tools"
    },
    {
        "context": "Navdeep's Frontend Tools: Navdeep used Vue.js for frontend development.",
        "label": "Frontend Tools"
    },
    {
        "context": "Navdeep's Life Story: Navdeep is from Charkhi Dadri, completed schooling there, and pursued two degrees simultaneously—BSc in Programming and Data Science and BTech in Information Technology.",
        "label": "Life Story"
    },
    {
        "context": "Navdeep's Superpower: A sharp mind with strong thinking abilities.",
        "label": "Superpower"
    },
    {
        "context": "Navdeep's Top 3 Growth Areas: AI & ML, work ethic, and physical health.",
        "label": "Top 3 Growth Areas"
    },
    {
        "context": "Navdeep's Misconception: Colleagues often think Navdeep is always serious about work.",
        "label": "Misconception"
    },
    {
        "context": "Navdeep's Pushing Boundaries: Driven by the fear of remaining average.",
        "label": "Pushing Boundaries"
    }
"""


# Speech Recognition
def listen():
    """ Starts listening when spacebar is pressed and stops immediately when it's released. """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nPress and hold SPACE to start speaking...")
        
        # Wait for space to be pressed
        keyboard.wait("space")
        print("🎤 Listening... Speak now.")

        recognizer.adjust_for_ambient_noise(source)

        # Start recording
        audio = recognizer.listen(source, phrase_time_limit=5)  # Limit each input to 5 seconds

        # Stop immediately when space is released
        while keyboard.is_pressed("space"):
            pass  # Do nothing while space is held

        print("🛑 Stopped recording.")

        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣 You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Speech service is unavailable."

# Get Answer from Question Answering Model
def get_answer(question, context):
    payload = {
        "inputs": {
            "question": question,
            "context": context,
        }
    }
    try:
        output = requests.post(QA_API_URL, headers=QA_HEADERS, json=payload).json()
        # print("Raw API Response:", output) #print the whole output.
        return output["answer"]
    except KeyError:
        return "Sorry, I could not find an answer."
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return "Sorry, there was an error processing your request."

# Text to Speech
def speak(text):
    """ Converts text to speech and speaks the response. """
    engine.say(text)
    engine.runAndWait()

# Main Function
def main():
    """ Runs the voice bot loop using the Question Answering model. """
    while True:
        user_question = listen()
        
        if user_question.lower() in ["exit", "quit", "stop"]:
            print("👋 Exiting...")
            speak("Goodbye!")
            break
        
        ai_answer = get_answer(user_question, context_data)
        print(f"🤖 AI: {ai_answer}")
        speak(ai_answer)

# Run the bot
if __name__ == "__main__":
    main()