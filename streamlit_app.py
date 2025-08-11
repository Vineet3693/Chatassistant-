
import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import json
import os
import datetime
import requests
import random
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="JARVIS AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'is_listening' not in st.session_state:
        st.session_state.is_listening = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    if 'commands_count' not in st.session_state:
        st.session_state.commands_count = 0
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = load_user_preferences()

def load_user_preferences():
    """Load user preferences from config file"""
    try:
        if os.path.exists('config/user_preferences.json'):
            with open('config/user_preferences.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return {
        "voice_enabled": True,
        "wake_word": "jarvis",
        "confidence_threshold": 0.7,
        "response_speed": 1.0
    }

def save_user_preferences(preferences):
    """Save user preferences to config file"""
    os.makedirs('config', exist_ok=True)
    with open('config/user_preferences.json', 'w') as f:
        json.dump(preferences, f, indent=4)

# Custom CSS for JARVIS theme
def load_css():
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #00d4ff;
            font-size: 3em;
            margin-bottom: 30px;
            text-shadow: 0 0 10px #00d4ff;
            font-family: 'Arial Black', sans-serif;
        }
        .status-indicator {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
        }
        .status-active { 
            background-color: #00ff00; 
            box-shadow: 0 0 10px #00ff00;
        }
        .status-inactive { 
            background-color: #ff0000; 
            box-shadow: 0 0 10px #ff0000;
        }
        .chat-message-user {
            padding: 10px;
            margin: 5px 0;
            border-radius: 10px;
            background-color: #2d3748;
            border-left: 4px solid #4299e1;
        }
        .chat-message-ai {
            padding: 10px;
            margin: 5px 0;
            border-radius: 10px;
            background-color: #1a202c;
            border-left: 4px solid #00d4ff;
        }
        .quick-command-btn {
            margin: 5px 0;
            width: 100%;
        }
        .metric-card {
            background-color: #2d3748;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

class JarvisAI:
    def __init__(self):
        self.context_memory = []
        self.commands_db = self.load_commands_database()
    
    def load_commands_database(self):
        """Load command patterns and responses"""
        return {
            "greetings": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
            "time_queries": ["time", "what time", "current time"],
            "date_queries": ["date", "what date", "today", "current date"],
            "weather_queries": ["weather", "temperature", "forecast"],
            "system_commands": ["open", "close", "launch", "start", "shutdown", "restart"],
            "calculations": ["calculate", "compute", "math", "+", "-", "*", "/"],
            "jokes": ["joke", "funny", "humor", "laugh"],
            "goodbye": ["bye", "goodbye", "see you", "exit", "quit"]
        }
    
    def process_command(self, command):
        """Main command processing function"""
        command_lower = command.lower().strip()
        
        # Update context memory
        self.context_memory.append(command_lower)
        if len(self.context_memory) > 10:
            self.context_memory.pop(0)
        
        # Classify and handle command
        intent = self.classify_intent(command_lower)
        
        if intent == "greeting":
            return self.handle_greeting()
        elif intent == "time":
            return self.handle_time_query()
        elif intent == "date":
            return self.handle_date_query()
        elif intent == "weather":
            return self.handle_weather_query(command_lower)
        elif intent == "system":
            return self.handle_system_command(command_lower)
        elif intent == "calculation":
            return self.handle_calculation(command_lower)
        elif intent == "joke":
            return self.handle_joke_request()
        elif intent == "goodbye":
            return self.handle_goodbye()
        else:
            return self.handle_unknown_command(command)
    
    def classify_intent(self, command):
        """Classify user intent based on command"""
        for intent, keywords in self.commands_db.items():
            if any(keyword in command for keyword in keywords):
                return intent.replace("_queries", "").replace("_commands", "").replace("s", "")
        return "unknown"
    
    def handle_greeting(self):
        greetings = [
            "Hello! I'm JARVIS, your AI assistant. How can I help you today?",
            "Greetings! JARVIS at your service. What can I do for you?",
            "Hi there! Ready to assist you with anything you need.",
            "Good day! JARVIS here, ready for your commands."
        ]
        return random.choice(greetings)
    
    def handle_time_query(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    def handle_date_query(self):
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        day_of_week = datetime.datetime.now().strftime("%A")
        return f"Today is {day_of_week}, {current_date}"
    
    def handle_weather_query(self, command):
        # For demo purposes - you'd integrate with a real weather API
        cities = ["New York", "London", "Tokyo", "Paris", "Sydney"]
        weather_conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "clear"]
        temperature = random.randint(15, 30)
        condition = random.choice(weather_conditions)
        
        return f"I'd need access to a weather API for real data, but here's a demo: It's {temperature}°C and {condition} outside. For real weather data, please integrate with OpenWeatherMap API."
    
    def handle_system_command(self, command):
        if "open" in command:
            if "calculator" in command:
                return "Calculator would be opened (system integration needed for actual execution)"
            elif "notepad" in command:
                return "Notepad would be opened (system integration needed for actual execution)"
            elif "browser" in command or "chrome" in command:
                return "Browser would be opened (system integration needed for actual execution)"
            else:
                return "System command recognized but specific application not identified"
        elif "shutdown" in command:
            return "Shutdown command received (would require elevated permissions in actual implementation)"
        else:
            return "System command recognized but not implemented in this demo version"
    
    def handle_calculation(self, command):
        try:
            # Simple calculation parser
            import re
            # Extract numbers and operators
            expression = re.findall(r'[\d+\-*/().]+', command)
            if expression:
                calc_string = ''.join(expression)
                # Basic safety check
                if all(c in '0123456789+-*/(). ' for c in calc_string):
                    result = eval(calc_string)
                    return f"The result is: {result}"
            return "I can help with calculations, but I need a clearer mathematical expression. Try something like '2 + 2' or 'calculate 10 * 5'"
        except:
            return "I couldn't process that calculation. Please try a simpler format like '2 + 2'"
    
    def handle_joke_request(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the AI go to therapy? It had too many deep learning issues!",
            "What do you call a computer that sings? A-Dell!",
            "Why don't robots ever panic? They have great artificial composure!",
            "What's an AI's favorite type of music? Algo-rhythms!"
        ]
        return random.choice(jokes)
    
    def handle_goodbye(self):
        farewells = [
            "Goodbye! Feel free to call on me anytime you need assistance.",
            "See you later! I'll be here whenever you need help.",
            "Until next time! Stay safe and productive.",
            "Farewell! It was a pleasure assisting you today."
        ]
        return random.choice(farewells)
    
    def handle_unknown_command(self, command):
        responses = [
            f"I'm not sure I understand '{command}'. Could you rephrase that?",
            "That's an interesting request! I'm still learning. Can you try asking differently?",
            "I don't have that capability yet, but I'm always improving. What else can I help with?",
            "Could you clarify what you'd like me to do? I'm here to help!"
        ]
        return random.choice(responses)

# Initialize JARVIS
@st.cache_resource
def get_jarvis():
    return JarvisAI()

def main():
    initialize_session_state()
    load_css()
    jarvis = get_jarvis()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 JARVIS AI Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Control Panel")
        
        # Status
        status_color = "🟢" if st.session_state.is_listening else "🔴"
        status_text = "Active" if st.session_state.is_listening else "Standby"
        st.markdown(f"**Status:** {status_color} {status_text}")
        
        # Voice Controls
        st.subheader("🎤 Voice Interface")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎙️ Activate", use_container_width=True):
                st.session_state.is_listening = True
                st.success("Voice recognition activated!")
                st.rerun()
        
        with col2:
            if st.button("⏹️ Deactivate", use_container_width=True):
                st.session_state.is_listening = False
                st.info("Voice recognition deactivated")
                st.rerun()
        
        # Settings
        st.subheader("⚙️ Settings")
        
        voice_enabled = st.checkbox(
            "Voice Responses", 
            value=st.session_state.user_preferences.get("voice_enabled", True)
        )
        
        wake_word = st.selectbox(
            "Wake Word", 
            ["jarvis", "computer", "assistant"],
            index=["jarvis", "computer", "assistant"].index(
                st.session_state.user_preferences.get("wake_word", "jarvis")
            )
        )
        
        confidence_threshold = st.slider(
            "Recognition Confidence", 
            0.1, 1.0, 
            st.session_state.user_preferences.get("confidence_threshold", 0.7)
        )
        
        response_speed = st.slider(
            "Response Speed", 
            0.5, 2.0, 
            st.session_state.user_preferences.get("response_speed", 1.0)
        )
        
        # Save settings
        if st.button("💾 Save Settings"):
            new_preferences = {
                "voice_enabled": voice_enabled,
                "wake_word": wake_word,
                "confidence_threshold": confidence_threshold,
                "response_speed": response_speed
            }
            st.session_state.user_preferences = new_preferences
            save_user_preferences(new_preferences)
            st.success("Settings saved!")
        
        # System Stats
        st.subheader("📊 Session Stats")
        session_time = int(time.time() - st.session_state.start_time)
        st.metric("Session Duration", f"{session_time//60}m {session_time%60}s")
        st.metric("Commands Processed", st.session_state.commands_count)
        st.metric("Conversations", len(st.session_state.conversation_history)//2)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Chat history container
        chat_container = st.container()
        
        with chat_container:
            if st.session_state.conversation_history:
                for i, message in enumerate(st.session_state.conversation_history[-20:]):  # Show last 20 messages
                    if message['type'] == 'user':
                        st.markdown(f"""
                        <div class="chat-message-user">
                            <strong>👤 You:</strong> {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="chat-message-ai">
                            <strong>🤖 JARVIS:</strong> {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("👋 Hello! I'm JARVIS. Type a message or use voice commands to get started!")
        
        # Input section
        st.subheader("📝 Command Input")
        
        # Text input
        user_input = st.text_input(
            "Enter your command:", 
            placeholder="Ask me anything...",
            key="text_input"
        )
        
        col_send, col_clear = st.columns([1, 1])
        
        with col_send:
            if st.button("📤 Send Command", use_container_width=True) and user_input:
                process_user_command(jarvis, user_input)
        
        with col_clear:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.conversation_history = []
                st.session_state.commands_count = 0
                st.rerun()
    
    with col2:
        st.subheader("⚡ Quick Commands")
        
        # Quick command categories
        command_categories = {
            "🕐 Time & Date": [
                "What time is it?",
                "What's today's date?",
                "Current time please"
            ],
            "🌤️ Information": [
                "Tell me the weather",
                "System status",
                "Tell me a joke"
            ],
            "🖥️ System": [
                "Open calculator",
                "Open notepad",
                "Open browser"
            ],
            "🧮 Math": [
                "Calculate 15 + 25",
                "What's 100 / 4?",
                "Compute 7 * 8"
            ]
        }
        
        for category, commands in command_categories.items():
            with st.expander(category):
                for cmd in commands:
                    if st.button(cmd, key=f"quick_{cmd}", use_container_width=True):
                        process_user_command(jarvis, cmd)
        
        # Voice status
        st.subheader("🔊 Audio Status")
        if st.session_state.is_listening:
            st.success("🎤 Ready for voice input")
            st.info("💡 Say 'Hey JARVIS' followed by your command")
        else:
            st.warning("🔇 Voice input inactive")
        
        # Help section
        with st.expander("❓ Help & Commands"):
            st.markdown("""
            **Available Commands:**
            - Greetings: Hello, Hi, Hey
            - Time: What time is it?
            - Date: What's the date today?
            - Weather: What's the weather?
            - Math: Calculate 2+2
            - Jokes: Tell me a joke
            - System: Open calculator
            - Goodbye: Bye, Exit
            """)

def process_user_command(jarvis, command):
    """Process user command and update conversation history"""
    if command.strip():
        # Add user message
        st.session_state.conversation_history.append({
            'type': 'user',
            'content': command,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        # Process with JARVIS
        response = jarvis.process_command(command)
        
        # Add AI response
        st.session_state.conversation_history.append({
            'type': 'ai',
            'content': response,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        # Update counters
        st.session_state.commands_count += 1
        
        # Auto-scroll and refresh
        st.rerun()

# Voice recognition placeholder (for future implementation)
def start_voice_recognition():
    """Start voice recognition (placeholder for actual implementation)"""
    st.session_state.is_listening = True

def stop_voice_recognition():
    """Stop voice recognition (placeholder for actual implementation)"""
    st.session_state.is_listening = False

# Run the app
if __name__ == "__main__":
    main()
