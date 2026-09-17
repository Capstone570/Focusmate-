import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier

st.set_page_config(page_title="FocusMate AI Pro", page_icon="🔮", layout="wide")

# Custom styling for glassmorphism layout
st.markdown("""
    <style>
        .block-container { padding-top: 2rem !important; }
        footer { visibility: hidden; }
        
        div[data-testid="stForm"], div[data-testid="stMetric"] {
            background: rgba(30, 27, 46, 0.6) !important;
            backdrop-filter: blur(16px);
            border: 1px solid rgba(192, 132, 252, 0.2) !important;
            border-radius: 1rem !important;
            padding: 1rem !important;
        }
        
        div[data-testid="stMetricValue"] {
            color: #c084fc !important;
            font-weight: 800 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. DATASET GENERATION & MODEL TRAINING (ML BACKEND)
# ---------------------------------------------------------
@st.cache_resource
def train_ml_models():
    """
    Generates synthetic productivity data and trains real Scikit-Learn ML models:
    1. Regressor: Predicts Focus Capacity %, Sprint Time, Rest Time.
    2. Classifier: Predicts optimal Soundscape based on Mood and Metrics.
    """
    np.random.seed(42)
    n_samples = 500

    # Feature Matrix (X): Sleep, Energy, Difficulty, Mood (encoded 0-3)
    sleep_data = np.random.randint(1, 11, n_samples)
    energy_data = np.random.randint(1, 11, n_samples)
    diff_data = np.random.randint(1, 11, n_samples)
    mood_data = np.random.randint(0, 4, n_samples)

    X = np.column_stack((sleep_data, energy_data, diff_data, mood_data))

    # Target Outputs (y)
    # Target 1: Focus Capacity (%)
    y_capacity = (sleep_data * 4.5) + (energy_data * 5.0) - (diff_data * 1.5) + np.random.normal(0, 3, n_samples)
    y_capacity = np.clip(y_capacity, 10, 100)

    # Target 2: Sprint Duration (minutes)
    y_sprint = (y_capacity * 0.35) - (diff_data * 1.2) + np.random.normal(0, 2, n_samples)
    y_sprint = np.clip(y_sprint, 15, 60)

    # Target 3: Rest Interval (minutes)
    y_rest = (y_sprint * 0.2) + (10 - energy_data) * 0.3
    y_rest = np.clip(y_rest, 5, 20)

    y_regression = np.column_stack((y_capacity, y_sprint, y_rest))

    # Soundscape Classification Target (0: Binaural, 1: Rain, 2: White Noise)
    y_audio = np.where(mood_data == 0, 1, np.where(mood_data == 2, 2, 0))

    # Train Models
    regressor = RandomForestRegressor(n_estimators=50, random_state=42)
    regressor.fit(X, y_regression)

    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X, y_audio)

    return regressor, classifier

# Load and train ML models
regressor_model, classifier_model = train_ml_models()

# Audio asset store
SOUND_URLS = {
    "binaural": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3",
    "rain": "https://cdn.pixabay.com/download/audio/2021/09/06/audio_8a287e07eb.mp3",
    "white": "https://cdn.pixabay.com/download/audio/2022/03/24/audio_c8c8731f82.mp3"
}
AUDIO_LABELS = {0: "binaural", 1: "rain", 2: "white"}

# Session state initialization
if "sprints_completed" not in st.session_state:
    st.session_state.sprints_completed = 0

if "ml_prediction" not in st.session_state:
    st.session_state.ml_prediction = None


# ---------------------------------------------------------
# 2. USER INPUT INTERFACE
# ---------------------------------------------------------
st.title("FocusMate AI Pro 🔮")
st.caption("Machine Learning Driven Focus & Productivity Engine")

st.markdown("### ⚙️ Input Parameters")

with st.form("focus_form"):
    mood_map = {
        "😰 Stressed / Anxious": 0,
        "🥱 Tired / Low Energy": 1,
        "📱 Distracted / Restless": 2,
        "🌟 Happy / Motivated": 3
    }
    selected_mood_label = st.radio("🧠 1. Current State of Mind", list(mood_map.keys()), horizontal=True)
    selected_mood_val = mood_map[selected_mood_label]

    task_name = st.text_input("🎯 2. Primary Task Goal", placeholder="e.g., Build ML regression pipeline...")
    
    col_diff, col_sleep, col_energy = st.columns(3)
    with col_diff:
        difficulty = st.slider("Perceived Difficulty", min_value=1, max_value=10, value=6)
    with col_sleep:
        sleep = st.slider("😴 Sleep Score", min_value=1, max_value=10, value=7)
    with col_energy:
        energy = st.slider("⚡ Energy Level", min_value=1, max_value=10, value=8)

    submit_btn = st.form_submit_button("🤖 Generate ML Strategy Prediction", use_container_width=True)


# ---------------------------------------------------------
# 3. MACHINE LEARNING PREDICTION ENGINE (NO IF-ELSE)
# ---------------------------------------------------------
if submit_btn:
    # 1. Format input vector for ML model inference
    input_features = np.array([[sleep, energy, difficulty, selected_mood_val]])

    # 2. Execute ML Regression Model Prediction
    regression_preds = regressor_model.predict(input_features)[0]
    predicted_capacity = int(round(regression_preds[0]))
    predicted_sprint = int(round(regression_preds[1]))
    predicted_rest = int(round(regression_preds[2]))

    # 3. Execute ML Soundscape Classification Prediction
    audio_class_pred = classifier_model.predict(input_features)[0]
    predicted_audio_key = AUDIO_LABELS[audio_class_pred]

    # Save predictions to state
    st.session_state.ml_prediction = {
        "capacity": predicted_capacity,
        "sprint_time": predicted_sprint,
        "rest_time": predicted_rest,
        "audio_key": predicted_audio_key,
        "task": task_name if task_name.strip() else "Primary Goal"
    }


# ---------------------------------------------------------
# 4. OUTPUT DASHBOARD & PREDICTION RESULTS
# ---------------------------------------------------------
if st.session_state.ml_prediction is not None:
    pred = st.session_state.ml_prediction
    
    st.markdown("---")
    st.markdown("### 🤖 ML Model Output & Strategy")

    # Display Predictions as UI Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Focus Capacity", f"{pred['capacity']}%")
    m2.metric("Optimal Sprint Length", f"{pred['sprint_time']} min")
    m3.metric("Recommended Rest", f"{pred['rest_time']} min")

    # AI Roadmap Output
    st.markdown("#### 📋 AI Generated Task Decomposition")
    st.info(f"""
    1. Set up workspace and open resources for: **{pred['task']}**
    2. Execute focused work sprint for **{pred['sprint_time']} minutes** based on ML model estimation.
    3. Recover with a **{pred['rest_time']}-minute break** before starting the next cycle.
    """)

    # Audio Classification Output
    st.markdown("#### 🔊 Recommended Ambient Soundscape (ML Categorized)")
    st.audio(SOUND_URLS[pred['audio_key']])

    # Performance Tracking
    col_a, col_b = st.columns(2)
    col_a.metric("Daily Streak", "🔥 1 Day")
    col_b.metric("Completed Sprints", f"{st.session_state.sprints_completed} Sprints")
