import streamlit as st
import pandas as pd
import numpy as np
import os

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FocusMate AI — Robot Focus Companion",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# CUSTOM CSS (DARK ROBOT THEME & HIGH CONTRAST)
# ============================================================

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 50% 20%, #1a162b 0%, #080b12 100%);
    color: #f8fafc;
}

label, .stMarkdown, p, h1, h2, h3, h4, span {
    color: #f8fafc !important;
}

.robot-header {
    text-align: center;
    font-size: 65px;
    margin-bottom: 0px;
}

.main-title {
    font-size: 52px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #a78bfa, #c084fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1 !important;
    font-size: 18px;
    margin-bottom: 30px;
}

div[data-testid="stForm"], div[data-testid="stExpander"] {
    background-color: rgba(30, 27, 46, 0.7);
    border: 1px solid rgba(192, 132, 252, 0.3);
    border-radius: 16px;
}

.result-card {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(168, 85, 247, 0.4);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
}

.big-number {
    font-size: 38px;
    font-weight: 800;
    color: #c084fc !important;
}

.small-text {
    color: #94a3b8 !important;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA STORAGE & KAGGLE INTEGRATION
# ============================================================

DATA_FILE = "focus_data.csv"
KAGGLE_FILE = "student_productivity_20k.csv"

# Fallback starter dataset if Kaggle file isn't uploaded locally yet
starter_data = pd.DataFrame({
    "sleep": [9, 8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 9, 8, 7, 6, 5, 3, 9, 8, 6, 7, 5, 4, 3, 8, 9, 7, 6, 5, 4],
    "energy": [9, 8, 9, 8, 7, 6, 7, 5, 4, 3, 4, 9, 8, 7, 6, 5, 3, 10, 9, 7, 8, 5, 4, 3, 8, 9, 7, 6, 5, 4],
    "difficulty": [3, 4, 5, 5, 6, 6, 7, 7, 8, 9, 8, 2, 4, 6, 7, 8, 9, 3, 5, 6, 4, 8, 9, 10, 5, 3, 7, 8, 9, 10],
    "mood": ["happy", "happy", "happy", "happy", "tired", "tired", "stressed", "stressed", "distracted", "distracted",
             "stressed", "happy", "happy", "tired", "stressed", "distracted", "tired", "happy", "happy", "stressed",
             "happy", "distracted", "tired", "stressed", "happy", "happy", "stressed", "distracted", "tired", "stressed"],
    "sprint": [45, 45, 45, 45, 25, 25, 25, 25, 15, 15, 15, 45, 45, 25, 25, 15, 15, 45, 45, 25, 45, 15, 15, 15, 45, 45, 25, 15, 15, 15]
})

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except Exception:
            pass
    elif os.path.exists(KAGGLE_FILE):
        try:
            return pd.read_csv(KAGGLE_FILE)
        except Exception:
            pass
    return starter_data.copy()

def save_data(data):
    data.to_csv(DATA_FILE, index=False)


# ============================================================
# PREPARE DATA & TRAIN ML MODEL
# ============================================================

data = load_data()

mood_mapping = {
    "stressed": 0,
    "tired": 1,
    "distracted": 2,
    "happy": 3
}

def prepare_features(df):
    features = df[["sleep", "energy", "difficulty", "mood"]].copy()
    features["mood"] = features["mood"].map(mood_mapping)
    return features

X = prepare_features(data)
y = data["sprint"]

# Train Decision Tree Model (Teacher's Curriculum Requirement)
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X, y)

# Evaluate Accuracy
if len(data) >= 15:
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        accuracy_model = DecisionTreeClassifier(max_depth=5, random_state=42)
        accuracy_model.fit(X_train, y_train)
        predictions = accuracy_model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
    except Exception:
        accuracy = None
else:
    accuracy = None


# ============================================================
# APP HEADER
# ============================================================

st.markdown('<div class="robot-header">🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">FocusMate AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI Robot Companion for Focus & Productivity</div>', unsafe_allow_html=True)


# ============================================================
# INPUT SECTION
# ============================================================

with st.container(border=True):
    st.subheader("🧠 Status Check-in")
    
    col1, col2 = st.columns(2)
    
    with col1:
        mood = st.selectbox("Current Mood", ["happy", "stressed", "tired", "distracted"])
        sleep = st.slider("😴 Sleep Score", min_value=1, max_value=10, value=7)
        
    with col2:
        energy = st.slider("⚡ Energy Level", min_value=1, max_value=10, value=8)
        difficulty = st.slider("🎯 Task Difficulty", min_value=1, max_value=10, value=6)
        
    task_name = st.text_input("What task are you working on?", placeholder="Example: Math Homework")
    
    predict_btn = st.button("✨ Ask FocusMate AI Robot", use_container_width=True, type="primary")


# ============================================================
# AI PREDICTION & OUTPUT
# ============================================================

if predict_btn:
    mood_number = mood_mapping[mood]
    input_data = pd.DataFrame({
        "sleep": [sleep],
        "energy": [energy],
        "difficulty": [difficulty],
        "mood": [mood_number]
    })

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    confidence = max(probabilities) * 100
    rest = 10 if prediction == 45 else 5

    st.markdown("---")
    st.subheader("🤖 Robot Recommendation")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="small-text">Recommended Sprint</div>
            <div class="big-number">{prediction} min</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="small-text">AI Confidence</div>
            <div class="big-number">{confidence:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="result-card">
            <div class="small-text">Recommended Break</div>
            <div class="big-number">{rest} min</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🔍 Robot Analysis")
    sleep_msg = "Good sleep recovery detected." if sleep >= 7 else "Low sleep score; suggesting a shorter sprint."
    energy_msg = "Energy level is high." if energy >= 7 else "Energy is lower than average."
    diff_msg = "Task complexity is high." if difficulty >= 8 else "Task difficulty is manageable."

    st.info(f"🤖 **Robot Insight:** {sleep_msg} {energy_msg} {diff_msg} Decision Tree model mapped your state to a **{prediction}-minute sprint**.")

    st.markdown("### 📋 Focus Strategy")
    task = task_name if task_name else "your task"
    st.write(f"1. **Setup:** Clear away distractions and prepare **{task}**.")
    st.write(f"2. **Sprint:** Work continuously for **{prediction} minutes**.")
    st.write(f"3. **Recovery:** Take a **{rest}-minute break**.")

    st.session_state["last_prediction"] = prediction
    st.session_state["last_inputs"] = {
        "sleep": sleep,
        "energy": energy,
        "difficulty": difficulty,
        "mood": mood
    }


# ============================================================
# FEEDBACK SECTION
# ============================================================

if "last_prediction" in st.session_state:
    st.markdown("---")
    with st.container(border=True):
        st.subheader("📊 Train Your Robot")
        st.write("Submit your feedback to retrain the Decision Tree model.")

        effectiveness = st.slider("How effective was this focus sprint?", min_value=1, max_value=5, value=3)

        if st.button("💾 Submit Feedback & Retrain Model", use_container_width=True):
            inputs = st.session_state["last_inputs"]

            if effectiveness >= 4:
                recommended_sprint = st.session_state["last_prediction"]
            elif effectiveness <= 2:
                current = st.session_state["last_prediction"]
                recommended_sprint = 25 if current == 45 else 15
            else:
                recommended_sprint = st.session_state["last_prediction"]

            new_row = pd.DataFrame({
                "sleep": [inputs["sleep"]],
                "energy": [inputs["energy"]],
                "difficulty": [inputs["difficulty"]],
                "mood": [inputs["mood"]],
                "sprint": [recommended_sprint]
            })

            data = pd.concat([data, new_row], ignore_index=True)
            save_data(data)

            X = prepare_features(data)
            y = data["sprint"]
            model.fit(X, y)

            st.success("Robot trained! Feedback saved to dataset.")
            st.info(f"Dataset updated to {len(data)} total entries.")


# ============================================================
# ML METRICS & DATASET VIEW
# ============================================================

st.markdown("---")
st.subheader("⚙️ Machine Learning Pipeline")

col1, col2, col3 = st.columns(3)
col1.metric("Training Examples", f"{len(data):,}")
col2.metric("ML Algorithm", "Decision Tree Classifier")
col3.metric("Test Accuracy", f"{accuracy * 100:.1f}%" if accuracy is not None else "Collecting Data")

with st.expander("🔬 View Training Data (Kaggle Dataset Source)"):
    st.caption("Source: Kaggle Student Productivity and Behavior Dataset (20k)")
    st.dataframe(data, use_container_width=True)
