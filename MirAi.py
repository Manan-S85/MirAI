from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton, QLabel, QSlider, QCheckBox,
    QSystemTrayIcon, QMenu
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
import sys, threading, requests, time
from openai import OpenAI
import keyboard  # keyboard lib for polling hotkey

# ------------------------------------------------------------------ CONFIG
OPENROUTER_API_KEY = "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"
SERPER_API_KEY     = "a95185ae731e522b65311f165d03cbf03af92ef3"
SERPER_NUM_RESULTS = 3
DEFAULT_MODEL      = "mistralai/mistral-7b-instruct:free"

# Weather config (wttr.in requires no key)
WEATHER_CITY = "Bhopal"
# -------------------------------------------------------------------------

class StylishAIAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MirAi")
        self.setFixedSize(700, 500)

        self.temperature      = 0.7
        self.serper_available = True

        self.client = OpenAI(api_key=OPENROUTER_API_KEY,
                             base_url="https://openrouter.ai/api/v1")

        self.setup_ui()
        self.setup_tray()
        self.apply_styles()

        self.hide()
        self._last_hotkey_trigger = 0

        self.hotkey_timer = QTimer()
        self.hotkey_timer.timeout.connect(self.check_hotkey)
        self.hotkey_timer.start(100)

        # Clock and weather
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_datetime_weather)
        self.clock_timer.start(1000)
        self.update_datetime_weather()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("🤖 MirAi")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Top info bar
        info_row = QHBoxLayout()
        self.datetime_label = QLabel()
        self.weather_label = QLabel()
        info_row.addWidget(self.datetime_label)
        info_row.addStretch()
        info_row.addWidget(self.weather_label)
        layout.addLayout(info_row)

        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Ask your question here…")
        layout.addWidget(self.query_input)

        temp_row = QHBoxLayout()
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setRange(1, 10)
        self.temp_slider.setValue(7)
        self.temp_slider.valueChanged.connect(self.on_temp_change)
        self.temp_label = QLabel("Creativity: 0.7")
        temp_row.addWidget(self.temp_label)
        temp_row.addWidget(self.temp_slider)
        layout.addLayout(temp_row)

        self.search_checkbox = QCheckBox("Enable Live Search")
        self.search_checkbox.setChecked(True)
        layout.addWidget(self.search_checkbox)

        self.ask_button = QPushButton("Ask MirAi")
        self.ask_button.clicked.connect(self.ask_ai)
        layout.addWidget(self.ask_button)

        self.output_box = QTextEdit(readOnly=True)
        layout.addWidget(self.output_box)

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(QIcon("logo.png"), self)
        menu = QMenu()
        menu.addAction("Open", self.show_and_raise)
        menu.addAction("Exit", QApplication.instance().quit)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.setToolTip("MirAi Assistant")
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_and_raise()

    def show_and_raise(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.query_input.setFocus()

    def closeEvent(self, e):
        e.ignore()
        self.hide()

    def check_hotkey(self):
        now = time.time()
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('k'):
            if now - self._last_hotkey_trigger > 0.7:
                print("🧠 Ctrl+K detected (polling)!")
                self._last_hotkey_trigger = now
                self.summon_window()

    def summon_window(self):
        self.show_and_raise()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {background:#121212; color:#EEE; font-family:'Segoe UI',sans-serif;}
            QLineEdit,QTextEdit {background:#1E1E1E; border:1px solid #444; border-radius:6px; padding:10px; font-size:14px;}
            QPushButton {background:#007ACC; border-radius:8px; padding:10px; font-weight:bold; font-size:16px; color:white;}
            QPushButton:hover {background:#005999;}
            QSlider::groove:horizontal {height:6px; background:#444; border-radius:3px;}
            QSlider::handle:horizontal {background:#007ACC; width:14px; height:14px; border-radius:7px; margin:-4px 0;}
            QCheckBox, QLabel {font-size:14px;}
        """)

    def on_temp_change(self, val):
        self.temperature = val / 10.0
        self.temp_label.setText(f"Creativity: {self.temperature:.1f}")

    def ask_ai(self):
        q = self.query_input.text().strip()
        if not q:
            return
        self.output_box.append(f"\n<b>You:</b> {q}")
        self.query_input.clear()
        threading.Thread(target=self.generate_response, args=(q,), daemon=True).start()

    def generate_response(self, query):
        context = self.live_search_serper(query)
        prompt = f"{query}\n\n{context}\n\nUsing ONLY the information above, answer clearly." if context else query
        try:
            res = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": prompt}],
                temperature=self.temperature
            )
            ans = res.choices[0].message.content.strip()
        except Exception as e:
            ans = f"<i>Error:</i> {e}"
        self.output_box.append(f"<b>AI:</b> {ans}")

    def live_search_serper(self, query):
        if not self.serper_available or not self.search_checkbox.isChecked():
            return None
        try:
            r = requests.post("https://google.serper.dev/search",
                              json={"q": query, "num": SERPER_NUM_RESULTS},
                              headers={"X-API-KEY": SERPER_API_KEY}, timeout=10)
            if r.status_code == 429:
                self.serper_available = False
                return None
            r.raise_for_status()
            data = r.json()
            snippets = []
            if (ab := data.get("answerBox", {})).get("answer"):
                snippets.append(f'AnswerBox: {ab["answer"]}')
            if (kg := data.get("knowledgeGraph")) and kg.get("title"):
                snippets.append(f'KnowledgeGraph: {kg["title"]} – {kg.get("description","")}')
            for res in data.get("organic", [])[:SERPER_NUM_RESULTS]:
                snippets.append(f'"{res.get("title","")}" – {res.get("snippet","")}')
            return "Recent Web Results:\n" + "\n".join(snippets) if snippets else None
        except Exception as e:
            print("[Serper error]", e)
            self.serper_available = False
            return None

    def update_datetime_weather(self):
        now = datetime.now().strftime("%A, %d %b %Y  %I:%M %p")
        self.datetime_label.setText(f"📅 {now}")
        if not hasattr(self, "_last_weather_update") or \
           (datetime.now().timestamp() - self._last_weather_update > 600):
            threading.Thread(target=self.fetch_weather, daemon=True).start()

    def fetch_weather(self):
        try:
            url = f"https://wttr.in/{WEATHER_CITY}?format=%t+%C"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                weather = res.text.strip()
                self.weather_label.setText(f"🌤 {WEATHER_CITY}: {weather}")
            else:
                self.weather_label.setText("⚠️ Weather Unavailable")
            self._last_weather_update = datetime.now().timestamp()
        except:
            self.weather_label.setText("⚠️ Weather Unavailable")

# ------------------------------------------------------------------ MAIN
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StylishAIAssistant()
    sys.exit(app.exec())
