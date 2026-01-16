import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

PLACEHOLDER_IMAGE = "https://via.placeholder.com/400x300?text=Exercise+Demo+Not+Available"


# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()
EXERCISE_API_KEY = os.getenv("EXERCISEDB_API_KEY")

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Workout & Diet Planner",
    layout="centered"
)

# -------------------------------------------------
# Safe Initialization
# -------------------------------------------------
bmi = None
daily_calories = None
workout_plan = []

# -------------------------------------------------
# Cached ExerciseDB API Function
# -------------------------------------------------
@st.cache_data(ttl=3600)  # cache for 1 hour
def get_exercises(body_part):
    if not EXERCISE_API_KEY:
        return []

    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{body_part}"

    headers = {
        "X-RapidAPI-Key": EXERCISE_API_KEY,
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()[:6]  # limit results (free tier safe)
    else:
        return []

# -------------------------------------------------
# App Title
# -------------------------------------------------
st.title("🏋️ Workout & Diet Planner")
st.write("Personalized fitness guidance using a **100% free ExerciseDB API**.")

st.divider()

# -------------------------------------------------
# Sidebar Inputs (UI Improvement)
# -------------------------------------------------
st.sidebar.header("👤 User Details")

height = st.sidebar.number_input(
    "Height (cm)",
    min_value=100.0,
    max_value=250.0,
    step=1.0
)

weight = st.sidebar.number_input(
    "Weight (kg)",
    min_value=30.0,
    max_value=200.0,
    step=1.0
)

goal = st.sidebar.selectbox(
    "Fitness Goal",
    ["", "Weight Loss", "Muscle Gain", "General Fitness"]
)

body_part = st.sidebar.selectbox(
    "Exercise Body Part",
    ["", "back", "chest", "legs", "arms", "shoulders", "waist"]
)
show_only_gif = st.sidebar.checkbox(
    "Show only exercises with animation",
    value=True
)

# -------------------------------------------------
# BMI & Calories Calculation
# -------------------------------------------------
if height > 0 and weight > 0:
    bmi = weight / ((height / 100) ** 2)
    daily_calories = 2000  # demo logic

    st.subheader("📊 Health Metrics")

    col1, col2 = st.columns(2)
    col1.metric("BMI", f"{bmi:.2f}")
    col2.metric("Daily Calories", daily_calories)

st.divider()
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"
recommended_body_parts = []

if bmi is not None and goal:
    bmi_category = get_bmi_category(bmi)

    if goal == "Weight Loss":
        recommended_body_parts = ["legs", "waist", "back"]
    elif goal == "Muscle Gain":
        recommended_body_parts = ["chest", "arms", "shoulders"]
    else:
        recommended_body_parts = ["back", "legs", "arms"]

    st.info(f"Recommended focus areas based on BMI ({bmi_category}) and goal: "
            f"{', '.join(recommended_body_parts)}")


# -------------------------------------------------
# Progress Chart
# -------------------------------------------------
if bmi is not None:
    chart_data = pd.DataFrame({
        "Metric": ["BMI", "Calories"],
        "Value": [bmi, daily_calories]
    })

    st.subheader("📈 Progress Overview")
    st.bar_chart(chart_data.set_index("Metric"))

st.divider()

# -------------------------------------------------
# Workout Plan
# -------------------------------------------------
if bmi is not None and goal:
    st.subheader("📅 Weekly Workout Plan")

    if goal == "Weight Loss":
        workout_plan = [
            "Day 1: Cardio + Abs",
            "Day 2: HIIT",
            "Day 3: Rest",
            "Day 4: Strength + Cardio",
            "Day 5: Cardio",
            "Day 6: Yoga",
            "Day 7: Rest"
        ]
    elif goal == "Muscle Gain":
        workout_plan = [
            "Day 1: Chest & Triceps",
            "Day 2: Back & Biceps",
            "Day 3: Legs",
            "Day 4: Shoulders",
            "Day 5: Arms",
            "Day 6: Core",
            "Day 7: Rest"
        ]
    else:
        workout_plan = [
            "Day 1: Full Body",
            "Day 2: Cardio",
            "Day 3: Strength",
            "Day 4: Yoga",
            "Day 5: Cardio",
            "Day 6: Core",
            "Day 7: Rest"
        ]

    with st.expander("View Workout Plan"):
        for day in workout_plan:
            st.write(day)

st.divider()

# -------------------------------------------------
# ExerciseDB Section with GIFs
# -------------------------------------------------
st.subheader("💪 Exercise Demonstrations")

if body_part:
    with st.spinner("Fetching exercises..."):
        exercises = get_exercises(body_part)

    if exercises:
        for ex in exercises:

            gif_url = ex.get("gifUrl")

            # FILTER: Only GIF exercises if enabled
            if show_only_gif and not gif_url:
                continue

            st.markdown(f"### {ex.get('name', 'Unknown').title()}")

            # IMAGE HANDLING
            if gif_url:
                st.image(gif_url, use_container_width=True)
            else:
                st.image(PLACEHOLDER_IMAGE, use_container_width=True)

            st.write(f"**Target Muscle:** {ex.get('target', 'N/A')}")
            st.write(f"**Equipment:** {ex.get('equipment', 'N/A')}")
            st.write("---")
    else:
        st.error("Unable to fetch exercises. Check API key or subscription.")
else:
    st.info("Select a body part from the sidebar to view exercises.")
