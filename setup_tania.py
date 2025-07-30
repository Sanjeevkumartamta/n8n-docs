#!/usr/bin/env python3
"""
Tania AI Setup Script
This script helps you set up Tania AI Assistant with all necessary configurations.
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🤖 TANIA AI ASSISTANT - SETUP WIZARD")
    print("=" * 60)
    print("This script will help you set up Tania AI Assistant.\n")

def check_python_version():
    """Check Python version compatibility"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"You are running Python {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("Please try installing manually with: pip install -r requirements.txt")
        return False
    
    return True

def setup_api_keys():
    """Help user set up API keys"""
    print("\n🔑 Setting up API Keys...")
    print("Tania AI requires several API keys for full functionality:")
    
    # DeepSeek API Key (Required)
    print("\n1. DeepSeek API Key (REQUIRED for AI conversation)")
    print("   - Go to: https://platform.deepseek.com/")
    print("   - Sign up and get your API key")
    deepseek_key = input("   Enter your DeepSeek API key (or press Enter to skip): ").strip()
    
    if deepseek_key:
        set_env_var("DEEPSEEK_API_KEY", deepseek_key)
        print("   ✅ DeepSeek API key configured!")
    else:
        print("   ⚠️  Skipped - Limited AI functionality available")
    
    # OpenWeather API Key (Optional)
    print("\n2. OpenWeather API Key (Optional - for weather information)")
    print("   - Go to: https://openweathermap.org/api")
    print("   - Sign up for free API key")
    weather_key = input("   Enter your OpenWeather API key (or press Enter to skip): ").strip()
    
    if weather_key:
        set_env_var("OPENWEATHER_API_KEY", weather_key)
        print("   ✅ OpenWeather API key configured!")
    else:
        print("   ⚠️  Skipped - Weather functionality will be limited")
    
    # News API Key (Optional)
    print("\n3. News API Key (Optional - for news headlines)")
    print("   - Go to: https://newsapi.org/")
    print("   - Sign up for free API key")
    news_key = input("   Enter your News API key (or press Enter to skip): ").strip()
    
    if news_key:
        set_env_var("NEWS_API_KEY", news_key)
        print("   ✅ News API key configured!")
    else:
        print("   ⚠️  Skipped - News functionality will be limited")

def set_env_var(key, value):
    """Set environment variable"""
    try:
        if platform.system() == "Windows":
            # For Windows, set user environment variable
            subprocess.run(f'setx {key} "{value}"', shell=True, check=True)
        else:
            # For Linux/Mac, add to .bashrc
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write(f'\nexport {key}="{value}"\n')
            print(f"   Added to ~/.bashrc: export {key}=***")
    except Exception as e:
        print(f"   ⚠️  Could not set environment variable automatically: {e}")
        print(f"   Please set manually: export {key}='{value}'")

def create_config_file():
    """Create a configuration file for API keys"""
    print("\n📄 Creating configuration file...")
    
    config_content = '''# Tania AI Configuration File
# Fill in your API keys here if environment variables don't work

# DeepSeek API Key (Required for AI conversation)
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"

# OpenWeather API Key (Optional - for weather)
OPENWEATHER_API_KEY = "your_openweather_api_key_here"

# News API Key (Optional - for news)
NEWS_API_KEY = "your_news_api_key_here"

# Wolfram Alpha API Key (Optional - for calculations)
WOLFRAM_API_KEY = "your_wolfram_api_key_here"
'''
    
    try:
        with open("config.py", "w") as f:
            f.write(config_content)
        print("✅ Configuration file 'config.py' created!")
        print("   You can edit this file to add your API keys manually.")
    except Exception as e:
        print(f"❌ Error creating config file: {e}")

def check_microphone():
    """Check microphone availability"""
    print("\n🎤 Checking microphone access...")
    
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()
        
        if len(mic_list) > 0:
            print(f"✅ {len(mic_list)} microphone(s) detected:")
            for i, mic in enumerate(mic_list[:3]):  # Show first 3
                print(f"   {i+1}. {mic}")
        else:
            print("⚠️  No microphones detected - Voice mode may not work")
            
    except Exception as e:
        print(f"⚠️  Could not check microphones: {e}")

def create_startup_script():
    """Create a startup script for easy launching"""
    print("\n🚀 Creating startup script...")
    
    if platform.system() == "Windows":
        script_content = '''@echo off
echo Starting Tania AI Assistant...
python tania_ai.py
pause
'''
        script_name = "start_tania.bat"
    else:
        script_content = '''#!/bin/bash
echo "Starting Tania AI Assistant..."
python3 tania_ai.py
'''
        script_name = "start_tania.sh"
    
    try:
        with open(script_name, "w") as f:
            f.write(script_content)
        
        if platform.system() != "Windows":
            os.chmod(script_name, 0o755)  # Make executable
        
        print(f"✅ Startup script '{script_name}' created!")
        print(f"   You can double-click this file to start Tania AI")
        
    except Exception as e:
        print(f"❌ Error creating startup script: {e}")

def test_installation():
    """Test if everything is working"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        print("   Testing imports...")
        import speech_recognition
        import pyttsx3
        import requests
        import pyautogui
        import psutil
        print("   ✅ All required modules imported successfully!")
        
        # Test TTS
        print("   Testing text-to-speech...")
        engine = pyttsx3.init()
        engine.say("Tania AI setup test")
        engine.runAndWait()
        print("   ✅ Text-to-speech working!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def print_final_instructions():
    """Print final setup instructions"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Run Tania AI with: python tania_ai.py")
    print("   Or use the startup script created above")
    
    print("\n🗣️  Voice Commands Examples:")
    print("   - 'Open notepad'")
    print("   - 'What's the weather?'")
    print("   - 'Search for Python tutorials'")
    print("   - 'Take a screenshot'")
    print("   - 'Change language to French'")
    print("   - 'Translate hello to Spanish'")
    
    print("\n💬 Text Commands:")
    print("   You can also type commands instead of speaking them")
    
    print("\n🔧 Troubleshooting:")
    print("   - If voice recognition doesn't work, check microphone permissions")
    print("   - If API calls fail, verify your API keys in config.py")
    print("   - For Linux users, you may need to install additional audio packages")
    
    print("\n📞 Support:")
    print("   Edit the tania_ai.py file to customize Tania's behavior")
    print("   Check the comments in the code for more details")

def main():
    """Main setup function"""
    print_banner()
    
    # Check system requirements
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Set up API keys
    setup_api_keys()
    
    # Create config file
    create_config_file()
    
    # Check microphone
    check_microphone()
    
    # Create startup script
    create_startup_script()
    
    # Test installation
    if test_installation():
        print_final_instructions()
    else:
        print("\n⚠️  Setup completed with some issues. Please check the error messages above.")

if __name__ == "__main__":
    main()