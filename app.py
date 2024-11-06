import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Set up Streamlit app
st.set_page_config(page_title="🏋️ Workout Tracker & Planner", page_icon="🏋️")

# Initialize session state for data storage
if 'workouts' not in st.session_state:
    st.session_state.workouts = pd.DataFrame(columns=["Date", "Exercise", "Duration (mins)", "Reps", "Weight (lbs)"])

# Sidebar for workout input
st.sidebar.header("📝 Log Your Workout")

# Predefined options
exercise_options = ["Squats", "Deadlifts", "Bench Press", "Running", "Cycling", "Yoga", "Swimming", "Other"]
duration_options = [15, 30, 45, 60, 90]  # Duration in minutes
rep_options = [5, 10, 15, 20]  # Repetitions
weight_options = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # Weight in lbs

# Workout input form with dropdowns
exercise = st.sidebar.selectbox("Exercise Name", exercise_options)
duration = st.sidebar.selectbox("Duration (mins)", duration_options)
reps = st.sidebar.selectbox("Repetitions", rep_options)
weight = st.sidebar.selectbox("Weight (lbs)", weight_options)

if st.sidebar.button("✅ Log Workout"):
    new_workout = pd.DataFrame({
        "Date": [datetime.date.today()],
        "Exercise": [exercise],
        "Duration (mins)": [duration],
        "Reps": [reps],
        "Weight (lbs)": [weight]
    })
    st.session_state.workouts = pd.concat([st.session_state.workouts, new_workout], ignore_index=True)
    st.success(f"Workout logged: {exercise} for {duration} minutes, {reps} reps at {weight} lbs.")

# Display logged workouts
st.header("📊 Workout Log")
if not st.session_state.workouts.empty:
    st.write(st.session_state.workouts)

    # Progress Tracking
    st.subheader("📈 Progress Over Time")
    
    # Calculate total workouts per exercise
    workout_summary = st.session_state.workouts.groupby('Exercise').sum().reset_index()
    
    # Bar chart for workouts
    plt.figure(figsize=(10, 5))
    plt.bar(workout_summary['Exercise'], workout_summary['Duration (mins)'], color='blue')
    plt.title("Total Workout Duration by Exercise")
    plt.xlabel("Exercise")
    plt.ylabel("Total Duration (mins)")
    st.pyplot(plt)
    
    # Optional: Add a feature to set goals and track them
    st.subheader("🏆 Set Fitness Goals")
    goal = st.text_input("Goal", placeholder="E.g., Run 5km in under 30 minutes")
    if st.button("✅ Set Goal"):
        if goal:
            st.session_state.goal = goal
            st.success(f"Goal set: {goal}")

# Weekly Planner (simple example)
st.sidebar.header("📅 Weekly Workout Planner")
planned_workouts = st.sidebar.multiselect("Select your workouts for the week", st.session_state.workouts['Exercise'].unique())

if st.sidebar.button("📅 Save Weekly Plan"):
    if planned_workouts:
        st.session_state.weekly_plan = planned_workouts
        st.success(f"Weekly plan saved: {', '.join(planned_workouts)}")
    else:
        st.warning("Please select at least one workout.")

# Display weekly plan
st.header("🗓️ Weekly Plan")
if 'weekly_plan' in st.session_state:
    st.write(", ".join(st.session_state.weekly_plan))

# Footer note
st.info("Note: Track your progress consistently and stay motivated! 💪")
