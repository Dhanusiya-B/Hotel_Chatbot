import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY is missing. Please configure it in Streamlit Secrets.")
    st.stop()
st.set_page_config(page_title="Hotel Assistant", page_icon="🏨", layout="centered")


# ---------------------------------------------------------------------------
# Premium Black + Luxury Red styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
 
/* Hide default Streamlit chrome for a cleaner, custom look */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
 
.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(177, 18, 38, 0.10) 0%, transparent 50%),
        #080808;
}
 
/* ---------------- Header ---------------- */
.hotel-header {
    text-align: center;
    padding: 2.25rem 1rem 1.5rem 1rem;
    margin-bottom: 1rem;
}
 
.hotel-header .eyebrow {
    display: block;
    font-size: 0.68rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #8a8a8a;
    font-weight: 500;
    margin-bottom: 0.7rem;
}
 
.hotel-header h1 {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    color: #F5F5F5;
    font-size: 2.6rem;
    margin: 0;
    letter-spacing: 0.5px;
}
 
.hotel-header p {
    color: #9c9c9c;
    font-size: 0.98rem;
    font-weight: 300;
    margin-top: 0.6rem;
}
 
.hotel-header::after {
    content: "";
    display: block;
    width: 70px;
    height: 2px;
    margin: 1.5rem auto 0 auto;
    background: linear-gradient(90deg, #B11226, #E01E37);
    border-radius: 2px;
}
 
/* ---------------- Empty state ---------------- */
.empty-state {
    text-align: center;
    padding: 1.5rem 1rem 0.5rem 1rem;
    animation: fadeIn 0.5s ease;
}
 
.empty-state-icon {
    font-size: 2.1rem;
    margin-bottom: 0.6rem;
}
 
.empty-state h3 {
    font-family: 'Manrope', sans-serif;
    color: #F5F5F5;
    font-weight: 700;
    font-size: 1.25rem;
    margin: 0 0 0.4rem 0;
}
 
.empty-state p {
    color: #8f8f8f;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}
 
/* Suggested question chips (st.button) */
[data-testid="stButton"] button {
    background-color: #151515 !important;
    color: #e6e6e6 !important;
    border: 1px solid rgba(177, 18, 38, 0.35) !important;
    border-radius: 12px !important;
    padding: 0.7rem 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    margin-bottom: 0.6rem !important;
}
 
[data-testid="stButton"] button:hover {
    border-color: #E01E37 !important;
    background-color: #1a1010 !important;
    color: #ffffff !important;
    box-shadow: 0 0 0 1px rgba(224, 30, 55, 0.25), 0 6px 16px rgba(177, 18, 38, 0.18) !important;
    transform: translateY(-1px);
}
 
/* ---------------- Chat messages ---------------- */
[data-testid="stChatMessage"] {
    background: #151515;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 0.55rem 0.4rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    animation: fadeIn 0.35s ease;
}
 
/* Messages alternate user -> assistant, so odd/even gives each role its own tone */
[data-testid="stChatMessage"]:nth-of-type(odd) {
    background: #181113;
    border: 1px solid rgba(177, 18, 38, 0.35);
    border-right: 2px solid #E01E37;
}
 
[data-testid="stChatMessage"]:nth-of-type(even) {
    background: #121212;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-left: 2px solid #B11226;
}
 
[data-testid="stChatMessage"] p {
    color: #ECECEC;
    font-size: 0.96rem;
    line-height: 1.6;
}
 
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
 
/* ---------------- Bottom bar container (the strip the input sits in) ---------------- */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer,
[data-testid="stChatInputContainer"] {
    background: #080808 !important;
}
 
[data-testid="stBottom"] > div {
    background: #080808 !important;
    box-shadow: none !important;
    border-top: 1px solid rgba(177, 18, 38, 0.12) !important;
}
 
/* ---------------- Chat input (glassmorphism red) ---------------- */
[data-testid="stChatInput"] {
    background: rgba(120, 15, 30, 0.22) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(224, 30, 55, 0.35) !important;
    border-radius: 30px !important;
    box-shadow: 0 8px 32px rgba(177, 18, 38, 0.25), 0 8px 30px rgba(0, 0, 0, 0.45) !important;
}
 
/* Streamlit wraps the textarea in its own div(s) that default to white — make them transparent */
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] div {
    background: transparent !important;
}
 
[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #f5f0f0 !important;
    border-radius: 26px !important;
    border: none !important;
    padding: 0.8rem 1.2rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: box-shadow 0.2s ease;
}
 
[data-testid="stChatInput"] textarea:focus {
    box-shadow: none !important;
}
 
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #E01E37, #B11226) !important;
    border-radius: 50% !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
 
[data-testid="stChatInput"] button:hover {
    transform: scale(1.06);
    box-shadow: 0 0 14px rgba(224, 30, 55, 0.55) !important;
}
 
[data-testid="stChatInput"] button svg {
    fill: #ffffff !important;
}
 
 
::placeholder {
    color: #6b6b6b !important;
}
 
/* ---------------- Scrollbar ---------------- */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #080808;
}
::-webkit-scrollbar-thumb {
    background: rgba(177, 18, 38, 0.45);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(224, 30, 55, 0.6);
}
 
/* ---------------- Responsive ---------------- */
@media (max-width: 640px) {
    .hotel-header h1 { font-size: 2rem; }
    .hotel-header p { font-size: 0.88rem; }
    .empty-state h3 { font-size: 1.1rem; }
    [data-testid="stButton"] button { font-size: 0.8rem !important; padding: 0.6rem 0.75rem !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hotel-header">
    <span class="eyebrow">Boutique Digital Concierge</span>
    <h1>🏨 Hotel Assistant</h1>
    <p>Ask me anything about your stay — I'm here to help, day or night.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Load knowledge base (same logic as notebook, just read from disk directly)
# ---------------------------------------------------------------------------
@st.cache_data
def load_kb():
    with open("hotel_data.json", "r", encoding="utf-8") as f:
        return f.read()

kb = load_kb()

# ---------------------------------------------------------------------------
# System prompt (unchanged logic)
# ---------------------------------------------------------------------------
prompt = f"""
 You are Hotel customer care executive. your job is to provide answers to the questions asked by the customer,
 you shoukd answer them in polite. if there any questions out of the kb say you didnt have that info, only refer the kb and provide the response.
{kb}
"""

# ---------------------------------------------------------------------------
# Gemini client + chat session (unchanged logic)
# ---------------------------------------------------------------------------
  # <-- your Gemini API key
api_key= GOOGLE_API_KEY
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=GOOGLE_API_KEY)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.6-flash",
        config={"system_instruction": prompt},
    )

# ---------------------------------------------------------------------------
# Chat state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

SUGGESTED_QUESTIONS = [
    "Is breakfast included?",
    "What time is check-in and check-out?",
    "Do you have a gym or spa?",
    "Is parking available on-site?",
]

# ---------------------------------------------------------------------------
# UI: welcome empty-state with suggestions (only before the first message),
# otherwise render the ongoing conversation. Nothing about how a question is
# sent to Gemini changes — a suggestion click just supplies the input text.
# ---------------------------------------------------------------------------
suggested_click = None

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🥂</div>
        <h3>Welcome to your stay</h3>
        <p>I'm your digital concierge — ask about amenities, dining, check-in and more.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, q in enumerate(SUGGESTED_QUESTIONS):
        with cols[i % 2]:
            if st.button(q, key=f"suggestion_{i}", use_container_width=True):
                suggested_click = q
else:
    for msg in st.session_state.messages:
        avatar = "🧑" if msg["role"] == "user" else "🏨"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

typed_input = st.chat_input("Type your question here...")
user_input = typed_input or suggested_click

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🏨"):
        with st.spinner("Typing..."):
            response = st.session_state.chat.send_message(user_input)
            st.markdown(response.text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )