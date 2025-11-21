import streamlit as st
import google.generativeai as genai
import os

# Set page configuration
st.set_page_config(
    page_title="Chat with Gemini",
    page_icon="🤖",
    layout="centered"
)

# Title and description
st.title("💬 Chat with Gemini")
st.markdown("Chat with Google's Gemini AI model. Type your messages below!")

# Sidebar for API key configuration
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Enter your Google API Key:", type="password")
    
    if api_key:
        os.environ['GOOGLE_API_KEY'] = api_key
        try:
            genai.configure(api_key=api_key)
            st.success("✅ API Key configured successfully!")
        except Exception as e:
            st.error(f"❌ Error configuring API: {e}")
    else:
        st.info("👆 Please enter your Google API Key to start chatting")

# Initialize the model and chat session
@st.cache_resource
def load_model():
    if 'GOOGLE_API_KEY' in os.environ:
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            return model.start_chat()
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
            return None
    return None

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check if API key is configured
    if not api_key:
        st.error("🚫 Please configure your API key in the sidebar first!")
        st.stop()
    
    # Get chat session
    chat = load_model()
    if chat is None:
        st.error("❌ Failed to initialize chat session. Please check your API key.")
        st.stop()
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat.send_message(prompt)
                response_text = response.text
                st.markdown(response_text)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Clear chat button
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Instructions in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 How to use:")
    st.markdown("""
    1. Enter your Google API key
    2. Start typing messages in the chat
    3. Click 'Clear Chat' to start over
    4. Type 'exit' to end the conversation
    """)
    
    st.markdown("### 🔒 Security Note:")
    st.markdown("Your API key is only stored in this session and won't be saved.")
