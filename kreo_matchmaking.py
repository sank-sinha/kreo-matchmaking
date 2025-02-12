import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="🎮 Kreo Lobby: Find Your Match", layout="centered")

# --- GOOGLE SHEETS CONFIGURATION ---
USE_GOOGLE_SHEETS = True  
GOOGLE_SHEET_NAME = "Kreo Matchmaking"

if USE_GOOGLE_SHEETS:
    credentials_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(credentials_dict))
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# --- SESSION STATE ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- UI DESIGN ---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;700&display=swap');
        html, body, [class*="st-"] {
            background-color: #ffffff !important;
            color: black !important;
            font-family: 'Josefin Sans', sans-serif;
        }
        .stButton>button {
            background-color: #a578fd !important;
            color: white !important;
            border-radius: 8px;
            font-size: 16px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #8c60e3 !important;
        }
        .info-text {
            color: grey;
            font-size: 14px;
            font-weight: 500;
        }
        .instruction-text {
            font-size: 12px;
            color: grey;
            font-weight: 500;
            margin-bottom: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if not st.session_state.submitted:
    st.title("🎮 Kreo Lobby: Find Your Match")

    # --- GAME SELECTION ---
    st.subheader("🎮 Select Your Game")
    selected_game = st.selectbox(
        "🕹 Which Game Do You Primarily Play?",
        ["Valorant", "CS:GO", "League of Legends", "Fortnite", "Apex Legends", "Dota 2", "BGMI", "Free Fire", "Call of Duty", "Other"],
        key="selected_game"
    )

    # --- Rank and Weapon Dictionaries ---
    game_ranks = {
        "Valorant": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Immortal", "Radiant"],
        "CS:GO": ["Silver", "Gold Nova", "Master Guardian", "Legendary Eagle", "Global Elite"],
        "League of Legends": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Challenger"],
        "Fortnite": ["Casual", "Arena Beginner", "Arena Intermediate", "Arena Expert"],
        "Apex Legends": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Predator"],
        "Dota 2": ["Herald", "Guardian", "Crusader", "Archon", "Legend", "Ancient", "Divine", "Immortal"],
        "BGMI": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Crown", "Ace", "Conqueror"],
        "Free Fire": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Heroic", "Grandmaster"],
        "Call of Duty": ["Rookie", "Veteran", "Elite", "Pro", "Master", "Grandmaster", "Legend"],
        "Other": ["Beginner", "Intermediate", "Advanced", "Pro"]
    }

    game_weapons = {
        "Valorant": ["Vandal", "Phantom", "Operator", "Judge", "Guardian", "Spectre", "Odin"],
        "CS:GO": ["AWP", "AK-47", "M4A1-S", "Desert Eagle", "P90", "Negev", "FAMAS"],
        "League of Legends": ["Ability Power Mage", "Attack Damage Carry", "Tank", "Support", "Bruiser", "Assassin"],
        "Fortnite": ["Pump Shotgun", "Scar", "Sniper Rifle", "Rocket Launcher", "Tactical SMG", "Heavy Shotgun"],
        "Apex Legends": ["R-301", "Wingman", "Peacekeeper", "Volt SMG", "R-99", "Kraber", "CAR SMG"],
        "Dota 2": ["Blink Dagger", "Aghanim's Scepter", "Black King Bar", "Divine Rapier", "Butterfly", "Desolator"],
        "BGMI": ["M416", "AKM", "AWM", "Uzi", "Groza", "Kar98k", "Vector"],
        "Free Fire": ["MP40", "M1014", "AWM", "Groza", "M82B", "SCAR"],
        "Call of Duty": ["M4", "DLQ33", "AK-47", "HVK-30", "Man-O-War", "Chicom"],
        "Other": ["Default Weapon"]
    }

    # --- FORM STARTS HERE ---
    with st.form(key="matchmaking_form", clear_on_submit=False):

        st.subheader("🎮 Gaming Preferences")
        game_rank = st.selectbox("🎖 Your Rank:", game_ranks.get(selected_game, ["Beginner"]))
        game_weapon = st.selectbox("⚔️ Your Favorite Weapon:", game_weapons.get(selected_game, ["Default Weapon"]))
        preferred_time = st.selectbox("⏰ When Do You Usually Play?", ["Morning", "Afternoon", "Evening", "Night", "Flexible"])
        toxicity_level = st.selectbox("😈 Acceptable Level of Toxicity:", ["No trash talks", "Some friendly Banter", "Full Ham M#$%^$"])

        st.subheader("📝 Personal Information")
        name = st.text_input("🆔 Your Name", placeholder="Enter your full name")

        st.markdown('<p class="instruction-text">📌 Ensure this is correct, as it will be used to contact you for Round 2</p>', unsafe_allow_html=True)
        email = st.text_input("📧 Email Address", placeholder="example@email.com")

        st.markdown('<p class="instruction-text">📌 Enter your correct Discord ID, as it will be required for the final showdown</p>', unsafe_allow_html=True)
        discord_id = st.text_input("🎤 Discord ID", placeholder="YourDiscord#1234")

        phone = st.text_input("📞 Phone Number", placeholder="Enter your 10-digit number")
        age = st.number_input("🎂 Age", min_value=13, max_value=99, step=1)
        sex = st.selectbox("⚧ Sex", ["Male", "Female", "Other"])

        submitted = st.form_submit_button("🔍 Find My Gaming Partner")

    if submitted:
        if USE_GOOGLE_SHEETS:
            sheet.append_row([name, email, discord_id, "+91" + phone, age, sex, game_rank, game_weapon, preferred_time, toxicity_level])

        st.session_state.submitted = True
        st.session_state.message = f"### Hey **{name}**, you've entered the Kreo Lobby! 🎮"
        st.session_state.witty_message = random.choice([
            "A sharp strategist, a fearless risk-taker, and an absolute clutch master.",
            "With precision, patience, and passion, you make every move count.",
            "You thrive in chaos, adapt like a pro, and dominate the battlefield.",
            "Gaming isn’t just a hobby for you—it’s a way of life."
        ])
        st.rerun()

else:
    st.title(st.session_state.message)
    st.markdown("We'll match you with your gaming partner and send you an email.\nFollow [Kreosphere](https://www.instagram.com/kreosphere) and stay tuned.")
    st.markdown(f'<p class="info-text">{st.session_state.witty_message}</p>', unsafe_allow_html=True)
