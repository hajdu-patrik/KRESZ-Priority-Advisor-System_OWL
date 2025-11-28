![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Framework-Flask-000000?style=flat&logo=flask&logoColor=white)
![Owlready2](https://img.shields.io/badge/Semantic_Web-Owlready2-A42E2B?style=flat&logo=python&logoColor=white)
![SWRL](https://img.shields.io/badge/Logic-SWRL%20%26%20Pellet-4B0082?style=flat)
![HTML5](https://img.shields.io/badge/Frontend-HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/Style-CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/Script-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Status](https://img.shields.io/badge/Status-Educational_Project-brightgreen?style=flat)
# KRESZ Priority Advisor System

A Semantic Web-based decision support system that models the **Hungarian Highway Code (KRESZ) Section 28** regarding Priority at Intersections. The project was developed as part of the **BME-VIK "Natural Language and Semantic Technologies"** course.

The system determines the right-of-way between two vehicles using a hybrid reasoning approach: it combines an **OWL 2.0 Ontology and SWRL rules** with procedural Python logic to handle complex, non-monotonic traffic exceptions.

---

## 🚀 Features

- 🚦 **Traffic Situation Modeling** – dynamic creation of ABox individuals (Vehicles, Roads, Signs) based on user input.
- 🧠 **Semantic Reasoning** – uses the **Pellet reasoner** to infer priority relationships (`yieldsTo`) based on defined SWRL rules.
- 📜 **Complex Rule Handling** – implements the hierarchy of KRESZ § 28:
    - *Emergency Vehicles*
    - *Road Surface (Paved vs. Dirt)*
    - *Traffic Signs (Priority, Stop, Yield)*
    - *Tram Priority (in equal situations)*
    - *Right-hand Rule*
- 🌐 **Web Interface** – clean, responsive UI using Flask and Jinja2 templates.
- 🌗 **Dark/Light Mode** – user preference is saved in local storage.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+
- **Web Server:** Flask
- **ML/NLPSemantic Web:** Scikit-learn, TF-IDF, Logistic Regression, Cosine Similarity
    - **Owlready2:** For Ontology manipulation and SWRL rule integration.
    - **Pellet:** For consistency checking and inference.
- **Frontend:** HTML5, CSS3, JavaScript

---

## 📂 Project Structure
```
KRESZ_Priority_Advisor_System/
├── app/
│   ├── business_logic.py   # Core Ontology definition, SWRL rules, and Decision Tree
│   └── app.py              # Flask server controller and routing
│
├── import/
│   └── requirements.txt
│
├── static/
│   ├── style.css
│   ├── scripts.js
│   └── icon.ico
│
└── template/
    ├── index.html
    └── 404.html
```

---

## 🧠 Ontology & Logic

The system creates an in-memory ontology (`http://test.org/kresz_full.owl`) for every request to ensure a stateless calculation.

1. **TBox (Terminology)**
    - **Classes:** `Vehicle` (Subclasses: `Tram`, `EmergencyVehicle`), `Road` (Subclasses: `PavedRoad`, `DirtRoad`), `TrafficSign` (`StopSign`, `PrioritySignv, etc.).
    - **Properties** `locatedOn` (Vehicle $\to$ Road), `hasSign` (Road $\to$ Sign), `isRightOf` (Spatial relation).

2. **Reasoning (SWRL & Python)**
The logic follows a strict hierarchy:
    1. **Emergency Vehicles:** Always take precedence (unless meeting another emergency vehicle).
    2. **Road Surface:** Dirt roads yield to paved roads.
    3. **Traffic Signs:** SWRL rules infer `yieldsTo` relations based on sign hierarchy (e.g., STOP vs. Priority).
    4. **Equal Situations:** If signs/roads are equal rank:
        - **Tram Rule:** Trams take priority.
        - **Right-hand Rule:** The vehicle coming from the right has priority.

---

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
git clone [https://github.com/hajdu-patrik/KRESZ-Priority-Advisor-System_OWL]
cd your-repo-name
```

### 2. Create and Activate Virtual Environment

**Windows (Git Bash):**
```bash
python -m venv .venv
source .venv/Scripts/activate"
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r imports/requirements.txt
```

### 4. Run the Application

To launch the server (the script automatically handles the split folder structure):
```bash
python app/app.py
```
The server will be available here:
- http://127.0.0.1:5000
- http://localhost:5000

Open it in your browser to use it.

---

## 🎮 Usage Example

1. **Open the Web Interface.**
2. **Configure Vehicle 'A' (You):**
    - Type: *Car*
    - Road: *Paved*
    - Sign: *STOP Sign*
3. **Configure Vehicle 'B' (Other):**
    - Type: *Car*
    - Road: *Paved*
    - Sign: *Priority Road*
    - Direction: *Coming from Left*
4. **Click Analyze.**

**Result:**
    ⚠️ **ELSŐBBSÉGET KELL ADNOD!** (Tábla szabályozás) (*Since Vehicle B is on a priority road and you have a STOP sign, the SWRL rule infers that you must yield*)
