import streamlit as st
import random
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Climate Crisis Simulator", layout="wide")

# --- Difficulty Selection ---
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Normal"

with st.sidebar:
    st.header("Settings")

    difficulty = st.selectbox(
        "Select Difficulty",
        ["Easy", "Normal", "Hard"],
        index=["Easy", "Normal", "Hard"].index(st.session_state.difficulty)
    )
    st.session_state.difficulty = difficulty

    if st.button("🔄 Restart Game"):
        st.session_state.clear()
        st.rerun()

# --- Difficulty Settings ---
difficulty_settings = {
    "Easy": {
        "temperature": 1.0,
        "economy": 80,
        "happiness": 75,
        "environment": 70,
        "event_chance": 0.2
    },
    "Normal": {
        "temperature": 1.2,
        "economy": 70,
        "happiness": 65,
        "environment": 60,
        "event_chance": 0.4
    },
    "Hard": {
        "temperature": 1.5,
        "economy": 60,
        "happiness": 55,
        "environment": 50,
        "event_chance": 0.6
    }
}

settings = difficulty_settings[st.session_state.difficulty]

# --- Initialize Game State ---
if "state" not in st.session_state:
    st.session_state.state = {
        "year": 2025,
        "temperature": settings["temperature"],
        "economy": settings["economy"],
        "happiness": settings["happiness"],
        "environment": settings["environment"],
        "log": []
    }

if "history" not in st.session_state:
    st.session_state.history = []

state = st.session_state.state

# --- Actions ---
actions = {
    "🌞 Build Solar Farms": {
        "environment": +10,
        "economy": -5,
        "temperature": -0.1,
        "happiness": +2
    },
    "🏭 Expand Industry": {
        "economy": +15,
        "environment": -10,
        "temperature": +0.2,
        "happiness": +5
    },
    "🚌 Improve Public Transport": {
        "environment": +5,
        "economy": -3,
        "temperature": -0.05,
        "happiness": +8
    }
}

# --- Events ---
events = [
    ("🔥 Heatwave", {"happiness": -10, "temperature": +0.2}),
    ("🌱 Green Tech Breakthrough", {"environment": +15, "economy": +5}),
    ("🌊 Flooding", {"economy": -10, "happiness": -5}),
    ("✊ Climate Protest", {"happiness": -5, "environment": +5})
]

# --- Apply Effects ---
def apply_effect(effect):
    multiplier = 1.0
    if st.session_state.difficulty == "Hard":
        multiplier = 1.3
    elif st.session_state.difficulty == "Easy":
        multiplier = 0.8

    for key in effect:
        state[key] += effect[key] * multiplier

# --- AI Advisor ---
def get_ai_advice(state):
    advice = []

    if state["temperature"] > 2:
        advice.append("🌡️ Temperature is too high — invest in green energy.")

    if state["economy"] < 40:
        advice.append("💰 Economy is weak — consider boosting industry.")

    if state["happiness"] < 40:
        advice.append("😊 People are unhappy — improve public services.")

    if state["environment"] < 40:
        advice.append("🌿 Environment is suffering — reduce pollution.")

    if not advice:
        return "✅ You're doing well! Maintain balance across all sectors."

    return " ".join(advice)

# --- Title ---
st.title("🌍 Climate Crisis Simulator")
st.caption(f"Difficulty: {st.session_state.difficulty}")

# --- Metrics ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Temperature (°C)", round(state["temperature"], 2))
col2.metric("💰 Economy", int(state["economy"]))
col3.metric("😊 Happiness", int(state["happiness"]))
col4.metric("🌿 Environment", int(state["environment"]))

# --- Warnings ---
if state["temperature"] > 2:
    st.warning("⚠️ Temperature is reaching dangerous levels!")

if state["economy"] < 30:
    st.warning("💸 Economy is struggling!")

if state["happiness"] < 30:
    st.warning("😡 Public unrest is growing!")

if state["environment"] < 30:
    st.warning("🌪️ Environment is degrading!")

st.markdown("---")

# --- Layout ---
left, right = st.columns([1, 2])

# LEFT: Actions + AI
with left:
    st.subheader(f"📅 Year: {state['year']}")
    st.markdown("### Choose a Policy")

    for action_name, effect in actions.items():
        if st.button(action_name, use_container_width=True):
            apply_effect(effect)
            state["year"] += 1
            state["log"].append(f"You chose: {action_name}")

            # Save history
            st.session_state.history.append({
                "year": state["year"],
                "temperature": state["temperature"],
                "economy": state["economy"]
            })

            # Random event
            if random.random() < settings["event_chance"]:
                event_name, event_effect = random.choice(events)
                apply_effect(event_effect)
                state["log"].append(f"⚡ Event: {event_name}")

    # --- AI Advisor UI ---
    st.markdown("---")
    st.subheader("🤖 AI Policy Advisor")

    if st.button("Get Advice"):
        advice = get_ai_advice(state)
        st.info(advice)

# RIGHT: Chart
with right:
    st.subheader("📈 Climate Trends")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        df = df.set_index("year")
        st.line_chart(df)

# --- Game Over ---
if state["temperature"] > 3:
    st.error("🔥 Game Over: Climate catastrophe!")
elif state["economy"] <= 0:
    st.error("💸 Game Over: Economy collapsed!")
elif state["happiness"] <= 0:
    st.error("😡 Game Over: Citizens revolted!")
elif state["year"] >= 2040:
    st.success("🎉 You successfully balanced climate and economy!")

# --- Log ---
st.markdown("---")
st.subheader("📜 Event Log")

for log in reversed(state["log"][-8:]):
    st.write(log)

