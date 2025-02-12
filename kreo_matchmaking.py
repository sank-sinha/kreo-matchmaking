import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="🎮 Kreo Lobby: Find Your Match", layout="centered")

# --- GOOGLE SHEETS CONFIGURATION ---
USE_GOOGLE_SHEETS = True  
GOOGLE_SHEET_NAME = "Kreo Matchmaking"
SERVICE_ACCOUNT_FILE = "your-google-key.json"

if USE_GOOGLE_SHEETS:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# --- UI DESIGN FIXES ---
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
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎮 Kreo Lobby: Find Your Match")

# --- SESSION STATE TO HANDLE GAME SELECTION ---
if "selected_game" not in st.session_state:
    st.session_state.selected_game = "Valorant"

# --- LOADING ANIMATION FUNCTION ---
def show_loading():
    with st.spinner("Loading game options..."):
        time.sleep(1.5)

# --- GAME SELECTION ---
st.subheader("🎮 Select Your Game")
selected_game = st.selectbox(
    "🕹 Which Game Do You Primarily Play?",
    ["Valorant", "CS:GO", "League of Legends", "Fortnite", "Apex Legends", "Other"],
    key="selected_game"
)

# --- SHOW LOADING ANIMATION WHEN GAME SELECTION CHANGES ---
if selected_game != st.session_state.selected_game:
    show_loading()
    st.session_state.selected_game = selected_game

# --- Rank and Weapon Dictionaries ---
game_ranks = {
    "Valorant": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Immortal", "Radiant"],
    "CS:GO": ["Silver", "Gold Nova", "Master Guardian", "Legendary Eagle", "Global Elite"],
    "League of Legends": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Challenger"],
    "Fortnite": ["Casual", "Arena Beginner", "Arena Intermediate", "Arena Expert"],
    "Apex Legends": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Predator"]
}

game_weapons = {
    "Valorant": ["Vandal", "Phantom", "Operator", "Judge"],
    "CS:GO": ["AWP", "AK-47", "M4A1-S", "Desert Eagle"],
    "League of Legends": ["Ability Power Mage", "Attack Damage Carry", "Tank", "Support"],
    "Fortnite": ["Pump Shotgun", "Scar", "Sniper Rifle", "Rocket Launcher"],
    "Apex Legends": ["R-301", "Wingman", "Peacekeeper", "Volt SMG"]
}

# --- FORM STARTS HERE ---
with st.form(key="matchmaking_form", clear_on_submit=False):

    # --- GAMING PREFERENCES ---
    st.subheader("🎮 Gaming Preferences")

    st.subheader("📊 Select Your Rank")
    game_rank = st.selectbox("🎖 Your Rank:", game_ranks[st.session_state.selected_game])

    st.subheader("🔫 Select Your Preferred Weapon/Power")
    game_weapon = st.selectbox("⚔️ Your Favorite Weapon:", game_weapons[st.session_state.selected_game])

    preferred_time = st.selectbox("⏰ When Do You Usually Play?", ["Morning", "Afternoon", "Evening", "Night", "Flexible"])
    toxicity_level = st.selectbox("😈 Acceptable Level of Toxicity:", ["None - I prefer a chill experience", "Low - Occasional banter is okay", "Moderate - Competitive trash talk is fine", "High - Full-on rage moments acceptable"])

    # --- PERSONAL INFORMATION ---
    st.subheader("📝 Personal Information")

    name = st.text_input("🆔 Your Name", placeholder="Enter your full name")

    # 📌 EMAIL & DISCORD INFO **VISIBLE, NOT INSIDE (i) BUTTON**
    st.markdown("📧 **Make sure you enter correct email address because this will be used to contact you for Round 2**")
    email = st.text_input("Email Address", placeholder="example@email.com")

    st.markdown("🎤 **Make sure you enter correct Discord ID because this will be used for the final showdown later**")
    discord_id = st.text_input("Discord ID", placeholder="YourDiscord#1234")

    phone = st.text_input("📞 Phone Number", placeholder="Enter your 10-digit number")

    age = st.number_input("🎂 Age", min_value=13, max_value=99, step=1)

    sex = st.selectbox("⚧ Sex", ["Male", "Female", "Other"])

    st.markdown("**🍕 Favorite Gaming Snack**")  
    favorite_snack = st.selectbox("", ["Chips", "Samosa", "Bhujia", "French Fries", "Chocolate", "Pizza", "Momos"])

    st.markdown("**🥤 Favorite Soda**")  
    favorite_soda = st.selectbox("", ["Thums Up", "Maaza", "Limca", "Mirinda", "Coca Cola", "Pepsi", "Sprite", "Mountain Dew"])

    # --- HOBBIES NOW TAB-BASED SELECTION ---
    st.subheader("🎭 Personality & Interests")

    interests = st.multiselect("💡 Select interests you’d like your gaming partner to share:", ["Anime", "Pets", "Fitness", "Music", "Foodie", "Meme Lover", "Tech Enthusiast"])

    hobbies = st.multiselect("🎨 Select Your Hobbies", ["Streaming", "Graphic Design", "Speedrunning", "Esports Watching", "Coding", "Drawing", "Cosplay", "Competitive Gaming"])

    submitted = st.form_submit_button("🔍 Find My Gaming Partner")

if submitted:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("❌ Please enter a valid email address.")
    elif not re.match(r"^[0-9]{10}$", phone):
        st.error("❌ Please enter a valid 10-digit phone number.")
    else:
        if USE_GOOGLE_SHEETS:
            sheet.append_row([name, email, discord_id, "+91" + phone, age, sex, game_rank, game_weapon, preferred_time, toxicity_level, ", ".join(interests), ", ".join(hobbies), favorite_snack, favorite_soda])
        st.success("✅ Thanks for submitting! We'll contact you on your email. Follow us: [Kreosphere](https://www.instagram.com/kreosphere) and stay tuned for further updates.")
        st.balloons()
