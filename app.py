import streamlit as st
import pandas as pd
from utils.intelligent_engine import generate_diet_plan, generate_fitness_tips


from utils.calculations import (
    calculate_bmi,
    bmi_category,
    calculate_bmr,
    calculate_tdee,
    adjust_calories,
    generate_workout_plan
)

from utils.intelligent_engine import (
    generate_diet_plan,
    generate_fitness_tips
)

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="AI Workout & Diet Planner",
    layout="centered"
)

# ------------------ Title ------------------
st.title("🏋️ Personalized Workout & Diet Planner")
st.subheader("Smart fitness and nutrition recommendations")

st.divider()

# ------------------ User Input Form ------------------
with st.form("user_profile_form"):
    st.markdown("### 👤 Personal Details")

    age = st.number_input("Age", min_value=15, max_value=65, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=120, max_value=220)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200)

    st.markdown("### 🎯 Fitness Preferences")

    goal = st.selectbox(
        "Fitness Goal",
        ["Weight Loss", "Muscle Gain", "Maintain Fitness"]
    )

    activity_level = st.selectbox(
        "Activity Level",
        ["Sedentary", "Moderately Active", "Highly Active"]
    )

    diet_pref = st.selectbox(
        "Diet Preference",
        ["Vegetarian", "Non-Vegetarian", "Vegan"]
    )

    workout_days = st.slider(
        "Workout Days per Week",
        min_value=3,
        max_value=6,
        value=4
    )

    submitted = st.form_submit_button("Generate My Plan")

# ------------------ Output Section ------------------
if submitted:
    # ----- Calculations -----
    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)

    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    daily_calories = adjust_calories(tdee, goal)

    workout_plan = generate_workout_plan(workout_days)

    profile = {
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height,
        "goal": goal,
        "diet": diet_pref,
        "activity": activity_level,
        "days": workout_days,
        "calories": round(daily_calories)
    }

    # ----- Display Metrics -----
    st.success("Your personalized plan is ready!")

    st.markdown("### 📊 Body Metrics")
    st.write(f"**BMI:** {bmi} ({bmi_status})")
    st.write(f"**BMR:** {round(bmr)} kcal/day")
    st.write(f"**Daily Calories Needed:** {round(daily_calories)} kcal")
    import pandas as pd
import matplotlib.pyplot as plt

# ----- Charts -----
st.markdown("### 📈 Progress Indicators")

chart_data = pd.DataFrame({
    "Metric": ["BMI", "Calories"],
    "Value": [bmi, daily_calories]
})

fig, ax = plt.subplots()
ax.bar(chart_data["Metric"], chart_data["Value"])
ax.set_ylabel("Value")
ax.set_title("Health Indicators")

st.pyplot(fig)


# ----- Workout Plan -----
st.markdown("### 🏋️ Weekly Workout Plan")
for day in workout_plan:
        st.write("•", day)

    # ----- Diet & Tips -----
diet_plan = generate_diet_plan(profile)
tips = generate_fitness_tips(profile)

st.markdown("### 🥗 Personalized Diet Plan")
st.text(diet_plan)

st.markdown("### 💡 Personalized Fitness Tips")
st.text(tips)
