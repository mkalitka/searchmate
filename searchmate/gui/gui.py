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
        # self.setStyleSheet("background-color: white; border-radius: 10px;")
        self.search_bar = QLineEdit(self)
        self.center_window()

        self.setFocus()
        QApplication.instance().focusChanged.connect(self.on_focusChanged)
        

        self.icon = QSvgWidget('imgs/icon_search.svg')
        
        frame = QFrame()
        frame.setFixedSize(60,self.tmp_height)
        # Layout
        topLayout = QGridLayout()
        topLayout.setSpacing(0)
        topLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(topLayout)

        # Search bar
        
        self.search_bar.returnPressed.connect(self.update_list)

        # List for results
        # self.result_list = QListWidget()
        topLayout.addWidget(frame)
        topLayout.addWidget(self.icon,0,0)
        topLayout.addWidget(self.search_bar,0,1)
        topLayout.setAlignment(self.icon,Qt.AlignmentFlag.AlignCenter)
        # line_edit.addAction(icon)
        # topLayout.addWidget(self.result_list,1,0)

        # Example data
        self.data = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]

    def center_window(self):

        screen = QApplication.primaryScreen()
        screen_x = screen.size().width()
        screen_y = screen.size().height()

        const = 1.5
        self.width = int(screen_x * 0.3 * const)
        self.height = int(screen_y * 0.4 * const)
        self.tmp_height = self.search_bar.sizeHint().height() 
        self.resize(self.width, self.tmp_height)
    
        self.move(int((screen_x - self.width)/2),int((screen_y-self.tmp_height)/2))
        
    def update_list(self):
        # Clear the list
        self.result_list.clear()
        # Get the search text
        text = self.search_bar.text()
        # Add data to the list
        for item in self.data:
            if text.lower() in item.lower():
                self.result_list.addItem(QListWidgetItem(item))

    def on_focusChanged(self):
        print(self.isActiveWindow())
        if self.isActiveWindow() == False:
            QApplication.instance().quit()


app = QApplication(sys.argv)
with open("styles.css", "r") as file:
    app.setStyleSheet(file.read())
window = MainWindow()
# window.setStyleSheet("border-radius: 20px;")
window.show()
sys.exit(app.exec())
