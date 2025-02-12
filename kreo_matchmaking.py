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
        st.write("✅ Successfully connected to Google Sheets!")  # Debugging message
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
        # --- USER INFORMATION ---
        name = st.text_input("🆔 Your Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email Address", placeholder="example@email.com")
        discord_id = st.text_input("🎤 Discord ID", placeholder="YourDiscord#1234")
        phone = st.text_input("📞 Phone Number", placeholder="Enter your 10-digit number")

        # --- FORM SUBMISSION BUTTON ---
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
                sheet.append_row([name, email, discord_id, "+91" + phone])
                st.session_state.submitted = True
                st.session_state.user_name = name
                st.session_state.selected_game = "Valorant"  # Placeholder, you can change based on actual input

                st.success("✅ Data successfully recorded in Google Sheets! 🎉")
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

    # --- WITTY STATIC MESSAGES BASED ON GAME ---
    game_messages = {
        "Valorant": "One tap headshots? Your aim better be crispy. 🔫",
        "CS:GO": "Flashbangs, smokes, and perfect spray control. Hope you’re ready! 🎯",
        "League of Legends": "Ganks, split-pushes, and OP plays – time to climb the ladder! 🏆",
        "Fortnite": "Crank those 90s and get ready to build to the sky! 🏗️",
        "Apex Legends": "Slide-jump your way to victory, the Apex games await! 🏅",
        "DOTA": "It's not just a game, it's a way of life. Time to carry your team! 🏹",
        "BGMI": "From hot drops to clutch moments – you were born for this! 🚁",
        "Free Fire": "Booyah! You’re about to light up the battlefield. 🔥",
        "Call of Duty": "Quickscope, drop shot, or a tactical nuke – it’s all in your hands. 🚀",
        "Other": "No matter the game, the grind is real. Let's go! 🎮"
    }

    witty_message = game_messages.get(st.session_state.selected_game, "Get ready to game on and find your perfect duo! 🎮")
    st.markdown(f"<p class='grey-text'>{witty_message}</p>", unsafe_allow_html=True)
