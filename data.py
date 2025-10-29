"""
Data management module for chatbot
Handles all data storage and retrieval operations
"""

import json
import datetime
from typing import List, Dict, Any

class ChatData:
    def __init__(self):
        self.conversations = []
        self.users = {}
        self.current_session = []

    def add_message(self, role: str, content: str, timestamp=None):
        """Add a message to current session"""
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()

        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }

        self.current_session.append(message)
        return message

    def get_session_messages(self) -> List[Dict]:
        """Get all messages from current session"""
        return self.current_session.copy()

    def clear_session(self):
        """Clear current session"""
        self.current_session.clear()

    def save_conversation(self, session_name: str | None):
        """Save current session to conversations"""
        if not session_name:
            session_name = f"Chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        conversation = {
            "name": session_name,
            "messages": self.current_session.copy(),
            "created_at": datetime.datetime.now().isoformat()
        }

        self.conversations.append(conversation)
        return conversation

    def get_conversations(self) -> List[Dict]:
        """Get all saved conversations"""
        return self.conversations

    def export_data(self, filename: str = "chat_data.json"):
        """Export all data to JSON file"""
        data = {
            "conversations": self.conversations,
            "users": self.users,
            "exported_at": datetime.datetime.now().isoformat()
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def import_data(self, filename: str = "chat_data.json"):
        """Import data from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.conversations = data.get('conversations', [])
                self.users = data.get('users', {})
        except FileNotFoundError:
            print("No previous data found. Starting fresh.")

# Global data instance
chat_data = ChatData()