#!/usr/bin/env python3
"""
Tania AI Assistant - Automated Installation Script
This script helps you install all dependencies and set up Tania easily.
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print the Tania banner"""
    print("=" * 60)
    print("🤖 Tania AI Assistant - Installation Script")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible!")
        return True

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def install_requirements():
    """Install all required packages"""
    print("\n📦 Installing required packages...")
    
    packages = [
        "requests>=2.31.0",
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90",
        "pyautogui>=0.9.54",
        "psutil>=5.9.5",
        "opencv-python>=4.8.1",
        "numpy>=1.24.3"
    ]
    
    # Special handling for PyAudio
    system = platform.system().lower()
    if system == "windows":
        print("🪟 Windows detected - installing PyAudio via pipwin...")
        if not install_package("pipwin"):
            print("❌ Failed to install pipwin")
            return False
        if not install_package("pyaudio"):
            print("❌ Failed to install PyAudio")
            return False
    else:
        packages.append("PyAudio>=0.2.11")
    
    # Install other packages
    for package in packages:
        print(f"   Installing {package}...")
        if not install_package(package):
            print(f"❌ Failed to install {package}")
            return False
    
    print("✅ All packages installed successfully!")
    return True

def check_system_requirements():
    """Check system requirements"""
    print("\n🔧 Checking system requirements...")
    
    # Check if microphone is available
    try:
        import speech_recognition as sr
        mic = sr.Microphone()
        print("✅ Microphone detected!")
    except Exception as e:
        print("⚠️  Warning: Microphone not detected or not working properly")
        print(f"   Error: {e}")
    
    # Check if speakers are available
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if voices:
            print(f"✅ Text-to-speech available ({len(voices)} voices found)")
        else:
            print("⚠️  Warning: No text-to-speech voices found")
    except Exception as e:
        print("⚠️  Warning: Text-to-speech not working properly")
        print(f"   Error: {e}")
    
    # Check system info
    system = platform.system()
    print(f"✅ Operating System: {system} {platform.version()}")
    
    return True

def create_api_key_file():
    """Create API key file if it doesn't exist"""
    if not os.path.exists('.api_key'):
        print("\n🔑 Setting up DeepSeek API key...")
        print("   You'll need a DeepSeek API key to use Tania's AI features.")
        print("   Get your free API key from: https://platform.deepseek.com/")
        
        api_key = input("\n   Enter your DeepSeek API key (or press Enter to skip): ").strip()
        
        if api_key:
            try:
                with open('.api_key', 'w') as f:
                    f.write(api_key)
                print("✅ API key saved successfully!")
                return True
            except Exception as e:
                print(f"❌ Error saving API key: {e}")
                return False
        else:
            print("⚠️  No API key provided. You can add it later by running Tania.")
            return True
    else:
        print("✅ API key file already exists!")
        return True

def run_tests():
    """Run basic tests to ensure everything works"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test imports
        import requests
        import speech_recognition as sr
        import pyttsx3
        import pyautogui
        import psutil
        import cv2
        import numpy as np
        
        print("✅ All modules imported successfully!")
        
        # Test basic functionality
        import platform
        print(f"✅ System info: {platform.system()} {platform.version()}")
        
        # Test speech recognition
        try:
            recognizer = sr.Recognizer()
            print("✅ Speech recognition initialized!")
        except Exception as e:
            print(f"⚠️  Speech recognition test failed: {e}")
        
        # Test text-to-speech
        try:
            engine = pyttsx3.init()
            print("✅ Text-to-speech initialized!")
        except Exception as e:
            print(f"⚠️  Text-to-speech test failed: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main installation function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Installation failed! Please upgrade Python and try again.")
        return False
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Installation failed! Please check the error messages above.")
        return False
    
    # Check system requirements
    check_system_requirements()
    
    # Create API key file
    if not create_api_key_file():
        print("\n❌ API key setup failed!")
        return False
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Some tests failed, but installation may still work.")
    
    print("\n" + "=" * 60)
    print("🎉 Installation completed successfully!")
    print("=" * 60)
    print("\n🚀 To start Tania, run:")
    print("   python tania_ai_assistant.py")
    print("\n📖 For more information, read the README.md file")
    print("\n🤖 Enjoy using Tania, your AI assistant!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)