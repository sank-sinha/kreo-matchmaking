import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="🎮 Kreo Lobby: Find Your Match", layout="centered")

# --- GOOGLE SHEETS CONFIGURATION ---
USE_GOOGLE_SHEETS = True  
GOOGLE_SHEET_NAME = "Kreo Matchmaking"

try:
    if USE_GOOGLE_SHEETS:
        credentials_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(credentials_dict))
        client = gspread.authorize(creds)
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
except Exception as e:
    st.error("❌ Failed to connect to Google Sheets. Check your API credentials or permissions.")
    st.stop()

# --- SESSION STATE ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- STYLING ---
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
        .grey-text {
            color: grey;
            font-size: 14px;
            font-style: italic;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- FORM ---
if not st.session_state.submitted:
    st.title("🎮 Kreo Lobby: Find Your Match")

    with st.form(key="matchmaking_form", clear_on_submit=False):
        # --- GAME SELECTION ---
        st.subheader("🎮 Select Your Game")
        selected_game = st.selectbox(
            "🕹 Which Game Do You Primarily Play?",
            ["Valorant", "CS:GO", "League of Legends", "Fortnite", "Apex Legends", "DOTA", "BGMI", "Free Fire", "Call of Duty", "Other"],
            key="selected_game"
        )

        # --- Rank and Weapon Dictionaries ---
        game_ranks = {
            "Valorant": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Immortal", "Radiant"],
            "CS:GO": ["Silver", "Gold Nova", "Master Guardian", "Legendary Eagle", "Global Elite"],
            "League of Legends": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Challenger"],
            "Fortnite": ["Casual", "Arena Beginner", "Arena Intermediate", "Arena Expert"],
            "Apex Legends": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Predator"],
            "DOTA": ["Herald", "Guardian", "Crusader", "Archon", "Legend", "Ancient", "Divine", "Immortal"],
            "BGMI": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ace", "Conqueror"],
            "Free Fire": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Heroic", "Grandmaster"],
            "Call of Duty": ["Rookie", "Veteran", "Elite", "Pro", "Master", "Grandmaster", "Legendary"],
            "Other": ["Beginner", "Intermediate", "Advanced", "Pro"]
        }

        game_weapons = {
            "Valorant": ["Vandal", "Phantom", "Operator", "Judge"],
            "CS:GO": ["AWP", "AK-47", "M4A1-S", "Desert Eagle"],
            "League of Legends": ["Ability Power Mage", "Attack Damage Carry", "Tank", "Support"],
            "Fortnite": ["Pump Shotgun", "Scar", "Sniper Rifle", "Rocket Launcher"],
            "Apex Legends": ["R-301", "Wingman", "Peacekeeper", "Volt SMG", "R-99"],
            "DOTA": ["Blink Dagger", "Aghanim's Scepter", "Black King Bar", "Divine Rapier"],
            "BGMI": ["M416", "AKM", "AWM", "Uzi"],
            "Free Fire": ["MP40", "M1014", "AWM", "Groza"],
            "Call of Duty": ["M4", "DLQ33", "AK-47", "HVK-30"],
            "Other": ["Default Weapon"]
        }

        # --- GAMING PREFERENCES ---
        st.subheader("🎮 Gaming Preferences")
        game_rank = st.selectbox("🎖 Your Rank:", game_ranks.get(selected_game, ["Beginner"]))
        game_weapon = st.selectbox("⚔️ Your Favorite Weapon:", game_weapons.get(selected_game, ["Default Weapon"]))
        preferred_time = st.selectbox("⏰ When Do You Usually Play?", ["Morning", "Afternoon", "Evening", "Night", "Flexible"])
        toxicity_level = st.selectbox("😈 Acceptable Level of Toxicity:", ["No trash talks", "Some friendly Banter", "Full Ham M#$%^$"])

        # --- PERSONAL INFORMATION ---
        st.subheader("📝 Personal Information")
        name = st.text_input("🆔 Your Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email Address", placeholder="example@email.com")
        discord_id = st.text_input("🎤 Discord ID", placeholder="YourDiscord#1234")
        phone = st.text_input("📞 Phone Number", placeholder="Enter your 10-digit number")
        age = st.number_input("🎂 Age", min_value=13, max_value=99, step=1)
        sex = st.selectbox("⚧ Sex", ["Male", "Female", "Other"])

        submitted = st.form_submit_button("🔍 Find My Gaming Partner")

    # --- VALIDATION CHECKS ---
    if submitted:
        if not name.strip():
            st.error("❌ Name is required!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("❌ Invalid email format! Please enter a valid email.")
        elif not re.match(r"^[0-9]{10}$", phone):
            st.error("❌ Invalid phone number! Enter a 10-digit phone number.")
        else:
            try:
                # --- WRITE TO GOOGLE SHEETS ---
                sheet.append_row([name, email, discord_id, "+91" + phone, age, sex, game_rank, game_weapon, preferred_time, toxicity_level])
                st.session_state.submitted = True
                st.session_state.user_name = name
                st.session_state.selected_game = selected_game
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to write to Google Sheets: {e}")
                st.stop()

# --- SUCCESS PAGE ---
else:
    st.markdown(f"""
    <h1 style="font-size:2.5rem; font-weight:bold;">Hey {st.session_state.user_name}, You've entered the Kreo Lobby! 🎮</h1>
    <p style="font-size:1.2rem;">We’ll match you with your ideal gaming partner and contact you on your email.</p>
    <p style="font-size:1.2rem;">Stay updated by following <a href='https://www.instagram.com/kreosphere' target='_blank'>Kreosphere</a>!</p>
    """, unsafe_allow_html=True)

    st.markdown(f"<p class='grey-text'>Time to squad up and make some epic gaming memories. GG WP! 🎮</p>", unsafe_allow_html=True)
