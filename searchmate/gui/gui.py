from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvgWidgets import *
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.center_window(1.5)

        self.setFocus()
        QApplication.instance().focusChanged.connect(self.on_focusChanged)

        self.icon = QSvgWidget("imgs/icon_search.svg")

        # setting frames
        self.setFrames()

        # Layout
        self.setLayouts()

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setFixedSize(self.width - self.icon_width, 60)
        self.search_bar.setPlaceholderText("Search something, mate")
        self.search_bar.returnPressed.connect(self.increaseWindow)

        # Settings of top Layout
        self.topLayoutSettings()

        # Example data
        self.data = [
            "Apple",
            "Banana",
            "Cherry",
            "Date",
            "Elderberry",
            "Fig",
            "Grape",
        ]

    def topLayoutSettings(self):
        # self.result_list = QListWidget()
        self.topLayout.addWidget(self.icFrame)
        self.topLayout.addWidget(self.icon, 0, 0)

        self.topLayout.addWidget(self.search_bar, 0, 1)
        self.topLayout.setAlignment(self.icon, Qt.AlignmentFlag.AlignCenter)
        # topLayout.addWidget(self.result_list,1,0)

    def setLayouts(self):
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.topLayout = QGridLayout()
        self.topLayout.setSpacing(0)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setContentsMargins(0, 10, 0, 0)
        self.mainLayout.addLayout(self.topLayout, 0, 0)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.rsFrame, 1, 0)

    def setFrames(self):
        self.icFrame = QFrame()
        self.icFrame.setFixedSize(self.icon_width, self.tmp_height - 10)

        self.rsFrame = QFrame()
        self.rsFrame.setFixedSize(self.width, 0)
        self.rsFrame.setStyleSheet(
            """border-top-left-radius: 0px; 
                                    border-bottom-right-radius: 16px;"""
        )

    def increaseWindow(self):
        self.search_bar.setStyleSheet("border-bottom-right-radius: 0px")
        self.icFrame.setStyleSheet("border-bottom-left-radius: 0px")
        if self.search_bar.text() == "chuj":
            self.setFixedSize(self.width, self.tmp_height)
            self.rsFrame.setFixedSize(self.width, 0)
            self.search_bar.setStyleSheet("border-bottom-right-radius: 14px")
            self.icFrame.setStyleSheet("border-bottom-left-radius: 14px")
        elif self.search_bar.text() == "dupa":
            self.setFixedSize(self.width, 460)
            self.mainLayout.addWidget(self.rsFrame, 1, 0)
            self.rsFrame.setFixedSize(self.width, 400 - 10)

    def resetWindowSize(self):
        self.rsFrame.hide()

    def center_window(self, const):
        self.screen = QApplication.primaryScreen()
        screen_x = self.screen.size().width()
        screen_y = self.screen.size().height()

        self.width = int(screen_x * 0.3 * const)
        self.height = int(screen_y / 2.13)

        self.icon_width = int(self.width / 13.5)

        self.width = self.width + self.icon_width
        self.tmp_height = 70
        print(self.width)
        print(int((screen_y - self.tmp_height) / 2))
        self.setFixedSize(self.width, self.tmp_height)
        self.x = int((screen_x - self.width) / 2)
        self.move(self.x, self.height)

    def update_list(self):
        self.result_list = QListWidget()

        # Clear the list
        self.result_list.clear()
        # Get the search text
        text = self.search_bar.text()
        # Add data to the list
        for item in self.data:
            if text.lower() in item.lower():
                self.result_list.addItem(QListWidgetItem(item))
        self.costam.addWidget(self.result_list, 1, 0)

    def on_focusChanged(self):
        print(self.isActiveWindow())
        if self.isActiveWindow() == False:
            QApplication.instance().quit()


app = QApplication(sys.argv)
with open("styles.css", "r") as file:
    app.setStyleSheet(file.read())
window = MainWindow()
window.show()
sys.exit(app.exec())
