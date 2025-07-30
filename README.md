# 🤖 Tania AI Assistant

A comprehensive female AI assistant that can control your PC and communicate in multiple languages using the DeepSeek API.

## 🌟 Features

- **Voice Recognition**: Speak to Tania naturally
- **Text-to-Speech**: Tania responds with a female voice
- **PC Control**: Open applications, take screenshots, get system info
- **Multi-language Support**: Communicates in 25+ languages (excluding major languages as requested)
- **Web Integration**: Search the web, open websites
- **Real-time Information**: Get current time, system status, and more
- **AI-powered Responses**: Uses DeepSeek API for intelligent conversations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Microphone and speakers
- DeepSeek API key (get it from [https://platform.deepseek.com/](https://platform.deepseek.com/))

### Installation

1. **Clone or download the files**
   ```bash
   # If you have git installed
   git clone <repository-url>
   # Or simply download the files to your computer
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Tania**
   ```bash
   python tania_ai_assistant.py
   ```

4. **Enter your DeepSeek API key when prompted**
   - Get your API key from: https://platform.deepseek.com/
   - The key will be saved for future use

## 🎯 Usage Examples

### Voice Commands
- "Open notepad"
- "Take a screenshot"
- "What's the system status?"
- "Search for Python tutorials"
- "Open website github.com"
- "What time is it?"

### Language Support
- "Speak French" - Switch to French
- "Speak German" - Switch to German
- "Speak Korean" - Switch to Korean
- And many more languages!

### General Questions
- Ask Tania anything - she'll use AI to provide intelligent responses
- "Help" - See all available commands
- "Exit" or "Goodbye" - Close the assistant

## 🌍 Supported Languages

Tania supports communication in these languages (excluding major languages as requested):
- French, German, Italian, Portuguese
- Dutch, Swedish, Norwegian, Danish, Finnish
- Polish, Czech, Hungarian, Romanian, Bulgarian
- Greek, Turkish, Arabic, Hebrew, Persian
- Urdu, Bengali, Thai, Vietnamese
- Indonesian, Malay, Filipino, Korean

## 🔧 System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **Hardware**: Microphone and speakers/headphones
- **Internet**: Required for AI responses and web features

## 📁 File Structure

```
tania_ai_assistant/
├── tania_ai_assistant.py    # Main application
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── .api_key               # Your API key (created automatically)
└── tania.log              # Log file (created automatically)
```

## 🛠️ Troubleshooting

### Common Issues

1. **"No module named 'speech_recognition'"**
   ```bash
   pip install SpeechRecognition
   ```

2. **"No module named 'pyttsx3'"**
   ```bash
   pip install pyttsx3
   ```

3. **Microphone not working**
   - Check your microphone permissions
   - Ensure microphone is not muted
   - Try running as administrator (Windows)

4. **API key issues**
   - Make sure you have a valid DeepSeek API key
   - Check your internet connection
   - Verify the API key is correctly entered

### Linux-specific Setup

On Linux, you might need to install additional packages:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyaudio portaudio19-dev

# Fedora
sudo dnf install python3-pyaudio portaudio-devel

# Arch Linux
sudo pacman -S python-pyaudio portaudio
```

### Windows-specific Setup

On Windows, if you encounter PyAudio issues:
```bash
pip install pipwin
pipwin install pyaudio
```

## 🔒 Security Notes

- Your API key is stored locally in `.api_key` file
- Keep this file secure and don't share it
- The assistant only makes requests to DeepSeek API and Google Speech Recognition

## 📝 Logging

Tania creates a log file (`tania.log`) that contains:
- Application startup/shutdown events
- API request logs
- Error messages
- System information

## 🤝 Contributing

Feel free to improve Tania by:
- Adding new language support
- Implementing additional PC control features
- Improving voice recognition accuracy
- Adding new AI capabilities

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Look at the `tania.log` file for error details
3. Ensure all dependencies are properly installed
4. Verify your API key is valid

---

**Enjoy using Tania, your personal AI assistant!** 🤖✨

