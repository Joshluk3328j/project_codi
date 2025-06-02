
---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/codi.git
cd codi
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
HF_TOKEN=your_huggingface_api_token
```

### 5. Run the App
```bash
streamlit run app.py
```

## 📁 Project Structure

```
codi/
├── .env                     # Environment variables (if used)
├── codi.env                 # Custom environment config file
├── main.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── modules/                 # Modular logic
│   ├── __init__.py
│   ├── audio_bar.py         # Custom audio player for Streamlit
│   ├── explainer.py         # Code explanation logic using HuggingFace API
│   ├── history_manager.py   # Manages upload, explanation, and chat history
│   ├── settings_manager.py  # Load/save user settings (voice, style, etc.)
│   ├── voice_assistant.py   # Text-to-speech logic for voice responses
│   └── data/                # Static and generated resources
│       ├── fonts/
│       │   └── DejaVuSans.ttf   # Font for multilingual PDF generation
│       ├── audio/
│       │   └── *.mp3            # Generated voice responses
│       └── *.pdf                # Generated explanation/chat PDFs
```
