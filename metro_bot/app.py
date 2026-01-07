import streamlit as st
import google.generativeai as genai

# 1. Streamlit UI Layout
st.set_page_config(page_title="Hyderabad Metro Guide", page_icon="🚇")

# Sidebar for Key Input & Project Info
with st.sidebar:
    st.title("🚇 Configuration")
    
    # --- API KEY INPUT ---
    api_key = st.text_input("Enter Google API Key:", type="password")
    
    st.markdown("---")
    st.title("Project Info")
    st.info("**Project 38:** Metro Passenger Guidance")
    st.write("**Capabilities:**")
    st.write("✅ Ticket Types")
    st.write("✅ Platform Rules")
    st.write("✅ Security Info")
    st.warning("❌ Cannot Sell Tickets")

st.title("Hyderabad Metro Passenger Help 🚆")

# 2. Check for API Key
if not api_key:
    st.info("👋 Welcome! Please enter your **Google API Key** in the sidebar to start the bot.")
    st.stop()  # Stop execution here until key is provided

# 3. Configure Gemini AI
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Invalid API Key. Please check and try again. Error: {e}")
    st.stop()

# 4. Define System Instructions
system_instruction = """
You are the 'Hyderabad Metro Explainer Bot', an AI assistant for L&T Metro Rail Hyderabad. 
Your goal is to guide passengers on rules, ticketing, and safety.

**KNOWLEDGE BASE (Hyderabad Metro Specifics):**
1. **Ticket Types:**
   - **Token:** Single journey coin (valid for the day). Drop at exit gate.
   - **Smart Card:** Contactless card (Nebula/Store Value). 10% discount. Recharge at counter or TSavaari App.
   - **QR Ticket:** Mobile ticket via TSavaari App, Paytm, or WhatsApp. Scan QR at gates.
2. **Security & Rules:**
   - **Prohibited:** Alcohol (open), sharp objects (>4 inches), guns, pets, gas cylinders.
   - **Security Check:** All bags scanned via X-ray; passengers pass through metal detectors (DFMD).
   - **Platform Rules:** Stand behind the Yellow Line. Let passengers exit first. No spitting (Rs. 500 fine).
3. **General Info:**
   - Children below 90cm height travel free.
   - Max time inside station: 30 mins (same station exit) or 180 mins (different station).

**CRITICAL BEHAVIORAL RESTRICTIONS:**
- **NO TICKETING:** You CANNOT book tickets or process payments. If asked, say: "I cannot book tickets. Please visit the station counter, use the TSavaari App, or Paytm."
- **NO REAL-TIME DATA:** You CANNOT provide live train locations. If asked for a schedule, say: "I cannot provide real-time tracking. Trains generally run every 3–10 minutes."
- **SHORT ANSWERS:** Keep responses simple, polite, and under 4-5 sentences for quick reading on mobile.
"""

# 5. Initialize Model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction
)

st.markdown("Ask me about tickets, security, or rules!")

# 6. Chat Session Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User Interaction Logic
user_query = st.chat_input("Ex: How do I buy a token?")

if user_query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # Generate Bot Response
    try:
        chat = model.start_chat(history=[
            {"role": "user", "parts": m["content"]} if m["role"] == "user" 
            else {"role": "model", "parts": m["content"]}
            for m in st.session_state.chat_history[:-1]
        ])
        
        response = chat.send_message(user_query)
        bot_reply = response.text

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"An error occurred: {e}")