from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, \
QListWidget, QListWidgetItem, QPushButton 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
import sys
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.center_window()
        # Layout
        layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        layout.addWidget(self.search_bar)

        # Search button
        self.search_button = QPushButton("Wyszukaj")
        self.search_button.clicked.connect(self.update_list)
        layout.addWidget(self.search_button)

        # List for results
        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        self.setLayout(layout)

        # Example data
        self.data = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]

    def center_window(self):
        screen = QApplication.primaryScreen()
        print(screen.size())
        screen_x = screen.size().width()
        screen_y = screen.size().height()
        const = 1.5
        width = int(screen_x * 0.34 * const)
        height = int(screen_y * 0.4 * const)
        self.resize(width, height)
    
        self.move(int((screen_x - width)/2),int((screen_y-height)/2*1.6))
        
    def update_list(self):
        # Clear the list
        self.result_list.clear()

        # Get the search text
        text = self.search_bar.text()

        # Add data to the list
        for item in self.data:
            if text.lower() in item.lower():
                self.result_list.addItem(QListWidgetItem(item))

    
    
    

app = QApplication([])
window = MainWindow()
window.show()
app.exec()