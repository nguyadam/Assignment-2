import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QSpinBox,
                             QComboBox, QLabel, QScrollArea, QFrame)
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QWidget):
    def __init__(self, initial_url=None):
        super().__init__()
        self.init_ui(initial_url)

    def init_ui(self, initial_url):
        self.setFixedSize(1920, 1080)  # Set a fixed size for each browser window
        layout = QVBoxLayout()
        self.url_entry = QLineEdit(self)
        self.url_entry.setPlaceholderText("Enter URL here...")
        layout.addWidget(self.url_entry)

        self.open_url_button = QPushButton('Open URL', self)
        self.open_url_button.clicked.connect(self.load_url)
        layout.addWidget(self.open_url_button)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        if initial_url:  # Load the URL if provided during initialization
            self.url_entry.setText(initial_url)
            self.load_url()

    def load_url(self):
        url = self.url_entry.text()
        self.browser.load(QUrl(url))

    def get_current_url(self):
        return self.url_entry.text()

class WindowManager(QWidget):
    def __init__(self):
        super().__init__()
        self.windows = []
        self.urls = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Window Management App with Integrated Browser')
        self.setGeometry(100, 100, 800, 600)
        self.main_layout = QVBoxLayout(self)

        self.theme_label = QLabel("Select Theme Color:", self)
        self.main_layout.addWidget(self.theme_label)
        
        self.theme_combo = QComboBox(self)
        self.theme_combo.addItems(["Light", "Dark", "Custom"])  # Simplified theme options
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.main_layout.addWidget(self.theme_combo)

        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(1, 10)
        self.spin_box.setValue(1)
        self.spin_box.valueChanged.connect(self.update_windows)
        self.main_layout.addWidget(self.spin_box)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_frame = QFrame()
        self.scroll_frame.setLayout(QVBoxLayout())
        self.scroll_area.setWidget(self.scroll_frame)
        self.main_layout.addWidget(self.scroll_area)

        self.update_windows()

    def change_theme(self, index):
        if index == 0:  # Light theme
            self.setStyleSheet("QWidget { background-color: #FFFFFF; color: #000000; }")
        elif index == 1:  # Dark theme
            self.setStyleSheet("QWidget { background-color: #333333; color: #FFFFFF; }")
        elif index == 2:  # Custom theme
            self.setStyleSheet("QWidget { background-color: #FF69B4; color: #000000; }")

    def update_windows(self):
        if len(self.windows) > 0:
            self.urls = [win.get_current_url() for win in self.windows if isinstance(win, BrowserWindow)]

        for win in self.windows:
            win.setParent(None)
            win.deleteLater()

        self.windows = []

        for i in range(self.spin_box.value()):
            initial_url = self.urls[i] if i < len(self.urls) else ""
            window = BrowserWindow(initial_url)
            self.windows.append(window)
            self.scroll_frame.layout().addWidget(window)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WindowManager()
    ex.show()
    sys.exit(app.exec_())
