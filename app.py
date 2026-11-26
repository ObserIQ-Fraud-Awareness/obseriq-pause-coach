import streamlit as st

st.set_page_config(
    page_title="ObserIQ Pause Coach",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# === Calm, high-contrast styling ===
st.markdown("""
<style>
    .stApp {
        background-color: #F8F9FA;
        color: #102A43;
    }
    
    h1, h2, h3 {
        color: #102A43;
        font-weight: 700;
    }
    
    .big-button {
        font-size: 2.2rem !important;
        padding: 1.5rem 3rem !important;
        background-color: #2EC4B6;
        color: white;
        border: none;
        border-radius: 20px;
        width: 100%;
        margin: 1.5rem 0;
    }
    
    .warning-text {
        font-size: 1.35rem;
        line-height: 1.6;
        color: #102A43;
    }
    
    .action-box {
        background-color: #E8F5E9;
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        border-left: 8px solid #2EC4B6;
    }
    
    .script-box {
        background-color: #FFF3E0;
        padding: 1.75rem;
        border-radius: 16px;
        font-size: 1.25rem;
        line-height: 1.6;
        border-left: 8px solid #FF9800;
    }
    
    .next-step {
        font-size: 1.25rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }
    
    .calm-header {
        font-size: 2.8rem;
        line-height: 1.2;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .small-note {
        font-size: 1rem;
        color: #5E6A7C;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def reset():
    st.session_state.clear()
    st.rerun()


# =====================
# STATE MANAGEMENT
# =====================
if "step" not in st.session_state:
    st.session_state.step = "start"

if "answers" not in st.session_state:
    st.session_state.answers = {}


# =====================
# START SCREEN
# =====================
if st.session_state.step == "start":
    st.markdown("<h1 class='calm-header'>Feeling rushed?<br>Let’s pause together.</h1>", unsafe_allow_html=True)
    
    st.markdown(
        "<p style='font-size:1.35rem; text-align:center; max-width:600px; margin:0 auto;'>"
        "Scammers win when you act fast.<br>"
        "Take 60 seconds before you pay, click, or share.</p>",
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("PAUSE — Tap to start", key="start_btn", use_container_width=True):
        st.session_state.step = "questions"
        st.rerun()
    
    st.markdown(
        "<p class='small-note'>Someone is on the phone now • Works on any phone browser</p>",
        unsafe_allow_html=True
    )


# =====================
# GUIDED QUESTIONS
# =====================
elif st.session_state.step == "questions":
    st.markdown("<h2 style='text-align:center;'>Quick Pause Questions</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.1rem;'>Answer honestly. This helps us give you the right words and steps.</p>", unsafe_allow_html=True)
    
    questions = [
        {
            "id": "payment",
            "q": "How are they asking you to pay?",
            "options": [
                "Gift cards or iTunes cards",
                "Bank transfer or e-transfer",
                "Cash or cryptocurrency",
                "Not sure / other"
            ]
        },
        {
            "id": "secret",
            "q": "Are they telling you to keep this secret?",
            "options": ["Yes", "No", "Not sure"]
        },
        {
            "id": "urgency",
            "q": "Are they saying you must act right now?",
            "options": ["Yes", "No", "Not sure"]
        },
        {
            "id": "who",
            "q": "Who do they say they are?",
            "options": [
                "Police or government",
                "Bank or credit card company",
                "Family member in trouble",
                "Tech support or computer company",
                "Other / Not sure"
            ]
        }
    ]
    
    for i, q in enumerate(questions):
        st.markdown(f"**{q['q']}**")
        ans = st.radio(
            label="",
            options=q["options"],
            key=f"q_{q['id']}",
            horizontal=False
        )
        st.session_state.answers[q["id"]] = ans
        st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Go Back", use_container_width=True):
            st.session_state.step = "start"
            st.rerun()
    
    with col2:
        if st.button("Show My Next Steps", type="primary", use_container_width=True):
            st.session_state.step = "result"
            st.rerun()


# =====================
# RESULT SCREEN
# =====================
elif st.session_state.step == "result":
    st.markdown("<h2 style='text-align:center; color:#2EC4B6;'>Stop. This has warning signs.</h2>", unsafe_allow_html=True)
    
    # Personalized script based on answers
    payment = st.session_state.answers.get("payment", "")
    secret = st.session_state.answers.get("secret", "")
    urgency = st.session_state.answers.get("urgency", "")
    who = st.session_state.answers.get("who", "")
    
    script = "I don’t make payments over the phone. I’ll call my bank directly."
    
    if "gift cards" in payment.lower() or "iTunes" in payment.lower():
        script = "I don’t buy gift cards for anyone. I’m hanging up now."
    elif "bank" in payment.lower() or "transfer" in payment.lower():
        script = "I only pay through my bank app. I’m not doing this over the phone."
    elif "cash" in payment.lower() or "crypto" in payment.lower():
        script = "I don’t send cash or cryptocurrency. I’m hanging up."
    
    if secret.lower() == "yes":
        script = "I don’t keep secrets from my family. I’m going to talk to them first."
    
    if urgency.lower() == "yes":
        script = "I don’t make decisions under pressure. I’m hanging up."
    
    st.markdown("<div class='script-box'>", unsafe_allow_html=True)
    st.markdown("**Say this out loud, then hang up:**")
    st.markdown(f"<h3 style='margin-top:1rem;'>{script}</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("**Then take these steps:**")
    
    with st.container():
        st.markdown("<div class='action-box'>", unsafe_allow_html=True)
        
        st.markdown("**1. Stop all contact**")
        st.markdown("Hang up or close the message. Do not reply.")
        
        st.markdown("**2. Call your bank or credit card company**")
        st.markdown("Use the real phone number on the back of your card.")
        
        st.markdown("**3. Report it**")
        st.markdown("Call the Canadian Anti-Fraud Centre: **1-888-495-8501**")
        
        st.markdown("**4. Tell someone you trust**")
        st.markdown("Call a family member or friend right now.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Over", use_container_width=True):
            reset()
    
    with col2:
        if st.button("I Need More Help", type="primary", use_container_width=True):
            st.session_state.step = "more_help"
            st.rerun()


# =====================
# MORE HELP SCREEN
# =====================
elif st.session_statestep == "more_help":
    st.header("You’re not alone. Here’s what to do next.")
    
    st.markdown("<div class='action-box'>", unsafe_allow_html=True)
    
    st.markdown("### If you already sent money or gave information")
    st.markdown("- Call your bank immediately using the number on the back of your card")
    st.markdown("- Report to the Canadian Anti-Fraud Centre: **1-888-495-8501**")
    st.markdown("- Change your passwords if you shared login details")
    st.markdown("- Tell a trusted person what happened")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='action-box'>", unsafe_allow_html=True)
    
    st.markdown("### If you think it was a scam but haven’t acted yet")
    st.markdown("- You did the right thing by pausing")
    st.markdown("- Share this tool with someone else who might be in the same situation")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Back to Pause", use_container_width=True):
        reset()
