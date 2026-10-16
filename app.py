
from flask import Flask, render_template, request
import pickle
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient
from chatbot import get_chatbot_response

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Connect to MongoDB Atlas
mongo_uri = os.getenv("MONGODB_URI")
client = None
scan_history = None

if mongo_uri:
    client = MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=10000
    )
    database = client["fakejobdetector"]
    scan_history = database["scan_history"]
else:
    print("Warning: MONGODB_URI is missing.")

# Load the trained AI model
with open("job_model.pkl", "rb") as file:
    model = pickle.load(file)


def find_red_flags(job):
    flags = []
    text = job.lower()

    if "registration fee" in text or "pay money" in text:
        flags.append("The employer may be asking for money.")

    if "guaranteed job" in text or "guaranteed placement" in text:
        flags.append("A guaranteed job promise needs verification.")

    if "security deposit" in text:
        flags.append("A security deposit request needs careful checking.")

    if "no interview" in text:
        flags.append("The offer promises selection without an interview.")

    if "immediately" in text and ("pay" in text or "transfer" in text):
        flags.append("Urgent payment requests can be suspicious.")

    if not flags:
        flags.append(
            "No listed warning phrases were found. "
            "This does not prove the offer is safe."
        )

    return flags


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    job = request.form.get("job", "").strip()

    if not job:
        return "Please enter a job description.", 400

    result = str(model.predict([job])[0])
    flags = find_red_flags(job)

    if len(flags) >= 3:
        risk_level = "High"
    elif len(flags) == 2:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    saved_to_db = False

    if scan_history is not None:
        try:
            scan_history.insert_one({
                "job_description": job,
                "prediction": result,
                "risk_level": risk_level,
                "red_flags": flags,
                "created_at": datetime.now(timezone.utc)
            })
            saved_to_db = True
            print("Scan saved to MongoDB Atlas successfully.")

        except Exception as error:
            print("MongoDB save failed:", error)

    return render_template(
        "result.html",
        result=result,
        job=job,
        flags=flags,
        risk_level=risk_level,
        saved_to_db=saved_to_db
    )


@app.route("/chat", methods=["POST"])
def chat():
    message = request.form.get("message", "").strip()

    if not message:
        answer = "Please enter a question."
    else:
        answer = get_chatbot_response(message)

    return render_template(
        "index.html",
        chat_answer=answer,
        chat_message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
