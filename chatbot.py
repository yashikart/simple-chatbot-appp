import streamlit as st
import requests

# Set page config once at the very start
st.set_page_config(page_title="🤖 AI Chatbots", page_icon="🤖", layout="centered")

# --- Common API setup ---
API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",  # Ideally, move to st.secrets!
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# --- Sidebar for Navigation ---
st.sidebar.title("Choose a Chatbot")
chatbot_choice = st.sidebar.radio(
    "Select your AI companion:",
    ("Janus 7B Chatbot", "Hugging Face Chatbot")
)

# --- Janus 7B Chatbot Section ---
if chatbot_choice == "Janus 7B Chatbot":
    st.markdown(
        """
        <h1 style='text-align:center; color:#008080; font-family:verdana;'>
            🧠 Chat with Janus 7B Model
        </h1>
        <div style='text-align:center;'>
            <img src="https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif" width="120" alt="Thinking animation"/>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history for Janus
    if "janus_history" not in st.session_state:
        st.session_state.janus_history = []

    def display_janus_chat():
        for chat in st.session_state.janus_history:
            if chat['role'] == 'user':
                st.markdown(f"**You:** {chat['content']}")
            else:
                st.markdown(f"**Janus:** {chat['content']}")

    with st.form(key="janus_form", clear_on_submit=True):
        user_input = st.text_input("Ask Janus anything...", placeholder="Type your question here...")
        submit_button = st.form_submit_button("Send 🧠")

    if submit_button:
        if not user_input.strip():
            st.warning("Please enter a question!")
        else:
            st.session_state.janus_history.append({"role": "user", "content": user_input})

            with st.spinner("Janus is thinking..."):
                payload = {
                    "messages": [{"role": "user", "content": user_input}],
                    "model": "vicgalle/Configurable-Janus-7B:featherless-ai"
                }
                try:
                    response = query(payload)
                    answer = response["choices"][0]["message"]["content"]
                    st.session_state.janus_history.append({"role": "bot", "content": answer})
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### Conversation (Janus):")
    display_janus_chat()

# --- Hugging Face Chatbot Section ---
elif chatbot_choice == "Hugging Face Chatbot":
    st.markdown(
        """
        <h1 style='text-align:center; color:#4B8BBE; font-family:verdana;'>
            🤖 Chat with Hugging Face Model
        </h1>
        <div style='text-align:center;'>
            <img src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif" width="150" alt="Robot Animation"/>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history for Hugging Face Bot
    if "hf_history" not in st.session_state:
        st.session_state.hf_history = []

    def display_hf_chat():
        for chat in st.session_state.hf_history:
            if chat['role'] == 'user':
                st.markdown(f"**You:** {chat['content']}")
            else:
                st.markdown(f"**Bot:** {chat['content']}")

    with st.form(key="hf_chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask me anything 💬", placeholder="Type your question here...")
        submit_button = st.form_submit_button(label="Send 🚀")

    if submit_button:
        if not user_input.strip():
            st.warning("Please enter a question!")
        else:
            st.session_state.hf_history.append({"role": "user", "content": user_input})

            with st.spinner("🤖 Thinking..."):
                payload = {
                    "messages": [{"role": "user", "content": user_input}],
                    "model": "CohereLabs/command-a-reasoning-08-2025:cohere"
                }
                try:
                    response = query(payload)
                    answer = response["choices"][0]["message"]["content"]
                    st.session_state.hf_history.append({"role": "bot", "content": answer})
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### Conversation (Hugging Face):")
    display_hf_chat()
