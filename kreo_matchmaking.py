import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import re

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
        .info-text {
            color: grey;
            font-size: 14px;
            font-weight: 500;
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
        "Valorant": ["Vandal", "Phantom", "Operator", "Judge"],
        "CS:GO": ["AWP", "AK-47", "M4A1-S", "Desert Eagle"],
        "League of Legends": ["Ability Power Mage", "Attack Damage Carry", "Tank", "Support"],
        "Fortnite": ["Pump Shotgun", "Scar", "Sniper Rifle", "Rocket Launcher"],
        "Apex Legends": ["R-301", "Wingman", "Peacekeeper", "Volt SMG", "R-99"],
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
        email = st.text_input("📧 Email Address", placeholder="example@email.com")
        discord_id = st.text_input("🎤 Discord ID", placeholder="YourDiscord#1234")
        phone = st.text_input("📞 Phone Number", placeholder="Enter your 10-digit number")
        age = st.number_input("🎂 Age", min_value=13, max_value=99, step=1)
        sex = st.selectbox("⚧ Sex", ["Male", "Female", "Other"])

        submitted = st.form_submit_button("🔍 Find My Gaming Partner")

    if submitted:
        errors = []

        if not name.strip():
            errors.append("❌ Name is required.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("❌ Please enter a valid email address.")
        if not discord_id.strip():
            errors.append("❌ Discord ID is required.")
        if not re.match(r"^[0-9]{10}$", phone):
            errors.append("❌ Please enter a valid 10-digit phone number.")

        if errors:
            for error in errors:
                st.error(error)
        else:
            if USE_GOOGLE_SHEETS:
                sheet.append_row([name, email, discord_id, "+91" + phone, age, sex, game_rank, game_weapon, preferred_time, toxicity_level])

            st.session_state.submitted = True
            st.session_state.message = f"### Hey **{name}**, You've entered the Kreo Lobby! 🎮\nWe’ll match you with your ideal gaming partner and contact you on your email. \n\nStay updated by following [Kreosphere](https://www.instagram.com/kreosphere)!"

            game_witty_messages = {
                "Valorant": "One tap headshots? Your aim better be crispy. 🔫",
                "CS:GO": "Flashbangs and flick shots – just don't rush B every round. 🎯",
                "Dota 2": "It's not just a game, it's **Dota 2**. GG or FF? 🏆",
                "Apex Legends": "Sliding into victory with an R-99 – fast and deadly! 🏅",
                "BGMI": "Drop hot, loot fast, and be the last one standing. 🎖️",
                "Call of Duty": "No camping allowed. Rush, frag, repeat. 🔥",
                "Other": "Whatever game it is, you got this! 🎮"
            }

            st.session_state.witty_message = game_witty_messages.get(selected_game, "Get ready to dominate! 🎮")
            st.rerun()

else:
    st.markdown(f"""
    <h1 style="font-size:2.5rem; font-weight:bold;">Hey {st.session_state.name}, You've entered the Kreo Lobby! 🎮</h1>
    <p style="font-size:1.2rem;">We’ll match you with your ideal gaming partner and contact you on your email.</p>
    <p style="font-size:1.2rem;">Stay updated by following <a href="https://www.instagram.com/kreosphere" target="_blank" style="color:#a578fd; text-decoration:none; font-weight:bold;">Kreosphere</a>!</p>
    <p class="info-text" style="color:grey; font-size:1rem;">{st.session_state.witty_message}</p>
    """, unsafe_allow_html=True)

    st.markdown(f'<p class="info-text">{st.session_state.witty_message}</p>', unsafe_allow_html=True)
