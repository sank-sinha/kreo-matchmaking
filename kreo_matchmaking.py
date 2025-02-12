import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
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
        h1, h2, h3, h4, h5, h6 {
            color: black !important;
            font-weight: bold;
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
        .valid {
            border: 2px solid green !important;
        }
        .invalid {
            border: 2px solid red !important;
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
        ["Valorant", "CS:GO", "League of Legends", "Fortnite", "Apex Legends", "Dota", "BGMI", "Free Fire", "Call of Duty", "Other"],
        key="selected_game",
        placeholder="Choose a game"
    )

    # --- Rank and Weapon Dictionaries ---
    game_ranks = {
        "Valorant": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Immortal", "Radiant"],
        "CS:GO": ["Silver", "Gold Nova", "Master Guardian", "Legendary Eagle", "Global Elite"],
        "League of Legends": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Challenger"],
        "Fortnite": ["Casual", "Arena Beginner", "Arena Intermediate", "Arena Expert"],
        "Apex Legends": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Predator"],
        "Dota": ["Herald", "Guardian", "Crusader", "Archon", "Legend", "Ancient", "Divine", "Immortal"],
        "BGMI": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ace", "Conqueror"],
        "Free Fire": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Heroic", "Grand Master"],
        "Call of Duty": ["Recruit", "Veteran", "Elite", "Pro", "Master", "Legendary"],
        "Other": ["Beginner", "Intermediate", "Advanced", "Pro"]
    }

    game_weapons = {
        "Valorant": ["Vandal", "Phantom", "Operator", "Judge"],
        "CS:GO": ["AWP", "AK-47", "M4A1-S", "Desert Eagle"],
        "League of Legends": ["Ability Power Mage", "Attack Damage Carry", "Tank", "Support"],
        "Fortnite": ["Pump Shotgun", "Scar", "Sniper Rifle", "Rocket Launcher"],
        "Apex Legends": ["R-301", "Wingman", "Peacekeeper", "Volt SMG", "R-99"],
        "Dota": ["Blink Dagger", "Divine Rapier", "Black King Bar"],
        "BGMI": ["M416", "AKM", "AWM", "Groza"],
        "Free Fire": ["M1014", "M1887", "UMP", "MP40"],
        "Call of Duty": ["M4", "AK117", "DLQ33", "MSMC"],
        "Other": ["Default Weapon"]
    }

    # --- FORM STARTS HERE ---
    with st.form(key="matchmaking_form", clear_on_submit=False):

        st.subheader("🎮 Gaming Preferences")

        game_rank = st.selectbox("🎖 Your Rank:", game_ranks.get(selected_game, ["Beginner"]), placeholder="Select your rank")

        game_weapon = st.selectbox("⚔️ Your Favorite Weapon:", game_weapons.get(selected_game, ["Default Weapon"]), placeholder="Choose your weapon")

        preferred_time = st.selectbox("⏰ When Do You Usually Play?", ["Morning", "Afternoon", "Evening", "Night", "Flexible"], placeholder="Select time")

        toxicity_level = st.selectbox("😈 Acceptable Level of Toxicity:", ["No trash talks", "Some friendly Banter", "Full Ham M#$%^$"], placeholder="Select toxicity level")

        st.subheader("📝 Personal Information")

        name = st.text_input("🆔 Your Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email Address", placeholder="example@email.com")
        discord_id = st.text_input("🎤 Discord ID", placeholder="YourDiscord#1234")
        phone = st.text_input("📞 Phone Number", placeholder="Enter your 10-digit number")
        age = st.number_input("🎂 Age", min_value=13, max_value=99, step=1)
        sex = st.selectbox("⚧ Sex", ["Male", "Female", "Other"], placeholder="Select your gender")

        submitted = st.form_submit_button("🔍 Find My Gaming Partner")

    if submitted:
        if not name or not email or not discord_id or not phone:
            st.error("❌ All fields are required!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("❌ Please enter a valid email address.")
        elif not re.match(r"^[0-9]{10}$", phone):
            st.error("❌ Please enter a valid 10-digit phone number.")
        else:
            st.session_state.submitted = True
            st.session_state.name = name
            st.session_state.message = f"Hey {name}, You've entered the Kreo Lobby! 🎮"
            witty_messages = {
                "Valorant": "One tap headshots? Your aim better be crispy. 🔫",
                "Apex Legends": "Slide, jump, repeat! Get ready to dominate. 🏆",
            }
            st.session_state.witty_message = witty_messages.get(selected_game, "Your gaming journey begins now! 🚀")
            st.rerun()

else:
    st.markdown(f"<h1>{st.session_state.message}</h1>", unsafe_allow_html=True)
    st.write("We'll match you with your ideal gaming partner and contact you on your email.")
    st.write("_Stay updated by following [Kreosphere](https://www.instagram.com/kreosphere)!_")
    st.markdown(f"<p style='color:grey'>{st.session_state.witty_message}</p>", unsafe_allow_html=True)
