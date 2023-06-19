from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvgWidgets import *
from searchmate.skill_loader import SkillLoader
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.list_of_widgets = []

        self.center_window(1.5)

        self.setFocus()
        QApplication.instance().focusChanged.connect(self.on_focusChanged)

        self.icon = QSvgWidget("imgs/icon_search.svg")

        # setting frames
        self.set_frames()
        self.mod = ""
        # Layout
        self.set_layouts()

        # Search bar
        self.set_search_bar()
        self.search_bar.textChanged.connect(self.change_win_size)
        self.search_bar.returnPressed.connect(self.run)
        # Settings of top Layout
        self.top_layout_settings()

    # Position of window
    def center_window(self, const):
        self.screen = QApplication.primaryScreen()
        screen_x = self.screen.size().width()
        screen_y = self.screen.size().height()

        self.width = int(screen_x * 0.3 * const)
        self.height = int(screen_y / 2.13)

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
        self.rsFrame.setFixedSize(self.width, 400 - 10)

    # Display
    def change_win_size(self):  
        input = self.search_bar.text()
        check = self.isMatch(input)
        # print("slowo:" , input)
        
        if (not (input.strip())) ^ (check == None):
            self.only_bar()

        elif check != None:
            self.extended_bar()
            self.suggestion(check)

    # Other
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
        # print(self.isActiveWindow())
        if self.isActiveWindow() == False:
            QApplication.instance().quit()

    def suggestion(self,result):
        if self.mod == "math":
            label = QLabel(result)
            label.setObjectName("Result")
            self.mainLayout.addWidget(label,1,0)
            self.mainLayout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)
            self.list_of_widgets.append(label)
    def remove_widgets(self):
        for widget in self.list_of_widgets:
            if widget != None:
                self.mainLayout.removeWidget(widget)

    def run(self):
        if self.mod == "gpt":
            
            text_edit = QTextEdit()
            text_edit.setFixedSize(self.width,390)
            self.mainLayout.addWidget(text_edit,1,0)
            self.mainLayout.setAlignment(text_edit, Qt.AlignmentFlag.AlignCenter)
            text_edit.setFocus()
            first = self.search_bar.text()
            first = first.replace("gpt ","user: ")
            text_edit.append(first)
            self.list_of_widgets.append(text_edit)

    def isMatch(self, input):
        if "math" in input:
            self.mod = "math"

        elif "gpt" in input:
            self.mod = "gpt"
        loader = SkillLoader()
        result = loader.get_suggestion(input)
        return result

        

app = QApplication(sys.argv)
with open("styles.css", "r") as file:
    app.setStyleSheet(file.read())
window = MainWindow()
window.show()
sys.exit(app.exec())
