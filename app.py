import streamlit as st
import streamlit.components.v1 as components
import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier

@st.cache_resource
def train_ml_models():
    np.random.seed(42)
    n_samples = 500

    # Features: Sleep, Energy, Difficulty, Mood (0-3)
    sleep_data = np.random.randint(1, 11, n_samples)
    energy_data = np.random.randint(1, 11, n_samples)
    diff_data = np.random.randint(1, 11, n_samples)
    mood_data = np.random.randint(0, 4, n_samples)
    X = np.column_stack((sleep_data, energy_data, diff_data, mood_data))

    # Regression Targets: Capacity, Sprint Time, Rest Time
    y_capacity = np.clip((sleep_data * 4.5) + (energy_data * 5.0) - (diff_data * 1.5) + np.random.normal(0, 3, n_samples), 10, 100)
    y_sprint = np.clip((y_capacity * 0.35) - (diff_data * 1.2) + np.random.normal(0, 2, n_samples), 15, 60)
    y_rest = np.clip((y_sprint * 0.2) + (10 - energy_data) * 0.3, 5, 20)
    y_regression = np.column_stack((y_capacity, y_sprint, y_rest))

    # Soundscape Classification Target (0: binaural, 1: rain, 2: white)
    y_audio = np.where(mood_data == 0, 1, np.where(mood_data == 2, 2, 0))

    regressor = RandomForestRegressor(n_estimators=50, random_state=42).fit(X, y_regression)
    classifier = KNeighborsClassifier(n_neighbors=5).fit(X, y_audio)

    return regressor, classifier

regressor_model, classifier_model = train_ml_models()
