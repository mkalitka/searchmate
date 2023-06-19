import os
import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvgWidgets import *
from searchmate.skill_loader import SkillLoader


STYLES_PATH = "styles.css"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._search_icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "assets/icon_search.svg"
        )

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.list_of_widgets = []

        self.center_window(1.5)

        self.setFocus()
        QApplication.instance().focusChanged.connect(self.on_focus_changed)

        self.icon = QSvgWidget(self._search_icon_path)

        # setting frames
        self.set_frames()

        # Layout
        self.set_layouts()

        # Load SkillLoader
        self._loader = SkillLoader()

        # Search bar
        self.set_search_bar()
        self.search_bar.textChanged.connect(self.suggestion)
        self.search_bar.returnPressed.connect(self.run)
        # Settings of top Layout
        self.top_layout_settings()

    # Position of window
    def center_window(self, const):
        self.screen = QApplication.primaryScreen()
        screen_x = self.screen.size().width()
        screen_y = self.screen.size().height()

        self.width = int(screen_x * 0.3 * const)
        self.height = int(screen_y / 3.4)

        self.icon_width = int(self.width / 13.5)

        self.width = self.width + self.icon_width
        self.tmp_height = 70
        self.setFixedSize(self.width, self.tmp_height)
        self.x = int((screen_x - self.width) / 2)
        self.move(self.x, self.height)

    # Settings
    def set_frames(self):
        self.icFrame = QFrame()
        self.icFrame.setFixedSize(self.icon_width, self.tmp_height - 10)

    def set_layouts(self):
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.topLayout = QGridLayout()
        self.topLayout.setSpacing(0)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setContentsMargins(0, 10, 0, 0)
        self.mainLayout.addLayout(self.topLayout, 0, 0)
        self.setLayout(self.mainLayout)

    def top_layout_settings(self):
        self.topLayout.addWidget(self.icFrame)
        self.topLayout.addWidget(self.icon, 0, 0)

        self.topLayout.addWidget(self.search_bar, 0, 1)
        self.topLayout.setAlignment(self.icon, Qt.AlignmentFlag.AlignCenter)

    def set_bottom_frame(self):
        self.rsFrame = QFrame()
        self.rsFrame.setFixedSize(self.width, 0)
        self.rsFrame.setObjectName("rsFrame")
        self.list_of_widgets.append(self.rsFrame)

    def set_search_bar(self):
        self.search_bar = QLineEdit(self)
        self.search_bar.setFixedSize(self.width - self.icon_width, 60)
        self.search_bar.setPlaceholderText("Search something, mate")
        self.search_bar.setFocus()

    def only_bar(self):
        self.remove_widgets()
        self.setFixedSize(self.width, self.tmp_height)
        self.search_bar.setStyleSheet("border-bottom-right-radius: 14px")
        self.icFrame.setStyleSheet("border-bottom-left-radius: 14px")

    def extended_bar(self):
        self.search_bar.setStyleSheet("border-bottom-right-radius: 0px")
        self.icFrame.setStyleSheet("border-bottom-left-radius: 0px")
        self.setFixedSize(self.width, 460)
        self.set_bottom_frame()
        self.mainLayout.addWidget(self.rsFrame, 1, 0)
        self.rsFrame.setFixedSize(self.width, 390)

    def suggestion(self):
        input = self.search_bar.text()

        if not input or input.isspace():
            self.only_bar()
        else:
            response = self._loader.get_suggestion(input)
            self.show_response(response)

    def run(self):
        input = self.search_bar.text()

        if not input or input.isspace():
            self.only_bar()
        else:
            response = self._loader.run(input)
            self.show_response(response)

    # Display
    def show_response(self, response):
        if response is None:
            self.only_bar()
        elif response["widget_type"] == "plain":
            self.extended_bar()
            self.plain(response["message"])
        elif response["widget_type"] == "markdown":
            self.extended_bar()
            self.markdown(response["message"])
        else:
            self.only_bar()

    def on_focus_changed(self):
        if self.isActiveWindow() == False:
            QApplication.instance().quit()

    def plain(self, message):
        label = QLabel(message)
        label.setObjectName("Result")
        self.mainLayout.addWidget(label, 1, 0)
        self.mainLayout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)
        self.list_of_widgets.append(label)

    def markdown(self, message):
        text_edit = QTextEdit(readOnly=True)
        text_edit.setFixedSize(self.width, 390)
        self.mainLayout.addWidget(text_edit, 1, 0)
        self.mainLayout.setAlignment(text_edit, Qt.AlignmentFlag.AlignCenter)
        text_edit.append(message)
        self.list_of_widgets.append(text_edit)

    def remove_widgets(self):
        for widget in self.list_of_widgets:
            if widget != None:
                self.mainLayout.removeWidget(widget)


def run():
    module_path = os.path.dirname(os.path.abspath(__file__))

    app = QApplication(sys.argv)

    # Load CSS file.
    with open(os.path.join(module_path, STYLES_PATH), "r") as file:
        app.setStyleSheet(file.read())

    window = MainWindow()
    window.show()

    app.exec()
