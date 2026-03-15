Heal-o-Thon
# Blood-Link 🩸
**Rewiring India’s veins: The decentralized grid where every drop beats the clock.**
Blood-Link is a real-time, decentralized emergency blood grid designed to track inventory and predict shortages across India using the **ABDM (Ayushman Bharat Digital Mission)** framework. By shifting from reactive logistics to proactive predictive routing, we ensure that life-saving resources are synchronized across the nation's heartbeat.
---
## ⚙️ The Problem & The Impact
In India, lives are often lost not because blood is unavailable, but because it is in the wrong place at the wrong time. Blood-Link solves this by creating an intelligent nexus:
- **Decentralized Tracking:** Real-time dashboard for inventory across all grid nodes.
- **Predictive Intelligence:** Shifting focus from where blood *is* to where it *will be needed*.
- **ABDM Integration:** Leveraging national digital health frameworks for seamless scalability.
---
## 🛠️ Requirements & Installation
This project is split into a **Predictive ML Dashboard** (Python) and a **Modern Web Frontend** (React/Vite).
### 1. Backend & ML Environment (Python)
You will need Python 3.9+ installed.
**Installation:**
```bash
# From the project root, install the core data science and dashboard stack
pip install streamlit scikit-learn pandas numpy folium streamlit-folium
2. Modern Frontend (React/Vite)
You will need Node.js (v18+) and npm installed.
Installation:
Bash
# Navigate to the frontend directory
cd health-frontend
# Recreate the node_modules folder locally
npm install
🖥️ How to Run
Start the Predictive Dashboard (Streamlit)
The dashboard handles the geospatial mapping and the ML risk assessment.
Bash
# From the root directory
streamlit run app.py
Start the Web Interface (Vite)
The modern web interface handles user interactions and hospital coordination.
Bash
cd health-frontend
npm run dev
🧠 Machine Learning: Predictive Routing
To make this system proactive, our intelligence engine utilizes a Random Forest Classifier built via Scikit-learn.
The Engine: We chose an ensemble Random Forest model because it excels at handling the non-linear variables inherent in healthcare logistics (seasonal demand, regional density, and depletion rates).
The Output: The classifier categorizes grid nodes into three actionable risk tiers: Stable, Warning, or Critical Shortage Imminent within a 48-hour window.
Explainability: By extracting feature importance, we ensure medical administrators can see why a shortage is predicted, removing the "black box" element of AI in healthcare.
🏗️ Tech Stack
ML Engine: Scikit-learn (Random Forest Classifier)
Data & Dashboard: Python, Streamlit, Pandas
Visualization: Folium (Geospatial mapping)
Frontend: React, Vite, Tailwind CSS
Database: SQLite (hospitals.db)
Framework: ABDM (Ayushman Bharat Digital Mission)
🏆 HEAL-A-Thon 2026
Developed for the HEAL-A-Thon 2026 at PES University.
requirements.txt
Plaintext
streamlit
scikit-learn
pandas
numpy
folium
streamlit-folium
db-sqlite3
