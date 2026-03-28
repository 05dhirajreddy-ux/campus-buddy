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
    key = subject.lower().replace(" ", "_")
    return plans.get(key, None)


def process_query(query):
    q = query.lower().strip()

    # Exam queries
    if any(word in q for word in ["exam", "test", "when is", "schedule", "upcoming"]):
        nearest = get_nearest_exam()
        if not nearest:
            return {"type": "exam", "message": "No upcoming exam found! You're all clear. 🎉"}
        exam, days = nearest
        all_upcoming = [(e, days_until(e["date"])) for e in data["exam"] if days_until(e["date"]) >= 0]
        all_upcoming.sort(key=lambda x: x[1])
        exam_list = []
        for e, d in all_upcoming[:4]:
            exam_list.append({
                "subject": e["subject"],
                "date": e["date"],
                "days": d,
                "type": e.get("type", "Exam"),
                "syllabus": e.get("syllabus", [])
            })
        warning = days <= 3
        return {
            "type": "exam",
            "nearest": {"subject": exam["subject"], "date": exam["date"], "days": days},
            "all": exam_list,
            "warning": warning,
            "message": f"⚠️ ALERT: {exam['subject']} exam is in just {days} day(s)!" if warning else f"📅 Your nearest exam is {exam['subject']} in {days} days."
        }

    # Attendance queries
    elif any(word in q for word in ["attendance", "bunk", "absent", "shortage", "75%"]):
        risks = get_attendance_risks()
        all_attendance = data["attendance"]
        response_list = []
        for s in all_attendance:
            rec = {"subject": s["subject"], "percentage": s["percentage"], "classes_attended": s["classes_attended"], "total_classes": s["total_classes"]}
            if s["percentage"] < 75:
                needed = 0
                attended = s["classes_attended"]
                total = s["total_classes"]
                while (attended / (total + needed)) * 100 < 75:
                    attended += 1
                    needed += 1
                rec["risk"] = True
                rec["classes_needed"] = needed
                rec["message"] = f"⚠️ Attend {needed} more consecutive classes to reach 75%"
            else:
                can_miss = 0
                attended = s["classes_attended"]
                total = s["total_classes"]
                while ((attended) / (total + can_miss + 1)) * 100 >= 75:
                    can_miss += 1
                rec["risk"] = False
                rec["can_miss"] = can_miss
                rec["message"] = f"✅ Safe! You can miss up to {can_miss} more classes."
            response_list.append(rec)

        return {
            "type": "attendance",
            "data": response_list,
            "risks": len(risks),
            "message": f"🚨 {len(risks)} subject(s) have attendance below 75%!" if risks else "✅ Your attendance is healthy across all subjects!"
        }

    # Assignment queries
    elif any(word in q for word in ["assignment", "submission", "pending", "due", "deadline"]):
        pending = get_pending_assignments()
        return {
            "type": "assignments",
            "pending": pending,
            "count": len(pending),
            "message": f"📝 You have {len(pending)} pending assignment(s)!" if pending else "🎉 All assignments submitted!"
        }

    # Study plan / free slots
    elif any(word in q for word in ["study plan", "free slot", "study time", "when to study", "schedule study"]):
        slots = data["free_slots"]
        return {
            "type": "study_plan",
            "slots": slots,
            "message": f"📚 Found {len(slots)} free study slots in your timetable!"
        }

    # Crash plan queries
    elif "crash" in q or "revision" in q or "last minute" in q or "quick revision" in q:
        subject = None
        for subj in ["dbms", "python", "cn", "computer networks", "operating systems", "os"]:
            if subj in q:
                subject = subj
                break
        if not subject:
            subject = "dbms"  # default

        plan = build_crash_plan(subject)
        if plan:
            return {
                "type": "crash_plan",
                "subject": plan["subject"],
                "days": plan["days"],
                "tips": plan.get("tips", []),
                "message": f"🚀 Here's your {plan['subject']} crash revision plan!"
            }
        else:
            return {"type": "crash_plan", "message": f"Crash plan for '{subject}' not found. Try: DBMS, Python, or CN."}

    # Stress / help queries
    elif any(word in q for word in ["stressed", "stress", "anxious", "worried", "scared", "pass", "fail", "help me"]):
        nearest = get_nearest_exam()
        plan = build_crash_plan("dbms")
        return {
            "type": "stress_support",
            "nearest_exam": nearest[0]["subject"] if nearest else None,
            "days_left": nearest[1] if nearest else None,
            "tips": [
                "🌬️ Take 3 deep breaths — you've got this.",
                "📌 Focus on one subject at a time.",
                "⏱️ Use the Pomodoro technique: 25 min study, 5 min break.",
                "💤 Sleep at least 6 hours — memory consolidates during sleep.",
                "📝 Don't re-read notes. Practice past papers instead.",
                "🎯 Cover high-weightage topics first (VTU pattern).",
            ],
            "message": "💙 Hey, take a breath. Here's a low-stress revision strategy for you:"
        }

    # Greetings
    elif any(word in q for word in ["hi", "hello", "hey", "good morning", "good evening"]):
        nearest = get_nearest_exam()
        risks = get_attendance_risks()
        pending = get_pending_assignments()
        alerts = []
        if nearest and nearest[1] <= 5:
            alerts.append(f"📅 {nearest[0]['subject']} exam in {nearest[1]} days!")
        if risks:
            alerts.append(f"⚠️ {len(risks)} subject(s) with attendance risk.")
        if pending:
            alerts.append(f"📝 {len(pending)} pending assignment(s).")
        return {
            "type": "greeting",
            "alerts": alerts,
            "message": "👋 Hey! I'm CampusBuddy AI — your Academic Copilot. Here's your quick academic pulse:"
        }

    # Default
    else:
        return {
            "type": "default",
            "suggestions": [
                "When is my next exam?",
                "Check my attendance",
                "Show pending assignments",
                "Create DBMS crash plan",
                "Show my study slots",
                "I'm feeling stressed"
            ],
            "message": "🤔 I didn't quite get that. Here are some things I can help you with:"
        }


@app.route("/")
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
