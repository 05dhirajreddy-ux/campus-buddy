from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, date
import os

app = Flask(__name__)

# Load data
with open("data.json", encoding="utf-8") as f:
    data = json.load(f)


def days_until(date_str):
    exam_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = date.today()
    return (exam_date - today).days


def get_nearest_exam():
    exams = data["exam"]
    subject = list(exams.keys())[0]
    date = exams[subject]
    return f"{subject} exam on {date}"

def get_attendance_risks():
    risks = [s for s in data["attendance"] if s["percentage"] < 75]
    return risks


def get_pending_assignments():
    pending = [a for a in data["assignments"] if not a["submitted"]]
    return pending


def get_best_study_slot():
    slots = data["free_slots"]
    return slots[0] if slots else None


def build_crash_plan(subject):
    plans = data.get("crash_plans", {})
    
    # normalize subject names
    mapping = {
        "dbms": "DBMS",
        "python": "Python",
        "cn": "CN"
    }
    
    key = mapping.get(subject.lower(), subject)

    return plans.get(key, f"Crash plan for '{subject}' not found.")

def process_query(query):
    query = query.lower()

    if "next exam" in query:
        return f"Your next exam is {get_nearest_exam()}"

    elif "attendance" in query:
        risks = get_attendance_risks()
        return f"You have {len(risks)} subjects at attendance risk."

    elif "dbms" in query:
        return build_crash_plan("DBMS")

    elif "python" in query:
        return build_crash_plan("Python")

    elif "cn" in query:
        return build_crash_plan("CN")

    else:
        return "Try asking about exams, attendance, DBMS, Python, or CN."
def index():
    nearest = get_nearest_exam()
    return render_template("index.html", nearest=nearest)

@app.route("/copilot", methods=["POST"])
def copilot():
    body = request.get_json()
    query = body.get("query", "")
    response = process_query(query)
    return jsonify(response)


@app.route("/dashboard-data")
def dashboard_data():
    nearest = get_nearest_exam()
    risks = get_attendance_risks()
    pending = get_pending_assignments()
    best_slot = get_best_study_slot()
    return jsonify({
        "nearest_exam": {"subject": nearest[0]["subject"], "days": nearest[1]} if nearest else None,
        "attendance_risks": len(risks),
        "pending_assignments": len(pending),
        "best_slot": best_slot
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
