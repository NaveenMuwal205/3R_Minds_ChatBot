"""
Main UI module for chatbot
Modern Streamlit-based user interface
"""

import streamlit as st
import controller
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="3rMinds ChatBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ChatUI:
    def __init__(self):
        self.controller = controller.chat_controller
        self.setup_ui()

    def setup_ui(self):
        """Setup the main UI components"""
        # Custom CSS for modern look
        self._inject_custom_css()

        # Sidebar
        self._setup_sidebar()

        # Main chat area
        self._setup_main_chat_area()

    def _inject_custom_css(self):
        """Inject custom CSS for modern styling"""
        st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }

        .stChatMessage {
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .user-message {
            background-color: #007bff;
            color: white;
            margin-left: 20%;
        }

        .assistant-message {
            background-color: #e9ecef;
            color: #333;
            margin-right: 20%;
        }

        .sidebar .sidebar-content {
            background-color: #2c3e50;
        }

        .stTextInput>div>div>input {
            border-radius: 25px;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
        }

        .stButton>button {
            border-radius: 25px;
            padding: 10px 25px;
            border: none;
            background-color: #007bff;
            color: white;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #0056b3;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    def _setup_sidebar(self):
        """Setup sidebar with controls and information"""
        with st.sidebar:
            st.title("🤖 ChatBot Controls")
            st.markdown("---")

            # Session controls
            if st.button("🔄 Clear Conversation", use_container_width=True):
                self.controller.clear_conversation()
                st.rerun()

            if st.button("💾 Save Conversation", use_container_width=True):
                session_name = f"Chat_{datetime.now().strftime('%H:%M:%S')}"
                saved = self.controller.save_conversation(session_name)
                st.success(f"Conversation saved as: {saved['name']}")

            st.markdown("---")

            # Saved conversations
            st.subheader("📁 Saved Chats")
            conversations = self.controller.get_saved_conversations()

            if conversations:
                for conv in conversations[-5:]:  # Show last 5
                    with st.expander(f"💬 {conv['name']}"):
                        st.write(f"Messages: {len(conv['messages'])}")
                        st.write(f"Created: {conv['created_at'][:16]}")
            else:
                st.info("No saved conversations yet")

            st.markdown("---")

            # Bot information
            st.subheader("ℹ️ About")
            st.markdown("""
            **ChatBot Features:**
            - 🤖 AI-powered responses
            - 💬 Real-time chatting
            - 💾 Conversation saving
            - 🎨 Modern UI
            - 🔄 Session management
            """)

    def _setup_main_chat_area(self):
        """Setup the main chat interface"""
        st.title("💬 3rMinds ChatBot")
        st.markdown("Welcome to your 3rMinds chatbot assistant! Start typing below to begin.")

        # Display chat messages
        self._display_chat_messages()

        # Chat input
        self._setup_chat_input()

    def _display_chat_messages(self):
        """Display all chat messages"""
        messages = self.controller.get_session_history()

        for message in messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
                    st.caption(f"Sent at: {message['timestamp'][11:19]}")
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
                    st.caption(f"Sent at: {message['timestamp'][11:19]}")

    def _setup_chat_input(self):
        """Setup chat input area"""
        col1, col2 = st.columns([6, 1])

        with col1:
            user_input = st.chat_input("Type your message here...", key="chat_input")

        with col2:
            if st.button("Send", use_container_width=True):
                if st.session_state.get("chat_input", ""):
                    user_input = st.session_state.chat_input
                    st.session_state.chat_input = ""

        if user_input:
            # Process the message
            response_data = self.controller.process_message(user_input)
            st.rerun()

def main():
    """Main function to run the chatbot UI"""
    # Initialize the UI
    chat_ui = ChatUI()

    # Add some introductory message if no messages exist
    if not chat_ui.controller.get_session_history():
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown("""
            👋 **Hello! I'm your modern chatbot assistant!**

            I can help you with:
            - Answering questions
            - Simple calculations
            - Casual conversation
            - Time information

            Feel free to ask me anything!
            """)

if __name__ == "__main__":
    main()