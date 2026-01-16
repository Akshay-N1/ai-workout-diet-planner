def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmr(weight, height_cm, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height_cm - 5 * age + 5
    elif gender == "Female":
        return 10 * weight + 6.25 * height_cm - 5 * age - 161
    else:
        return 10 * weight + 6.25 * height_cm - 5 * age


def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        "Sedentary": 1.2,
        "Moderately Active": 1.55,
        "Highly Active": 1.725
    }
    return round(bmr * activity_multipliers[activity_level], 2)


def adjust_calories(tdee, goal):
    if goal == "Weight Loss":
        return tdee - 500
    elif goal == "Muscle Gain":
        return tdee + 400
    else:
        return tdee
def generate_workout_plan(days):
    plans = {
        3: [
            "Day 1: Full Body",
            "Day 2: Cardio + Core",
            "Day 3: Strength Training"
        ],
        4: [
            "Day 1: Chest + Triceps",
            "Day 2: Back + Biceps",
            "Day 3: Legs",
            "Day 4: Shoulders + Core"
        ],
        5: [
            "Day 1: Chest",
            "Day 2: Back",
            "Day 3: Legs",
            "Day 4: Shoulders",
            "Day 5: Arms + Core"
        ],
        6: [
            "Day 1: Chest",
            "Day 2: Back",
            "Day 3: Legs",
            "Day 4: Shoulders",
            "Day 5: Arms",
            "Day 6: Cardio + Core"
        ]
    }
    return plans.get(days, [])
