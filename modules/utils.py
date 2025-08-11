
import json
import os
import datetime
import logging
from pathlib import Path

def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f"jarvis_{datetime.date.today()}.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("JARVIS")

def load_config(config_path="config/config.json"):
    """Load configuration from JSON file"""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Return default config if file doesn't exist
            return get_default_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        return get_default_config()

def save_config(config, config_path="config/config.json"):
    """Save configuration to JSON file"""
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def get_default_config():
    """Return default configuration"""
    return {
        "app_name": "JARVIS AI Assistant",
        "version": "1.0.0",
        "debug": False,
        "voice": {
            "enabled": True,
            "wake_word": "jarvis",
            "confidence_threshold": 0.7,
            "language": "en-US"
        },
        "ui": {
            "theme": "dark",
            "max_history": 100,
            "auto_scroll": True
        },
        "system": {
            "auto_start": False,
            "minimize_to_tray": True,
            "check_updates": True
        }
    }

def format_timestamp(timestamp=None):
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.datetime.now()
    elif isinstance(timestamp, str):
        timestamp = datetime.datetime.fromisoformat(timestamp)
    
    return timestamp.strftime("%H:%M:%S")

def sanitize_input(text):
    """Sanitize user input for security"""
    if not isinstance(text, str):
        return ""
    
    # Remove potentially harmful characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    # Limit length
    return text[:500].strip()

def validate_command(command):
    """Validate if command is safe to execute"""
    dangerous_keywords = [
        'rm -rf', 'del *', 'format', 'fdisk', 'mkfs',
        'shutdown -r now', 'reboot', 'halt', 'poweroff'
    ]
    
    command_lower = command.lower()
    return not any(keyword in command_lower for keyword in dangerous_keywords)

def get_file_size(file_path):
    """Get file size in human readable format"""
    try:
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    except:
        return "Unknown"

def create_directory_structure():
    """Create necessary directory structure"""
    directories = [
        "config",
        "logs",
        "data",
        "assets/audio",
        "assets/images",
        "modules"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

class ConversationManager:
    """Manage conversation history and context"""
    
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.history_file = "data/conversation_history.json"
        self.load_history()
    
    def load_history(self):
        """Load conversation history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.conversations = json.load(f)
            else:
                self.conversations = []
        except:
            self.conversations = []
    
    def save_history(self):
        """Save conversation history to file"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(self.conversations[-self.max_history:], f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_conversation(self, user_input, ai_response):
        """Add new conversation to history"""
        conversation = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response
        }
        self.conversations.append(conversation)
        
        # Keep only recent conversations
        if len(self.conversations) > self.max_history:
            self.conversations = self.conversations[-self.max_history:]
        
        self.save_history()
    
    def get_recent_context(self, num_messages=5):
        """Get recent conversation context"""
        return self.conversations[-num_messages:] if self.conversations else []
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversations = []
        self.save_history()
