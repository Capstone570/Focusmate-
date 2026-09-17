import os

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FocusMate AI Pro", page_icon="🔮", layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: radial-gradient(
        circle at 50% 20%,
        #0f172a 0%,
        #020617 100%
    );
    color: #f8fafc;
}

.main-title {
    font-size: 60px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(
        135deg,
        #a5f3fc,
        #38bdf8,
        #818cf8
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 20px;
    margin-bottom: 35px;
}

.card {
    background: rgba(15, 23, 42, 0.75);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(56, 189, 248, 0.3);
    margin-bottom: 20px;
}

.result {
    background: rgba(15, 23, 42, 0.9);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(56, 189, 248, 0.2);
    text-align: center;
}

.big-number {
    font-size: 42px;
    font-weight: 800;
    color: #38bdf8;
}

.small-text {
    color: #94a3b8;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# STARTER TRAINING DATA
# ============================================================

# This is starter/demo data.
# Replace or expand it with real user data for a stronger project.

starter_data = pd.DataFrame({
    "sleep": [
        9,
        8,
        8,
        7,
        7,
        6,
        6,
        5,
        5,
        4,
        4,
        9,
        8,
        7,
        6,
        5,
        3,
        9,
        8,
        6,
        7,
        5,
        4,
        3,
        8,
        9,
        7,
        6,
        5,
        4,
    ],
    "energy": [
        9,
        8,
        9,
        8,
        7,
        6,
        7,
        5,
        4,
        3,
        4,
        9,
        8,
        7,
        6,
        5,
        3,
        10,
        9,
        7,
        8,
        5,
        4,
        3,
        8,
        9,
        7,
        6,
        5,
        4,
    ],
    "difficulty": [
        3,
        4,
        5,
        5,
        6,
        6,
        7,
        7,
        8,
        9,
        8,
        2,
        4,
        6,
        7,
        8,
        9,
        3,
        5,
        6,
        4,
        8,
        9,
        10,
        5,
        3,
        7,
        8,
        9,
        10,
    ],
    "mood": [
        "happy",
        "happy",
        "happy",
        "happy",
        "tired",
        "tired",
        "stressed",
        "stressed",
        "distracted",
        "distracted",
        "stressed",
        "happy",
        "happy",
        "tired",
        "stressed",
        "distracted",
        "tired",
        "happy",
        "happy",
        "stressed",
        "happy",
        "distracted",
        "tired",
        "stressed",
        "happy",
        "happy",
        "stressed",
        "distracted",
        "tired",
        "stressed",
    ],
    "sprint": [
        45,
        45,
        45,
        45,
        25,
        25,
        25,
        25,
        15,
        15,
        15,
        45,
        45,
        25,
        25,
        15,
        15,
        45,
        45,
        25,
        45,
        15,
        15,
        15,
        45,
        45,
        25,
        15,
        15,
        15,
    ],
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
# PREPARE DATA
# ============================================================

data = load_data()

mood_mapping = {"stressed": 0, "tired": 1, "distracted": 2, "happy": 3}


def prepare_features(df):

    features = df[["sleep", "energy", "difficulty", "mood"]].copy()

    features["mood"] = features["mood"].map(mood_mapping)

    return features


X = prepare_features(data)
y = data["sprint"]


# ============================================================
# TRAIN MACHINE LEARNING MODEL
# ============================================================

model = DecisionTreeClassifier(max_depth=5, random_state=42)

model.fit(X, y)


# ============================================================
# MODEL ACCURACY
# ============================================================

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

st.markdown(
    '<div class="main-title">FocusMate AI</div>', unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    "Your Personal Machine-Learning Focus Assistant"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🧠 Tell FocusMate About Your Current State")

col1, col2 = st.columns(2)

with col1:

    mood = st.selectbox(
        "Current Mood", ["happy", "stressed", "tired", "distracted"]
    )

    sleep = st.slider("😴 Sleep Score", min_value=1, max_value=10, value=7)

with col2:

    energy = st.slider("⚡ Energy Level", min_value=1, max_value=10, value=8)

    difficulty = st.slider(
        "🎯 Task Difficulty", min_value=1, max_value=10, value=6
    )

task_name = st.text_input(
    "What are you working on?", placeholder="Example: Biology revision"
)

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# AI PREDICTION
# ============================================================

if st.button("✨ Ask FocusMate AI", use_container_width=True):

    mood_number = mood_mapping[mood]

    input_data = pd.DataFrame({
        "sleep": [sleep],
        "energy": [energy],
        "difficulty": [difficulty],
        "mood": [mood_number],
    })

    # --------------------------------------------------------
    # ML PREDICTION
    # --------------------------------------------------------

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    confidence = max(probabilities) * 100

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("🤖 AI Recommendation")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="result">'
            '<div class="small-text">Recommended Sprint</div>'
            f'<div class="big-number">{prediction} min</div>'
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="result">'
            '<div class="small-text">AI Confidence</div>'
            f'<div class="big-number">{confidence:.0f}%</div>'
            "</div>",
            unsafe_allow_html=True,
        )

    with col3:

        if prediction == 45:
            rest = 10
        else:
            rest = 5

        st.markdown(
            '<div class="result">'
            '<div class="small-text">Recommended Break</div>'
            f'<div class="big-number">{rest} min</div>'
            "</div>",
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------------

    st.markdown("### 🔍 Why did the AI choose this?")

    if sleep >= 7:
        sleep_message = "Your sleep score suggests good recovery."
    else:
        sleep_message = (
            "Your sleep score suggests you may benefit from shorter sessions."
        )

    if energy >= 7:
        energy_message = "Your energy level is relatively high."
    else:
        energy_message = "Your energy level is relatively low."

    if difficulty >= 8:
        difficulty_message = "The task is quite difficult."
    else:
        difficulty_message = "The task difficulty is manageable."

    st.info(
        f"{sleep_message} "
        f"{energy_message} "
        f"{difficulty_message} "
        f"The machine-learning model combined these inputs with your mood "
        f"to predict the most suitable sprint length."
    )

    # --------------------------------------------------------
    # TASK ROADMAP
    # --------------------------------------------------------

    st.subheader("📋 AI Action Roadmap")

    task = task_name if task_name else "your task"

    st.write(f"**1. Prepare:** Set up everything needed for {task}.")

    st.write(f"**2. Focus:** Work continuously for {prediction} minutes.")

    st.write(
        f"**3. Review:** Check your progress and take a {rest}-minute break."
    )

    # --------------------------------------------------------
    # STORE PREDICTION
    # --------------------------------------------------------

    st.session_state["last_prediction"] = prediction

    st.session_state["last_inputs"] = {
        "sleep": sleep,
        "energy": energy,
        "difficulty": difficulty,
        "mood": mood,
    }


# ============================================================
# FEEDBACK SECTION
# ============================================================

if "last_prediction" in st.session_state:

    st.markdown("---")

    st.subheader("📊 Teach FocusMate AI")

    st.write("After completing your sprint, tell the AI how effective it was.")

    effectiveness = st.slider(
        "How effective was the sprint?", min_value=1, max_value=5, value=3
    )

    if st.button("💾 Submit Feedback", use_container_width=True):

        inputs = st.session_state["last_inputs"]

        # ----------------------------------------------------
        # Convert effectiveness into a training decision
        # ----------------------------------------------------

        if effectiveness >= 4:

            recommended_sprint = st.session_state["last_prediction"]

        elif effectiveness <= 2:

            # If the sprint wasn't effective,
            # choose a shorter duration as feedback.

            current = st.session_state["last_prediction"]

            if current == 45:
                recommended_sprint = 25

            elif current == 25:
                recommended_sprint = 15

            else:
                recommended_sprint = 15

        else:

            recommended_sprint = st.session_state["last_prediction"]

        new_row = pd.DataFrame({
            "sleep": [inputs["sleep"]],
            "energy": [inputs["energy"]],
            "difficulty": [inputs["difficulty"]],
            "mood": [inputs["mood"]],
            "sprint": [recommended_sprint],
        })

        data = pd.concat([data, new_row], ignore_index=True)

        save_data(data)

        # Retrain model immediately

        X = prepare_features(data)

        y = data["sprint"]

        model.fit(X, y)

        st.success(
            "Feedback saved! FocusMate AI has learned from your result."
        )

        st.info(f"The training dataset now contains {len(data)} examples.")


# ============================================================
# MODEL INFORMATION
# ============================================================

st.markdown("---")

st.subheader("🧠 Machine Learning Information")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric("Training Examples", len(data))

with col2:

    st.metric("ML Algorithm", "Decision Tree")

with col3:

    if accuracy is not None:

        st.metric("Test Accuracy", f"{accuracy * 100:.1f}%")

    else:

        st.metric("Test Accuracy", "Collecting Data")


st.caption(
    "FocusMate AI learns from sleep, energy, mood, task difficulty, "
    "and user feedback to recommend a focus sprint."
)


# ============================================================
# DATASET VIEW
# ============================================================

with st.expander("🔬 View Training Data"):

    st.dataframe(data, use_container_width=True)
