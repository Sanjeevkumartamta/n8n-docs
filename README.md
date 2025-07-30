# 🤖 Tania - Female Artificial Intelligence Assistant

Tania is a comprehensive AI assistant powered by the DeepSeek API that can control your PC, provide real-time information, and communicate in multiple languages through both voice and text.

## ✨ Features

### 🎯 Core Capabilities
- **AI Conversation**: Powered by DeepSeek API for intelligent responses
- **PC Control**: Open/close applications, control volume, take screenshots
- **Voice Interaction**: Speech recognition and text-to-speech with female voice
- **Multilingual Support**: Communicate in 30+ languages (excluding major ones like English, Chinese, Hindi, Russian, Japanese, Spanish)
- **Real-time Information**: Weather, news, web search, system information
- **Translation**: Translate text between supported languages

### 🖥️ System Control
- Open applications (Notepad, Calculator, Browser, File Explorer)
- Close running applications
- Volume control (up, down, mute)
- Take screenshots
- System information
- Lock screen (shutdown/restart commands included but commented for safety)

### 🌍 Supported Languages
French, German, Italian, Portuguese, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Czech, Hungarian, Romanian, Bulgarian, Croatian, Slovak, Slovenian, Lithuanian, Latvian, Estonian, Turkish, Greek, Hebrew, Arabic, Persian, Urdu, Bengali, Tamil, Telugu, Malayalam, Kannada, Gujarati, Punjabi, Marathi, Thai, Vietnamese, Korean, Indonesian, Malay, Tagalog, Swahili, Yoruba, Zulu, Afrikaans

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Microphone (for voice mode)
- Internet connection

### Installation

1. **Download the files** and place them in a folder
2. **Run the setup script**:
   ```bash
   python setup_tania.py
   ```
3. **Follow the setup wizard** to:
   - Install dependencies
   - Configure API keys
   - Test your setup

### Alternative Manual Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get your DeepSeek API key**:
   - Go to [https://platform.deepseek.com/](https://platform.deepseek.com/)
   - Sign up and get your API key
   - Set environment variable:
     ```bash
     export DEEPSEEK_API_KEY="your_api_key_here"
     ```

3. **Run Tania**:
   ```bash
   python tania_ai.py
   ```

## 🎮 Usage

### Running Tania
```bash
python tania_ai.py
```

Choose from three modes:
1. **Voice Mode**: Speak your commands
2. **Text Mode**: Type your commands
3. **Mixed Mode**: Both voice and text

### Voice Commands Examples

#### System Control
- "Open notepad"
- "Open calculator" 
- "Open browser"
- "Close browser"
- "Volume up"
- "Volume down"
- "Take a screenshot"
- "Lock the computer"

#### Information
- "What's the weather?"
- "What's the weather in Paris?"
- "What's the news?"
- "What time is it?"
- "System info"

#### Web & Search
- "Search for Python tutorials"
- "Search for best restaurants"

#### Language & Translation
- "Change language to French"
- "Translate hello to German"
- "Translate good morning to Italian"

#### AI Conversation
- "Tell me a joke"
- "What is artificial intelligence?"
- "Help me write an email"
- "Explain quantum computing"

### Text Commands
You can type any of the above commands instead of speaking them.

## ⚙️ Configuration

### API Keys Setup

Edit `config.py` or set environment variables:

```python
# Required for AI conversation
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"

# Optional for weather
OPENWEATHER_API_KEY = "your_openweather_api_key_here"

# Optional for news
NEWS_API_KEY = "your_news_api_key_here"
```

### Getting API Keys

1. **DeepSeek API** (Required):
   - Visit: https://platform.deepseek.com/
   - Create account and get API key
   - Used for AI conversation and responses

2. **OpenWeather API** (Optional):
   - Visit: https://openweathermap.org/api
   - Free tier available
   - Used for weather information

3. **News API** (Optional):
   - Visit: https://newsapi.org/
   - Free tier available
   - Used for news headlines

## 🔧 Customization

### Changing Voice Settings
Edit the `setup_female_voice()` method in `tania_ai.py`:
```python
self.tts_engine.setProperty('rate', 180)    # Speech speed
self.tts_engine.setProperty('volume', 0.9)  # Volume level
```

### Adding New Commands
Add new command patterns in the `process_command()` method:
```python
elif "your_command" in command:
    response = your_custom_function(command)
```

### Adding New Languages
Add language codes to `supported_languages` dictionary:
```python
'your_language': 'language_code'
```

## 🛠️ Troubleshooting

### Common Issues

**Voice Recognition Not Working**:
- Check microphone permissions
- Ensure microphone is connected and working
- Try running as administrator (Windows)

**API Calls Failing**:
- Verify API keys are correct
- Check internet connection
- Ensure API quotas aren't exceeded

**Import Errors**:
- Run: `pip install -r requirements.txt`
- Ensure Python 3.7+ is installed

**Linux Audio Issues**:
```bash
# Install audio packages
sudo apt-get install portaudio19-dev python3-pyaudio
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
```

**Windows Audio Issues**:
- Install Visual Studio Build Tools
- Ensure Windows Audio Service is running

### Performance Tips
- Use text mode for faster response times
- Close unnecessary applications for better voice recognition
- Ensure stable internet connection for API calls

## 📁 File Structure

```
tania-ai/
├── tania_ai.py          # Main AI assistant script
├── setup_tania.py       # Setup wizard
├── requirements.txt     # Python dependencies
├── config.py           # Configuration file (created by setup)
├── README.md           # This file
├── start_tania.bat     # Windows startup script
└── start_tania.sh      # Linux/Mac startup script
```

## 🔒 Privacy & Security

- All voice processing is done locally
- API calls are only made to specified services
- No data is stored permanently
- API keys are stored locally only

## 🤝 Contributing

Feel free to customize and extend Tania for your needs:
- Add new voice commands
- Integrate additional APIs
- Improve language support
- Enhance PC control features

## 📄 License

This project is for educational and personal use. Please respect the terms of service of all integrated APIs.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure API keys are configured correctly
4. Check system permissions for microphone access

---

**Enjoy your AI assistant Tania! 🎉**

