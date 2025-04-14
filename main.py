#!/usr/bin/env python3
"""
JarvisBox: AI-Powered Voice Assistant Terminal
Main application entry point
"""

import os
import sys
import time
import signal
import threading
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Set up base directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# Import core modules
from core.wake_word import WakeWordDetector
from core.speech_to_text import SpeechToTextEngine
from core.text_to_speech import TextToSpeechEngine
from core.llm_interface import LLMInterface
from hardware.led_controller import LEDController
from hardware.servo_controller import ServoController
from hardware.display_controller import DisplayController
from utils.logging_utils import setup_logger

# Load configuration
def load_config():
    config_path = BASE_DIR / "config" / "settings.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

class JarvisBox:
    """Main JarvisBox application class"""
    
    def __init__(self):
        self.config = load_config()
        self.logger = setup_logger(self.config["system"]["log_level"])
        self.logger.info("Initializing JarvisBox...")
        
        # Initialize components
        self.initialize_components()
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        self.running = True
        self.logger.info("JarvisBox initialized and ready!")
    
    def initialize_components(self):
        """Initialize all JarvisBox components"""
        try:
            # Hardware controllers
            self.logger.info("Initializing hardware components...")
            self.led = LEDController(self.config["hardware"]["led_pin"])
            self.servo = ServoController(self.config["hardware"]["servo_pin"])
            self.display = DisplayController(
                self.config["hardware"]["display"]["width"],
                self.config["hardware"]["display"]["height"],
                self.config["hardware"]["display"]["i2c_address"]
            )
            
            # AI components
            self.logger.info("Initializing AI components...")
            self.wake_word = WakeWordDetector(self.config["system"]["wake_word"])
            self.stt = SpeechToTextEngine(self.config["speech"]["stt_engine"])
            self.tts = TextToSpeechEngine(self.config["speech"]["tts_engine"])
            self.llm = LLMInterface(
                provider=self.config["llm"]["provider"],
                model=self.config["llm"]["model"],
                system_prompt=self.config["llm"]["system_prompt"]
            )
            
            # Visual feedback for initialization
            self.led.startup_sequence()
            self.display.show_text("JarvisBox Ready")
            
        except Exception as e:
            self.logger.error(f"Initialization error: {e}")
            sys.exit(1)
    
    def run(self):
        """Main application loop"""
        self.logger.info("Starting main loop...")
        
        try:
            while self.running:
                # 1. Wait for wake word
                self.logger.debug("Listening for wake word...")
                self.led.set_state("listening")
                self.display.show_text("Listening for wake word...")
                
                if self.wake_word.detect():
                    # Wake word detected
                    self.led.set_state("active")
                    self.servo.turn_to_speaker()
                    self.display.show_text("How can I help?")
                    
                    # 2. Capture user query
                    self.logger.debug("Wake word detected, capturing speech...")
                    audio_data = self.stt.listen()
                    user_query = self.stt.transcribe(audio_data)
                    
                    if user_query:
                        self.logger.info(f"User query: {user_query}")
                        self.display.show_text("Processing...")
                        
                        # 3. Process with LLM
                        self.led.set_state("thinking")
                        response = self.llm.generate_response(user_query)
                        
                        # 4. Respond to user
                        self.logger.info(f"AI response: {response}")
                        self.led.set_state("speaking")
                        self.display.show_text(response[:20] + "..." if len(response) > 20 else response)
                        
                        audio_response = self.tts.generate_speech(response)
                        self.tts.play_audio(audio_response)
                        
                        # Return to listening state
                        self.led.set_state("idle")
                        self.display.show_text("Ready")
                
                time.sleep(0.1)  # Small delay to prevent CPU hogging
                
        except Exception as e:
            self.logger.error(f"Runtime error: {e}")
            self.cleanup()
    
    def cleanup(self, *args):
        """Clean up resources before exiting"""
        self.logger.info("Cleaning up resources...")
        self.running = False
        
        # Clean up hardware
        self.led.cleanup()
        self.servo.cleanup()
        self.display.cleanup()
        
        self.logger.info("JarvisBox shutdown complete")
        sys.exit(0)

if __name__ == "__main__":
    jarvis = JarvisBox()
    jarvis.run()