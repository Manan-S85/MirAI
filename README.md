<h1 align="center">🤖 MirAi – Desktop AI Assistant</h1>

<p align="center">
  A sleek AI-powered assistant with OpenRouter support, real-time weather, date/time, and web search – all wrapped in a beautiful GUI. Just press <code>Ctrl+K</code> to summon it!
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" />
  <img src="https://img.shields.io/badge/UI-PySide6-purple" />
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

---

## ✨ Features

- 🧠 Chat with models via **OpenRouter** (Mistral, GPT, Claude & more)
- 🔍 Optional **Live Search** via Serper.dev
- 🌤 **Weather updates** (free via `wttr.in`)
- 🕒 **Live date & time**
- 🎯 Summon from anywhere using `Ctrl + K` hotkey
- 💻 Clean, dark-themed GUI with temperature control
- 📦 Easy `.exe` build — no VSCode required!

---

## 📸 Preview
<img width="874" height="655" alt="image" src="https://github.com/user-attachments/assets/0be56bc3-dd11-466a-85bc-976f57466817" />

<h2>🚀 Getting Started</h2>
<h3>1. Clone the Repository</h3>

```bash
git clone https://github.com/Manan-S85/MirAi.git
cd MirAi

```
<h2>2. Install Python</h2>
Make sure Python 3.9 or higher is installed.
You can download it from: https://www.python.org/downloads/

<h2>3. Create a Virtual Environment(Recommended)</h2>

```bash
python -m venv venv
```
Activate it:
On Windows
```bash
venv\Scripts\activate
```
<h2>4. Install Dependencies</h2>

```bash
pip install -r requirements.txt
```

<h2>5. Add Your API Keys</h2>
Open the MirAi.py file and find the following lines:

```bash
OPENROUTER_API_KEY = ""
SERPER_API_KEY     = ""
```

Replace the empty quotes with your keys

Get your keys from:

🔑 OpenRouter API key

🔍 Serper API key (Only if you need latest knowledge)

<h2>6. Run the Assistant</h2>

```bash
python MirAi.py
```
The assistant will minimize to your system tray.
Press Ctrl + K anytime to open it!

<h2>💬 Using the Assistant</h2>

~Ask your question in the input field

~Toggle “Enable Live Search” (optional)

~Adjust creativity with the slider

~Click Ask MirAi to get a response

~Weather and time are displayed at the top

<h2>🧪 Build a Standalone Windows .exe</h2>

Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

Step 2: Generate the .exe
```bash
pyinstaller --onefile --windowed --icon=logo.pico --add-data "logo.png;." MirAi.py
```
You’ll find the .exe file in the dist/ folder.

Now you can share or run it on any Windows machine — no Python or VSCode needed.

<h2>⚙️ Configuration Options</h2>
You can customize these inside MirAi.py:
<table>
  <thead>
    <tr>
      <th>Setting</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>DEFAULT_MODEL</code></td>
      <td>OpenRouter model to use (e.g., Mistral, GPT, Claude)</td>
    </tr>
    <tr>
      <td><code>SERPER_API_KEY</code></td>
      <td>API key for web search</td>
    </tr>
    <tr>
      <td><code>SERPER_NUM_RESULTS</code></td>
      <td>Number of search results to include in context</td>
    </tr>
    <tr>
      <td><code>WEATHER_CITY</code></td>
      <td>Set default city for weather display</td>
    </tr>
  </tbody>
</table>

<h2>📁 Project Structure</h2>

<pre><code>MirAi/
├── MirAi.py            # Main Python script
├── logo.png            # App & tray icon
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── dist/               # Compiled .exe output
└── .gitignore          # Excludes venv, __pycache__, etc.
</code></pre>


<h2>📄 License</h2>
This project is licensed under the MIT License — free to use, modify, and share.

<h2>🙌 Acknowledgements</h2>

OpenRouter – AI model aggregator

Serper.dev – Google Search API

wttr.in – Terminal weather

PySide6 – Qt for Python

<h2>👨‍💻 Author</h2>
<h3>Manan Sandhaliya</h3>

🎓 CSE(Spec. in AIML) and Tech Enthusiast at VIT Bhopal University.

📫 Reach out with feedback or suggestions!
