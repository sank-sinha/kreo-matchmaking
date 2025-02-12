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
    # Load credentials from Streamlit Secrets
    credentials_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(credentials_dict))
    
    # Authorize Google Sheets API
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# --- SESSION STATE ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

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
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #8c60e3 !important;
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
        ["Valorant", "CS:GO", "League of Legends", "Fortnite", "Apex Legends", "Other"],
        key="selected_game"
    )

    # --- Rank and Weapon Dictionaries ---
    game_ranks = {
        "Valorant": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Immortal", "Radiant"],
        "CS:GO": ["Silver", "Gold Nova", "Master Guardian", "Legendary Eagle", "Global Elite"],
        "League of Legends": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Challenger"],
        "Fortnite": ["Casual", "Arena Beginner", "Arena Intermediate", "Arena Expert"],
        "Apex Legends": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Predator"],
        "Other": ["Beginner", "Intermediate", "Advanced", "Pro"]
    }

    game_weapons = {
        "Valorant": ["Vandal", "Phantom", "Operator", "Judge"],
        "CS:GO": ["AWP", "AK-47", "M4A1-S", "Desert Eagle"],
        "League of Legends": ["Ability Power Mage", "Attack Damage Carry", "Tank", "Support"],
        "Fortnite": ["Pump Shotgun", "Scar", "Sniper Rifle", "Rocket Launcher"],
        "Apex Legends": ["R-301", "Wingman", "Peacekeeper", "Volt SMG"],
        "Other": ["Default Weapon"]
    }

    # --- FORM STARTS HERE ---
    with st.form(key="matchmaking_form", clear_on_submit=False):

        st.subheader("🎮 Gaming Preferences")

        game_rank = st.selectbox("🎖 Your Rank:", game_ranks.get(selected_game, ["Beginner"]))

        game_weapon = st.selectbox("⚔️ Your Favorite Weapon:", game_weapons.get(selected_game, ["Default Weapon"]))

        preferred_time = st.selectbox("⏰ When Do You Usually Play?", ["Morning", "Afternoon", "Evening", "Night", "Flexible"])
        toxicity_level = st.selectbox("😈 Acceptable Level of Toxicity:", ["None - I prefer a chill experience", "Low - Occasional banter is okay", "Moderate - Competitive trash talk is fine", "High - Full-on rage moments acceptable"])

        st.subheader("📝 Personal Information")

        name = st.text_input("🆔 Your Name", placeholder="Enter your full name")

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

        interests = st.multiselect("💡 Interests:", ["Anime", "Pets", "Fitness", "Music", "Foodie", "Meme Lover", "Tech Enthusiast"])

        hobbies = st.multiselect("🎨 Hobbies:", ["Streaming", "Graphic Design", "Speedrunning", "Esports Watching", "Coding", "Drawing", "Cosplay", "Competitive Gaming"])

        submitted = st.form_submit_button("🔍 Find My Gaming Partner")

    if submitted:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("❌ Please enter a valid email address.")
        elif not re.match(r"^[0-9]{10}$", phone):
            st.error("❌ Please enter a valid 10-digit phone number.")
        else:
            if USE_GOOGLE_SHEETS:
                sheet.append_row([name, email, discord_id, "+91" + phone, age, sex, game_rank, game_weapon, preferred_time, toxicity_level, ", ".join(interests), ", ".join(hobbies), favorite_snack, favorite_soda])

            st.session_state.submitted = True
            st.session_state.message = f"🎉 {name}, you're now part of the Kreo Lobby!"
            st.session_state.witty_message = random.choice([
                f"Looks like a **{game_rank}** with a **{game_weapon}** is ready to conquer! 🚀",
                f"Ah, a fellow **{favorite_snack}** lover! Snacks and gaming – name a better duo! 🍕",
                f"With your skills and a **{favorite_soda}** in hand, you'll be unstoppable! 🥤"
            ])
            st.rerun()

else:
    st.title(st.session_state.message)
    st.subheader(st.session_state.witty_message)
    st.success("✅ Thanks for submitting! We'll contact you on your email. Follow us: [Kreosphere](https://www.instagram.com/kreosphere)")
