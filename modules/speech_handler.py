
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import streamlit as st

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = self.initialize_tts()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
    def initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            engine = pyttsx3.init()
            # Set properties
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate - 50)  # Slower speech
            
            volume = engine.getProperty('volume')
            engine.setProperty('volume', volume + 0.1)  # Louder
            
            return engine
        except:
            st.error("Text-to-speech engine not available")
            return None
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            return True
        except:
            return False
    
    def listen_for_speech(self, timeout=5):
        """Listen for speech input"""
        try:
            with self.microphone as source:
                st.info("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
                
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "Timeout - no speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"
    
    def speak_text(self, text):
        """Convert text to speech"""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                st.error("Could not synthesize speech")
        else:
            st.info(f"JARVIS would say: {text}")
    
    def start_continuous_listening(self):
        """Start continuous speech recognition in background"""
        self.is_listening = True
        threading.Thread(target=self._continuous_listen, daemon=True).start()
    
    def stop_continuous_listening(self):
        """Stop continuous speech recognition"""
        self.is_listening = False
    
    def _continuous_listen(self):
        """Continuous listening loop"""
        while self.is_listening:
            try:
                speech_text = self.listen_for_speech(timeout=1)
                if speech_text and not speech_text.startswith("Timeout") and not speech_text.startswith("Could not"):
                    self.audio_queue.put(speech_text)
                time.sleep(0.1)
            except:
                continue
    
    def get_speech_from_queue(self):
        """Get recognized speech from queue"""
        try:
            return self.audio_queue.get_nowait()
        except queue.Empty:
            return None
