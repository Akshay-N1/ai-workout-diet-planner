def generate_diet_plan(profile):
    calories = profile["calories"]
    diet = profile["diet"]
    goal = profile["goal"]

    meals = {
        "Breakfast": int(calories * 0.25),
        "Lunch": int(calories * 0.35),
        "Dinner": int(calories * 0.30),
        "Snacks": int(calories * 0.10),
    }

    veg_foods = {
        "Breakfast": "Oats + Fruit + Nuts",
        "Lunch": "Brown rice + Dal + Vegetables",
        "Dinner": "Roti + Paneer + Salad",
        "Snacks": "Sprouts / Buttermilk"
    }

    nonveg_foods = {
        "Breakfast": "Boiled eggs + Toast",
        "Lunch": "Rice + Chicken curry + Vegetables",
        "Dinner": "Roti + Fish / Chicken",
        "Snacks": "Egg whites / Yogurt"
    }

    foods = veg_foods if diet != "Non-Vegetarian" else nonveg_foods

    plan = ""
    for meal, cal in meals.items():
        plan += f"{meal}: {foods[meal]} (~{cal} kcal)\n"

    return plan


def generate_fitness_tips(profile):
    goal = profile["goal"]
    tips = []

    if goal == "Weight Loss":
        tips = [
            "Maintain a calorie deficit consistently",
            "Include daily walking or cardio",
            "Avoid sugary drinks",
            "Prioritize protein intake",
            "Sleep at least 7 hours"
        ]
    elif goal == "Muscle Gain":
        tips = [
            "Increase protein intake",
            "Train with progressive overload",
            "Rest adequately between workouts",
            "Avoid skipping meals",
            "Track your strength gains"
        ]
    else:
        tips = [
            "Stay physically active daily",
            "Balance strength and cardio",
            "Eat a balanced diet",
            "Stay hydrated",
            "Maintain a regular sleep schedule"
        ]

    return "\n".join([f"- {tip}" for tip in tips])
