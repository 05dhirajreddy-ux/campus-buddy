# 🎓 CampusBuddy AI — Academic Copilot

> **Unlike reactive college bots, CampusBuddy AI proactively predicts deadlines, attendance risk, and generates personalized revision plans.**

---

## 🚀 Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
# http://localhost:5000
```

---

## 🌍 Deploy to Render (Free)

1. Push this folder to a GitHub repo
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Deploy! ✅

---

## 📁 Project Structure

```
CampusBuddyAI/
├── app.py              ← Flask backend + AI logic
├── data.json           ← Simulated ERP database (VTU data)
├── requirements.txt    ← Flask + Gunicorn
├── render.yaml         ← Render deployment config
├── templates/
│   └── index.html      ← Full dashboard + chat UI
└── static/
    └── style.css       ← Premium dark/light design system
```

---

## 🎥 Hackathon Demo Flow

1. **Open Dashboard** — 4 pulse cards show live academic pulse
2. **Exam Countdown** — DBMS exam in 5 days with ⚠️ warning
3. **Ask: "Show my attendance"** — 3 subjects below 75% with fix plans
4. **Ask: "Create DBMS crash plan"** — 2-day revision roadmap with VTU topics
5. **Ask: "I'm stressed"** — Low-anxiety revision strategy with tips

---

## 🧠 AI Logic (Rule-Based)

| Query Type | Triggers | Response |
|---|---|---|
| Exams | "exam", "when is", "schedule" | Countdown + syllabus + warnings |
| Attendance | "attendance", "bunk", "75%" | Risk analysis + fix plan |
| Crash Plan | "crash", "revision", "DBMS" | 2-day topic roadmap |
| Assignments | "assignment", "pending" | Due dates + priority |
| Study Plan | "study slot", "free time" | Timetable-based suggestions |
| Stress | "stressed", "worried", "fail" | Low-anxiety tips + resources |

---

## 🏆 Innovation Highlights

- **Proactive Alerts**: Warns 3 days before exams automatically
- **Attendance AI**: Calculates exactly how many classes to attend
- **Crash Plans**: VTU-pattern topic breakdowns with weightage
- **Stress-Aware**: Detects emotional keywords → offers calm support
- **Dark/Light Mode**: Toggle with ☀️/🌙 button

---

## 🌍 Future Scope

- 🔗 Real ERP API integration (VTU, VTOP portals)
- 📱 WhatsApp bot via Twilio
- 📧 Email reminders for exams
- 🎙️ Voice assistant mode
- 📄 Syllabus PDF summarizer (Claude AI)
- 💼 Placement prep mode
- 🤝 Study group matcher

---

## 👨‍💻 Built With

- **Python Flask** — Backend
- **Vanilla JS** — Frontend logic (no framework needed)
- **CSS Variables** — Dark/light theming
- **JSON** — Simulated ERP database
- **Rule-based AI** — Smart pattern matching

---

*Built for hackathon demo. Data is simulated for BMS College of Engineering, Bengaluru.*
