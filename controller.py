"""
Controller module for chatbot
Handles business logic and coordination between data and UI
"""

from data import chat_data
import re
import random
from typing import Dict, List, Any

class ChatController:
    def __init__(self):
        self.responses = {
            "greeting": [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Hey! Nice to see you. How can I help?"
            ],
            "farewell": [
                "Goodbye! Have a great day!",
                "See you later! Feel free to come back anytime.",
                "Bye! It was nice chatting with you."
            ],
            "help": [
                "I can help you with various tasks. You can ask me about weather, time, calculations, or just chat!",
                "I'm here to assist you with information and conversations. What do you need help with?",
                "I can answer questions, help with calculations, or just have a friendly chat!"
            ],
            "default": [
                "I'm not sure I understand. Could you rephrase that?",
                "That's interesting! Could you tell me more?",
                "I'm still learning. Could you explain that differently?"
            ]
        }

    def process_message(self, user_input: str) -> Dict[str, Any]:
        """Process user input and return bot response"""
        # Add user message to data
        user_message = chat_data.add_message("user", user_input)

        # Generate bot response
        bot_response = self._generate_response(user_input)

        # Add bot response to data
        bot_message = chat_data.add_message("assistant", bot_response)

        return {
            "user_message": user_message,
            "bot_message": bot_message,
            "session_messages": chat_data.get_session_messages()
        }

    def _generate_response(self, user_input: str) -> str:
        """Generate appropriate response based on user input"""
        input_lower = user_input.lower()

        # Greeting detection
        if any(word in input_lower for word in ['hello', 'hi', 'hey', 'hola']):
            return random.choice(self.responses["greeting"])

        # Farewell detection
        elif any(word in input_lower for word in ['bye', 'goodbye', 'see you', 'exit']):
            return random.choice(self.responses["farewell"])

        # Help request
        elif any(word in input_lower for word in ['help', 'what can you do', 'capabilities']):
            return random.choice(self.responses["help"])

        # Question about name
        elif any(word in input_lower for word in ['your name', 'who are you']):
            return "I'm a modern chatbot assistant! You can call me ChatAI."

        # Time question
        elif 'time' in input_lower:
            from datetime import datetime
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"

        # Math calculation
        elif re.search(r'\d+[\+\-\*\/]\d+', user_input):
            try:
                # Simple math evaluation (be careful with eval in production)
                result = eval(user_input)
                return f"The answer is: {result}"
            except:
                return "I couldn't calculate that. Please check your math expression."

        # Default response
        else:
            return random.choice(self.responses["default"])

    def get_session_history(self) -> List[Dict]:
        """Get current session message history"""
        return chat_data.get_session_messages()

    def clear_conversation(self) -> bool:
        """Clear current conversation"""
        chat_data.clear_session()
        return True

    def save_conversation(self, session_name: str | None) -> Dict:
        """Save current conversation"""
        return chat_data.save_conversation(session_name)

    def get_saved_conversations(self) -> List[Dict]:
        """Get all saved conversations"""
        return chat_data.get_conversations()

# Global controller instance
chat_controller = ChatController()