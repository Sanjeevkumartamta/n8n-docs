#!/usr/bin/env python3
"""
Tania - Female Artificial Intelligence Assistant
A comprehensive AI assistant that can control your PC and communicate in multiple languages.
"""

import os
import sys
import json
import time
import datetime
import subprocess
import platform
import psutil
import requests
import speech_recognition as sr
import pyttsx3
import threading
import webbrowser
import pyautogui
import cv2
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Optional, Any
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tania.log'),
        logging.StreamHandler()
    ]
)

class TaniaAI:
    def __init__(self):
        """Initialize Tania AI Assistant"""
        self.name = "Tania"
        self.version = "1.0.0"
        self.is_active = True
        self.conversation_history = []
        
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        # Set up voice properties
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to find a female voice
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # DeepSeek API configuration
        self.api_key = None
        self.api_base_url = "https://api.deepseek.com/v1"
        
        # Supported languages (excluding major languages as requested)
        self.supported_languages = {
            'french': 'fr',
            'german': 'de',
            'italian': 'it',
            'portuguese': 'pt',
            'dutch': 'nl',
            'swedish': 'sv',
            'norwegian': 'no',
            'danish': 'da',
            'finnish': 'fi',
            'polish': 'pl',
            'czech': 'cs',
            'hungarian': 'hu',
            'romanian': 'ro',
            'bulgarian': 'bg',
            'greek': 'el',
            'turkish': 'tr',
            'arabic': 'ar',
            'hebrew': 'he',
            'persian': 'fa',
            'urdu': 'ur',
            'bengali': 'bn',
            'thai': 'th',
            'vietnamese': 'vi',
            'indonesian': 'id',
            'malay': 'ms',
            'filipino': 'tl',
            'korean': 'ko'
        }
        
        self.current_language = 'en'
        
        # PC Control capabilities
        self.pc_control_enabled = True
        
        # Initialize system information
        self.system_info = self.get_system_info()
        
        logging.info(f"{self.name} AI Assistant initialized successfully")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get current system information"""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'hostname': platform.node(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'disk_usage': psutil.disk_usage('/').percent
        }
    
    def setup_api_key(self):
        """Setup DeepSeek API key"""
        print(f"\n{self.name}: Hello! I need your DeepSeek API key to function properly.")
        print("You can get your API key from: https://platform.deepseek.com/")
        
        api_key = input("Please enter your DeepSeek API key: ").strip()
        
        if api_key:
            self.api_key = api_key
            # Save to file for future use
            with open('.api_key', 'w') as f:
                f.write(api_key)
            print(f"{self.name}: Thank you! API key saved successfully.")
            return True
        else:
            print(f"{self.name}: No API key provided. Some features will be limited.")
            return False
    
    def load_api_key(self):
        """Load API key from file if it exists"""
        try:
            if os.path.exists('.api_key'):
                with open('.api_key', 'r') as f:
                    self.api_key = f.read().strip()
                return True
        except Exception as e:
            logging.error(f"Error loading API key: {e}")
        return False
    
    def speak(self, text: str, language: str = 'en'):
        """Convert text to speech"""
        try:
            # Set language-specific voice if available
            voices = self.engine.getProperty('voices')
            if language != 'en' and voices:
                # Try to find a voice for the specified language
                for voice in voices:
                    if language in voice.id.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"Error in text-to-speech: {e}")
            print(f"{self.name}: {text}")
    
    def listen(self) -> Optional[str]:
        """Listen for voice input"""
        try:
            with self.microphone as source:
                print(f"{self.name}: Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print(f"{self.name}: I couldn't understand what you said.")
            return None
        except sr.RequestError as e:
            print(f"{self.name}: Speech recognition service error: {e}")
            return None
        except Exception as e:
            logging.error(f"Error in speech recognition: {e}")
            return None
    
    def call_deepseek_api(self, message: str, language: str = 'en') -> Optional[str]:
        """Call DeepSeek API for AI response"""
        if not self.api_key:
            return "I'm sorry, but I need an API key to provide intelligent responses. Please set up your DeepSeek API key."
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Create context-aware prompt
            system_prompt = f"""You are {self.name}, a helpful and intelligent AI assistant. You can control computers and communicate in multiple languages. 
            Current system: {self.system_info['os']} {self.system_info['os_version']}
            Current language: {language}
            
            You can:
            - Control the computer (open apps, files, websites)
            - Provide system information
            - Answer questions
            - Help with tasks
            - Communicate in multiple languages
            
            Be helpful, friendly, and concise. If the user asks to control the computer, provide clear instructions on what you can do."""
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': message}
                ],
                'max_tokens': 500,
                'temperature': 0.7
            }
            
            response = requests.post(
                f"{self.api_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logging.error(f"API Error: {response.status_code} - {response.text}")
                return f"I'm sorry, there was an error with the AI service. Error code: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            return "I'm sorry, I'm having trouble connecting to the AI service right now."
        except Exception as e:
            logging.error(f"Error calling DeepSeek API: {e}")
            return "I'm sorry, something went wrong while processing your request."
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the input text"""
        # Simple language detection based on common words
        text_lower = text.lower()
        
        # French
        if any(word in text_lower for word in ['bonjour', 'salut', 'merci', 'oui', 'non', 'je', 'tu', 'il', 'elle']):
            return 'fr'
        # German
        elif any(word in text_lower for word in ['hallo', 'guten', 'danke', 'ja', 'nein', 'ich', 'du', 'er', 'sie']):
            return 'de'
        # Italian
        elif any(word in text_lower for word in ['ciao', 'grazie', 'si', 'no', 'io', 'tu', 'lui', 'lei']):
            return 'it'
        # Portuguese
        elif any(word in text_lower for word in ['olá', 'oi', 'obrigado', 'sim', 'não', 'eu', 'tu', 'ele', 'ela']):
            return 'pt'
        # Spanish (excluded as per request, but keeping for detection)
        elif any(word in text_lower for word in ['hola', 'gracias', 'sí', 'no', 'yo', 'tú', 'él', 'ella']):
            return 'es'
        # Korean
        elif any(char in text for char in ['안녕', '감사', '네', '아니', '저', '나']):
            return 'ko'
        # Arabic
        elif any(char in text for char in ['مرحبا', 'شكرا', 'نعم', 'لا', 'أنا', 'أنت']):
            return 'ar'
        
        return 'en'  # Default to English
    
    def get_system_status(self) -> str:
        """Get current system status"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = f"""
System Status:
- CPU Usage: {cpu_percent}%
- Memory Usage: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
- Disk Usage: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
- Operating System: {self.system_info['os']} {self.system_info['os_version']}
- Python Version: {self.system_info['python_version']}
"""
            return status
        except Exception as e:
            logging.error(f"Error getting system status: {e}")
            return "Unable to get system status at the moment."
    
    def open_application(self, app_name: str) -> str:
        """Open an application"""
        try:
            if self.system_info['os'] == 'Windows':
                subprocess.Popen(app_name, shell=True)
            elif self.system_info['os'] == 'Darwin':  # macOS
                subprocess.Popen(['open', '-a', app_name])
            else:  # Linux
                subprocess.Popen([app_name])
            
            return f"Opening {app_name}..."
        except Exception as e:
            logging.error(f"Error opening application {app_name}: {e}")
            return f"Sorry, I couldn't open {app_name}."
    
    def open_website(self, url: str) -> str:
        """Open a website in the default browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            return f"Opening {url} in your default browser..."
        except Exception as e:
            logging.error(f"Error opening website {url}: {e}")
            return f"Sorry, I couldn't open {url}."
    
    def take_screenshot(self) -> str:
        """Take a screenshot"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            return f"Screenshot saved as {filename}"
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
            return "Sorry, I couldn't take a screenshot."
    
    def get_current_time(self) -> str:
        """Get current time and date"""
        now = datetime.datetime.now()
        return now.strftime("%A, %B %d, %Y at %I:%M %p")
    
    def search_web(self, query: str) -> str:
        """Search the web"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching for '{query}' on Google..."
        except Exception as e:
            logging.error(f"Error searching web: {e}")
            return f"Sorry, I couldn't search for '{query}'."
    
    def process_command(self, command: str) -> str:
        """Process user commands and execute appropriate actions"""
        command_lower = command.lower()
        
        # System status
        if any(word in command_lower for word in ['system status', 'computer status', 'pc status', 'system info']):
            return self.get_system_status()
        
        # Time and date
        elif any(word in command_lower for word in ['time', 'date', 'what time', 'current time']):
            return f"Current time is: {self.get_current_time()}"
        
        # Screenshot
        elif any(word in command_lower for word in ['screenshot', 'take screenshot', 'capture screen']):
            return self.take_screenshot()
        
        # Open applications
        elif 'open' in command_lower:
            apps = {
                'notepad': 'notepad.exe' if self.system_info['os'] == 'Windows' else 'gedit',
                'calculator': 'calc.exe' if self.system_info['os'] == 'Windows' else 'gnome-calculator',
                'paint': 'mspaint.exe' if self.system_info['os'] == 'Windows' else 'gimp',
                'word': 'winword.exe' if self.system_info['os'] == 'Windows' else 'libreoffice --writer',
                'excel': 'excel.exe' if self.system_info['os'] == 'Windows' else 'libreoffice --calc',
                'chrome': 'chrome',
                'firefox': 'firefox',
                'edge': 'msedge.exe' if self.system_info['os'] == 'Windows' else 'microsoft-edge',
                'spotify': 'spotify',
                'discord': 'discord',
                'steam': 'steam'
            }
            
            for app_name, app_command in apps.items():
                if app_name in command_lower:
                    return self.open_application(app_command)
            
            # Generic app opening
            for word in command_lower.split():
                if word not in ['open', 'please', 'can', 'you', 'the', 'a', 'an']:
                    return self.open_application(word)
        
        # Open websites
        elif any(word in command_lower for word in ['website', 'site', 'go to', 'visit']):
            # Extract URL from command
            words = command_lower.split()
            for i, word in enumerate(words):
                if word in ['website', 'site', 'to', 'visit'] and i + 1 < len(words):
                    url = words[i + 1]
                    return self.open_website(url)
        
        # Web search
        elif any(word in command_lower for word in ['search', 'google', 'find']):
            # Extract search query
            search_terms = ['search for', 'search', 'google', 'find']
            for term in search_terms:
                if term in command_lower:
                    query = command_lower.split(term)[-1].strip()
                    return self.search_web(query)
        
        # Language switching
        elif 'language' in command_lower or 'speak' in command_lower:
            for lang_name, lang_code in self.supported_languages.items():
                if lang_name in command_lower:
                    self.current_language = lang_code
                    return f"I'll now communicate in {lang_name}."
        
        # Help
        elif any(word in command_lower for word in ['help', 'what can you do', 'capabilities']):
            return self.get_help_text()
        
        # Exit
        elif any(word in command_lower for word in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
            self.is_active = False
            return "Goodbye! It was nice talking to you."
        
        # If no specific command matched, use AI
        else:
            return self.call_deepseek_api(command, self.current_language)
    
    def get_help_text(self) -> str:
        """Get help text with available commands"""
        return f"""
{self.name} AI Assistant - Available Commands:

PC Control:
- "Open [application]" - Open applications like notepad, calculator, chrome, etc.
- "Take screenshot" - Capture your screen
- "System status" - Get computer performance info
- "Search for [query]" - Search the web
- "Open website [url]" - Open a website

Information:
- "What time is it?" - Get current time and date
- "Help" - Show this help message

Language Support:
- "Speak [language]" - Switch to different languages
- Supported languages: French, German, Italian, Portuguese, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Czech, Hungarian, Romanian, Bulgarian, Greek, Turkish, Arabic, Hebrew, Persian, Urdu, Bengali, Thai, Vietnamese, Indonesian, Malay, Filipino, Korean

General:
- Ask me anything! I can help with questions, tasks, and conversations
- "Exit" or "Goodbye" - Close the assistant

Voice Commands: Just speak naturally and I'll understand!
"""
    
    def run(self):
        """Main run loop for Tania AI Assistant"""
        print(f"\n{'='*60}")
        print(f"🤖 {self.name} AI Assistant v{self.version}")
        print(f"🌍 Multi-language PC Control Assistant")
        print(f"{'='*60}")
        
        # Setup API key
        if not self.load_api_key():
            self.setup_api_key()
        
        print(f"\n{self.name}: Hello! I'm {self.name}, your AI assistant. I can help you control your computer and answer questions in multiple languages.")
        print(f"{self.name}: You can speak to me or type your commands. Say 'help' to see what I can do!")
        
        # Main interaction loop
        while self.is_active:
            try:
                # Get user input (voice or text)
                print(f"\n{self.name}: How can I help you?")
                
                # Try voice input first
                voice_input = self.listen()
                
                if voice_input:
                    user_input = voice_input
                else:
                    # Fall back to text input
                    user_input = input("You: ").strip().lower()
                
                if not user_input:
                    continue
                
                # Detect language
                detected_lang = self.detect_language(user_input)
                if detected_lang != self.current_language:
                    self.current_language = detected_lang
                
                # Process the command
                response = self.process_command(user_input)
                
                # Add to conversation history
                self.conversation_history.append({
                    'user': user_input,
                    'assistant': response,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'language': self.current_language
                })
                
                # Speak and display response
                print(f"{self.name}: {response}")
                self.speak(response, self.current_language)
                
                # Check if user wants to exit
                if not self.is_active:
                    break
                
            except KeyboardInterrupt:
                print(f"\n{self.name}: Goodbye!")
                break
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                print(f"{self.name}: I encountered an error. Please try again.")
        
        print(f"\n{self.name}: Thank you for using me! Have a great day!")

def main():
    """Main function to run Tania AI Assistant"""
    try:
        tania = TaniaAI()
        tania.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"An error occurred: {e}")
        print("Please check the logs for more details.")

if __name__ == "__main__":
    main()