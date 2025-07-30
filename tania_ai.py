#!/usr/bin/env python3
"""
Tania - Female Artificial Intelligence Assistant
A comprehensive AI assistant with PC control, voice interaction, and multilingual support.
Uses DeepSeek API for intelligent responses.
"""

import os
import sys
import subprocess
import threading
import time
import json
import requests
import speech_recognition as sr
import pyttsx3
import psutil
import webbrowser
from datetime import datetime
import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageGrab
import openai
from googletrans import Translator
import wikipedia
import wolframalpha
import socket
import platform
import winsound if sys.platform == "win32" else None

class TaniaAI:
    def __init__(self):
        """Initialize Tania AI Assistant"""
        print("🌟 Initializing Tania AI Assistant...")
        
        # DeepSeek API Configuration
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY', 'your_deepseek_api_key_here')
        self.deepseek_base_url = "https://api.deepseek.com/v1"
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.translator = Translator()
        
        # Configure TTS for female voice
        self.setup_female_voice()
        
        # System info
        self.system_info = self.get_system_info()
        
        # Supported languages
        self.supported_languages = {
            'french': 'fr', 'german': 'de', 'italian': 'it', 'portuguese': 'pt',
            'dutch': 'nl', 'swedish': 'sv', 'norwegian': 'no', 'danish': 'da',
            'finnish': 'fi', 'polish': 'pl', 'czech': 'cs', 'hungarian': 'hu',
            'romanian': 'ro', 'bulgarian': 'bg', 'croatian': 'hr', 'slovak': 'sk',
            'slovenian': 'sl', 'lithuanian': 'lt', 'latvian': 'lv', 'estonian': 'et',
            'turkish': 'tr', 'greek': 'el', 'hebrew': 'he', 'arabic': 'ar',
            'persian': 'fa', 'urdu': 'ur', 'bengali': 'bn', 'tamil': 'ta',
            'telugu': 'te', 'malayalam': 'ml', 'kannada': 'kn', 'gujarati': 'gu',
            'punjabi': 'pa', 'marathi': 'mr', 'thai': 'th', 'vietnamese': 'vi',
            'korean': 'ko', 'indonesian': 'id', 'malay': 'ms', 'tagalog': 'tl',
            'swahili': 'sw', 'yoruba': 'yo', 'zulu': 'zu', 'afrikaans': 'af'
        }
        
        self.current_language = 'en'
        self.listening = True
        
        print("✅ Tania AI Assistant initialized successfully!")
        self.speak("Hello! I am Tania, your AI assistant. I'm ready to help you control your computer and answer your questions in multiple languages.")

    def setup_female_voice(self):
        """Configure TTS engine for female voice"""
        voices = self.tts_engine.getProperty('voices')
        
        # Try to find a female voice
        for voice in voices:
            if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        else:
            # If no explicitly female voice, use the second voice (often female)
            if len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', 180)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level

    def get_system_info(self):
        """Get system information"""
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'ip_address': socket.gethostbyname(socket.gethostname()),
            'processor': platform.processor(),
            'ram': str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        }

    def speak(self, text, language='en'):
        """Convert text to speech"""
        try:
            if language != 'en' and language in self.supported_languages.values():
                # Translate to target language for speech
                translated = self.translator.translate(text, dest=language)
                text = translated.text
            
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

    def listen(self):
        """Listen for voice commands"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition: {e}")
            return None

    def call_deepseek_api(self, prompt, system_message=None):
        """Call DeepSeek API for intelligent responses"""
        try:
            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }
            
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": "deepseek-chat",
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.deepseek_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API Error: {response.status_code}"
                
        except Exception as e:
            return f"Error calling DeepSeek API: {e}"

    def get_weather(self, city="current location"):
        """Get weather information"""
        try:
            # Using a free weather API (OpenWeatherMap)
            api_key = "your_openweather_api_key"  # You'll need to get this
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                return f"The weather in {city} is {weather} with a temperature of {temp}°C"
            else:
                return "Sorry, I couldn't get the weather information right now."
        except:
            return "Weather service is currently unavailable."

    def get_news(self):
        """Get latest news headlines"""
        try:
            # Using NewsAPI (you'll need to get an API key)
            api_key = "your_news_api_key"
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                headlines = [article['title'] for article in data['articles'][:5]]
                return "Here are the top 5 news headlines: " + "; ".join(headlines)
            else:
                return "Sorry, I couldn't get the news right now."
        except:
            return "News service is currently unavailable."

    def search_web(self, query):
        """Search the web"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"I've opened a web search for '{query}' in your browser."
        except Exception as e:
            return f"Error opening web search: {e}"

    def control_system(self, command):
        """Control PC functions"""
        command = command.lower()
        
        try:
            if "open" in command:
                if "notepad" in command:
                    subprocess.Popen(['notepad.exe'])
                    return "Opening Notepad"
                elif "calculator" in command:
                    subprocess.Popen(['calc.exe'])
                    return "Opening Calculator"
                elif "browser" in command or "chrome" in command:
                    webbrowser.open('https://www.google.com')
                    return "Opening web browser"
                elif "file explorer" in command or "explorer" in command:
                    subprocess.Popen(['explorer.exe'])
                    return "Opening File Explorer"
                
            elif "close" in command:
                if "browser" in command:
                    os.system("taskkill /f /im chrome.exe")
                    return "Closing browser"
                elif "notepad" in command:
                    os.system("taskkill /f /im notepad.exe")
                    return "Closing Notepad"
                
            elif "volume" in command:
                if "up" in command:
                    pyautogui.press('volumeup', presses=5)
                    return "Volume increased"
                elif "down" in command:
                    pyautogui.press('volumedown', presses=5)
                    return "Volume decreased"
                elif "mute" in command:
                    pyautogui.press('volumemute')
                    return "Volume muted"
                    
            elif "screenshot" in command:
                screenshot = ImageGrab.grab()
                screenshot.save('screenshot.png')
                return "Screenshot saved as screenshot.png"
                
            elif "shutdown" in command:
                return "Shutting down the computer"
                # os.system("shutdown /s /t 1")  # Uncomment to actually shutdown
                
            elif "restart" in command:
                return "Restarting the computer"
                # os.system("shutdown /r /t 1")  # Uncomment to actually restart
                
            elif "lock" in command:
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return "Locking the computer"
                
            else:
                return "I didn't understand that system command."
                
        except Exception as e:
            return f"Error executing system command: {e}"

    def translate_text(self, text, target_language):
        """Translate text to specified language"""
        try:
            if target_language in self.supported_languages:
                lang_code = self.supported_languages[target_language]
                translated = self.translator.translate(text, dest=lang_code)
                return f"Translation to {target_language}: {translated.text}"
            else:
                return f"Sorry, I don't support {target_language} yet."
        except Exception as e:
            return f"Translation error: {e}"

    def change_language(self, language):
        """Change the assistant's communication language"""
        if language in self.supported_languages:
            self.current_language = self.supported_languages[language]
            return f"Language changed to {language}"
        else:
            return f"Sorry, I don't support {language} yet."

    def get_time(self):
        """Get current time"""
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')} on {now.strftime('%Y-%m-%d')}"

    def process_command(self, command):
        """Process voice/text commands"""
        if not command:
            return
            
        command = command.lower()
        response = ""
        
        # System control commands
        if any(word in command for word in ["open", "close", "volume", "screenshot", "shutdown", "restart", "lock"]):
            response = self.control_system(command)
            
        # Information commands
        elif "weather" in command:
            city = "current location"
            if "in" in command:
                words = command.split("in")
                if len(words) > 1:
                    city = words[1].strip()
            response = self.get_weather(city)
            
        elif "news" in command:
            response = self.get_news()
            
        elif "time" in command:
            response = self.get_time()
            
        elif "search" in command:
            query = command.replace("search", "").replace("for", "").strip()
            response = self.search_web(query)
            
        # Language commands
        elif "translate" in command:
            parts = command.split("to")
            if len(parts) == 2:
                text = parts[0].replace("translate", "").strip()
                language = parts[1].strip()
                response = self.translate_text(text, language)
            else:
                response = "Please say 'translate [text] to [language]'"
                
        elif "change language to" in command:
            language = command.replace("change language to", "").strip()
            response = self.change_language(language)
            
        # System information
        elif "system info" in command or "computer info" in command:
            info = self.system_info
            response = f"System: {info['platform']} {info['platform_release']}, RAM: {info['ram']}, Processor: {info['processor']}"
            
        # Stop command
        elif "stop listening" in command or "goodbye" in command or "exit" in command:
            response = "Goodbye! It was nice helping you."
            self.listening = False
            
        # General AI conversation
        else:
            system_msg = f"""You are Tania, a helpful female AI assistant. You can control the user's computer, 
            provide real-time information, and communicate in multiple languages. The user is running {self.system_info['platform']} 
            on {self.system_info['hostname']}. Be friendly, helpful, and conversational. Keep responses concise but informative."""
            
            response = self.call_deepseek_api(command, system_msg)
        
        print(f"Tania: {response}")
        self.speak(response, self.current_language)
        return response

    def run_voice_mode(self):
        """Run in continuous voice listening mode"""
        print("🎤 Voice mode activated. Say 'stop listening' to exit.")
        self.speak("Voice mode activated. How can I help you?")
        
        while self.listening:
            try:
                command = self.listen()
                if command:
                    self.process_command(command)
                time.sleep(0.5)
            except KeyboardInterrupt:
                break
        
        print("Voice mode deactivated.")

    def run_text_mode(self):
        """Run in text input mode"""
        print("💬 Text mode activated. Type 'exit' to quit.")
        self.speak("Text mode activated. How can I help you?")
        
        while self.listening:
            try:
                command = input("\nYou: ").strip()
                if command.lower() in ['exit', 'quit', 'goodbye']:
                    self.listening = False
                    break
                elif command:
                    self.process_command(command)
            except KeyboardInterrupt:
                break
        
        print("Text mode deactivated.")

def main():
    """Main function to run Tania AI"""
    print("=" * 60)
    print("🤖 TANIA - Female Artificial Intelligence Assistant")
    print("=" * 60)
    
    # Check for DeepSeek API key
    if not os.getenv('DEEPSEEK_API_KEY'):
        print("⚠️  Warning: DEEPSEEK_API_KEY environment variable not set!")
        print("Please set it with: export DEEPSEEK_API_KEY='your_api_key_here'")
        print("You can still use Tania with limited functionality.\n")
    
    try:
        # Initialize Tania
        tania = TaniaAI()
        
        # Choose mode
        print("\nChoose interaction mode:")
        print("1. Voice Mode (speak commands)")
        print("2. Text Mode (type commands)")
        print("3. Mixed Mode (both voice and text)")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            tania.run_voice_mode()
        elif choice == "2":
            tania.run_text_mode()
        elif choice == "3":
            print("Mixed mode: Use voice commands or type in the console")
            # Start voice mode in a separate thread
            voice_thread = threading.Thread(target=tania.run_voice_mode)
            voice_thread.daemon = True
            voice_thread.start()
            
            # Run text mode in main thread
            tania.run_text_mode()
        else:
            print("Invalid choice. Starting text mode...")
            tania.run_text_mode()
    
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your setup and try again.")
    
    finally:
        print("Thank you for using Tania AI Assistant!")

if __name__ == "__main__":
    main()