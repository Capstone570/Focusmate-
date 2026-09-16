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
    page_title="FocusMate AI Pro",
    page_icon="🔮",
    layout="wide"
)

# ============================================================
# CLEAN UI ENHANCEMENTS (STREAMLIT NATIVE-FRIENDLY)
# ============================================================

st.markdown("""
<style>
/* Clean primary color accent for sliders & buttons */
:root {
    --primary-color: #8b5cf6;
}

/* Stylized main header */
.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    color: #7c3aed;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 1.1rem;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# STARTER TRAINING DATA
# ============================================================

starter_data = pd.DataFrame({
    "sleep": [
        9, 8, 8, 7, 7, 6, 6, 5, 5, 4,
        4, 9, 8, 7, 6, 5, 3, 9, 8, 6,
        7, 5, 4, 3, 8, 9, 7, 6, 5, 4
    ],
    "energy": [
        9, 8, 9, 8, 7, 6, 7, 5, 4, 3,
        4, 9, 8, 7, 6, 5, 3, 10, 9, 7,
        8, 5, 4, 3, 8, 9, 7, 6, 5, 4
    ],
    "difficulty": [
        3, 4, 5, 5, 6, 6, 7, 7, 8, 9,
        8, 2, 4, 6, 7, 8, 9, 3, 5, 6,
        4, 8, 9, 10, 5, 3, 7, 8, 9, 10
    ],
    "mood": [
        "happy", "happy", "happy", "happy", "tired",
        "tired", "stressed", "stressed", "distracted", "distracted",
        "stressed", "happy", "happy", "tired", "stressed",
        "distracted", "tired", "happy", "happy", "stressed",
        "happy", "distracted", "tired", "stressed", "happy",
        "happy", "stressed", "distracted", "tired", "stressed"
    ],
    "sprint": [
        45, 45, 45, 45, 25, 25, 25, 25, 15, 15,
        15, 45, 45, 25, 25, 15, 15, 45, 45, 25,
        45, 15, 15, 15, 45, 45, 25, 15, 15, 15
    ]
})


# ============================================================
# DATA STORAGE
# ============================================================

DATA_FILE = "focus_data.csv"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            saved_data = pd.read_csv(DATA_FILE)
            if len(saved_data) > 0:
                return saved_data
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

# Train Decision Tree Classifier
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X, y)


# Evaluate Model Accuracy
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
# HEADER
# ============================================================

st.markdown('<h1 class="main-title">🔮 FocusMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Personal Machine-Learning Focus Assistant</p>', unsafe_allow_html=True)


# ============================================================
# INPUT SECTION (NATIVE STREAMLIT CONTAINER)
# ============================================================

with st.container(border=True):
    st.subheader("🧠 Tell FocusMate About Your Current State")
    st.write("Adjust your metrics below so the Decision Tree algorithm can predict your optimal focus time.")
    
    col1, col2 = st.columns(2)

    with col1:
        mood = st.selectbox(
            "Current Mood",
            ["happy", "stressed", "tired", "distracted"]
        )
        sleep = st.slider(
            "😴 Sleep Score (1 = Poor, 10 = Rested)",
            min_value=1, max_value=10, value=7
        )

    with col2:
        energy = st.slider(
            "⚡ Energy Level (1 = Exhausted, 10 = Peak)",
            min_value=1, max_value=10, value=8
        )
        difficulty = st.slider(
            "🎯 Task Difficulty (1 = Easy, 10 = Hard)",
            min_value=1, max_value=10, value=6
        )

    task_name = st.text_input(
        "What are you working on?",
        placeholder="Example: Biology revision"
    )

    predict_btn = st.button("✨ Ask FocusMate AI", use_container_width=True, type="primary")


# ============================================================
# AI PREDICTION & DISPLAY
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

    st.divider()
    st.subheader("🤖 AI Recommendation Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Recommended Sprint", f"{prediction} mins")
    col2.metric("AI Model Confidence", f"{confidence:.0f}%")
    col3.metric("Recommended Break", f"{rest} mins")

    st.markdown("### 🔍 Model Reasoning")
    sleep_msg = "Your sleep score suggests good recovery." if sleep >= 7 else "Your sleep score suggests shorter sessions."
    energy_msg = "Your energy level is high." if energy >= 7 else "Your energy level is currently low."
    diff_msg = "The task is quite demanding." if difficulty >= 8 else "Task difficulty is manageable."

    st.info(f"{sleep_msg} {energy_msg} {diff_msg} The Decision Tree evaluated these inputs alongside your '{mood}' mood to output a {prediction}-minute focus window.")

    st.markdown("### 📋 AI Action Plan")
    task = task_name if task_name else "your task"
    st.markdown(f"""
    1. **Prepare:** Clear distractions and set up material for **{task}**.
    2. **Focus:** Work without interruption for **{prediction} minutes**.
    3. **Rest:** Step away from the screen for a **{rest}-minute break**.
    """)

    st.session_state["last_prediction"] = prediction
    st.session_state["last_inputs"] = {
        "sleep": sleep,
        "energy": energy,
        "difficulty": difficulty,
        "mood": mood
    }


# ============================================================
# FEEDBACK SECTION (RETRAIN MODEL)
# ============================================================

if "last_prediction" in st.session_state:
    st.divider()
    with st.container(border=True):
        st.subheader("📊 Reinforcement Feedback (Train the AI)")
        st.write("Did the AI give you a good recommendation? Submit feedback to update the Decision Tree.")

        effectiveness = st.slider(
            "How effective was this sprint session?",
            min_value=1, max_value=5, value=3,
            help="1 = Too long/unproductive, 5 = Perfect focus session"
        )

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

            # Retrain model with new feedback data
            X = prepare_features(data)
            y = data["sprint"]
            model.fit(X, y)

            st.success("Feedback saved! The Decision Tree model has been updated with your session data.")
            st.info(f"Total dataset size is now {len(data)} observations.")


# ============================================================
# MACHINE LEARNING METRICS & DATASET VIEW
# ============================================================

st.divider()
st.subheader("⚙️ Machine Learning Pipeline Info")

m1, m2, m3 = st.columns(3)
m1.metric("Training Samples", len(data))
m2.metric("Algorithm", "Decision Tree Classifier")
m3.metric("Test Accuracy Score", f"{accuracy * 100:.1f}%" if accuracy is not None else "Collecting Data")

with st.expander("🔬 View Training Dataset (CSV Data)"):
    st.dataframe(data, use_container_width=True)
