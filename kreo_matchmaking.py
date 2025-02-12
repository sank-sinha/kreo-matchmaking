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

# --- ULTRA CLEAN UI DESIGN ---
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

        /* Style for the Submit Button */
        .custom-button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }

        .custom-button button {
            background-color: #A578FD !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            padding: 12px 28px !important;
            border: none !important;
            cursor: pointer !important;
            box-shadow: 0px 0px 10px rgba(165, 120, 253, 0.5) !important;
            transition: all 0.3s ease-in-out !important;
        }

        .custom-button button:hover {
            background-color: #8B4CF7 !important;
            box-shadow: 0px 0px 20px rgba(165, 120, 253, 0.8) !important;
            transform: scale(1.05) !important;
        }

        .stTextInput, .stSelectbox, .stMultiselect, .stNumberInput {
            border-radius: 8px !important;
            padding: 10px !important;
            border: 1px solid #A578FD !important;
        }

        .stMarkdown {
            font-weight: bold !important;
            font-size: 16px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎮 Kreo Lobby: Find Your Match")

# --- SESSION STATE ---
if "selected_game" not in st.session_state:
    st.session_state.selected_game = "Valorant"

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

if selected_game != st.session_state.selected_game:
    show_loading()
    st.session_state.selected_game = selected_game

# --- Rank and Weapon Dictionaries ---
game_ranks = {
    "Valorant": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Immortal", "Radiant"],
    "CS:GO": ["Silver", "Gold Nova", "Master Guardian", "Legendary Eagle", "Global Elite"],
    "League of Legends": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Challenger"],
    "Fortnite": ["Casual", "Arena Beginner", "Arena Intermediate", "Arena Expert"],
    "Apex Legends": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Predator"],
    "Other": ["Casual", "Pro", "Hardcore", "Noob"]
}

game_weapons = {
    "Valorant": ["Vandal", "Phantom", "Operator", "Judge"],
    "CS:GO": ["AWP", "AK-47", "M4A1-S", "Desert Eagle"],
    "League of Legends": ["Ability Power Mage", "Attack Damage Carry", "Tank", "Support"],
    "Fortnite": ["Pump Shotgun", "Scar", "Sniper Rifle", "Rocket Launcher"],
    "Apex Legends": ["R-301", "Wingman", "Peacekeeper", "Volt SMG"],
    "Other": ["Default Weapon", "Power Moves", "Basic Gear"]
}

# --- FORM ---
with st.form(key="matchmaking_form", clear_on_submit=False):

    st.subheader("🎮 Gaming Preferences")
    game_rank = st.selectbox("🎖 Your Rank:", game_ranks[selected_game])
    game_weapon = st.selectbox("⚔️ Your Favorite Weapon:", game_weapons[selected_game])

    preferred_time = st.selectbox("⏰ When Do You Usually Play?", ["Morning", "Afternoon", "Evening", "Night", "Flexible"])
    toxicity_level = st.selectbox("😈 Acceptable Level of Toxicity:", ["None - I prefer a chill experience", "Low - Occasional banter is okay", "Moderate - Competitive trash talk is fine", "High - Full-on rage moments acceptable"])

    st.subheader("📝 Personal Information")
    name = st.text_input("🆔 Your Name")
    
    st.markdown("📧 **Make sure you enter correct email address because this will be used to contact you for Round 2**")
    email = st.text_input("Email Address")
    
    st.markdown("🎤 **Make sure you enter correct Discord ID because this will be used for the final showdown later**")
    discord_id = st.text_input("Discord ID")

    phone = st.text_input("📞 Phone Number")
    age = st.number_input("🎂 Age", min_value=13, max_value=99, step=1)
    sex = st.selectbox("⚧ Sex", ["Male", "Female", "Other"])

    favorite_snack = st.selectbox("🍕 Favorite Gaming Snack", ["Chips", "Samosa", "Bhujia", "French Fries", "Chocolate", "Pizza", "Momos"])
    favorite_soda = st.selectbox("🥤 Favorite Soda", ["Thums Up", "Maaza", "Limca", "Mirinda", "Coca Cola", "Pepsi", "Sprite", "Mountain Dew"])

    interests = st.multiselect("💡 Select interests you’d like your gaming partner to share:", ["Anime", "Pets", "Fitness", "Music", "Foodie", "Meme Lover", "Tech Enthusiast"])
    
    hobbies = st.multiselect("🎨 Select Your Hobbies", ["Streaming", "Graphic Design", "Speedrunning", "Esports Watching", "Coding", "Drawing", "Cosplay", "Competitive Gaming"])

    submitted = st.form_submit_button("Submit")

# --- CUSTOM SUBMIT BUTTON OUTSIDE FORM ---
st.markdown('<div class="custom-button"><button type="submit">🔍 Find My Gaming Partner</button></div>', unsafe_allow_html=True)

if submitted:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("❌ Please enter a valid email address.")
    elif not re.match(r"^[0-9]{10}$", phone):
        st.error("❌ Please enter a valid 10-digit phone number.")
    else:
        if USE_GOOGLE_SHEETS:
            sheet.append_row([name, email, discord_id, "+91" + phone, age, sex, game_rank, game_weapon, preferred_time, toxicity_level, ", ".join(interests), ", ".join(hobbies), favorite_snack, favorite_soda])

        st.success("✅ Thanks for submitting! We'll contact you on your email.")
        st.write(f"🎉 **Nice choice! A fellow {selected_game} {game_rank} player might just be your next best teammate!**")
        st.balloons()
