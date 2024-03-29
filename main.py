from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QListWidget, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter, ImageEnhance
import os
from PyQt5.QtGui import QPixmap


with Image.open("urubamba.jpg")as pic:
    #pic.show()

    saturate = ImageEnhance.Color(pic)
    saturate = saturate.enhance(1.2)

    #saturate.show()

    black_white = pic.convert("L")
    black_white.save("gray_urubamba.jpg")
    #black_white.show()

    mirror = pic.transpose(Image.FLIP_LEFT_RIGHT)
    mirror.save("mirror_urubamba.jpg")
    #mirror.show()

    blur = pic.filter(ImageFilter.BLUR)
    blur.save("blur_urubamba.jpg")
    #blur.show()

    # ImageEnhance
    contrast = ImageEnhance.Contrast(pic)
    contrast = contrast.enhance(2.5)
    contrast.save("contrast_urubamba.jpg")
    #contrast.show()

    color = ImageEnhance.Color(pic).enhance(2.7)
    color.save("color_urubamba.jpg")
    #color.show()

# App Settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("PhotoApp")
main_window.resize(900, 700)

# Widgets/Objects
btn_folder = QPushButton("Folder")

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror = QPushButton("Mirror")
sharpness = QPushButton("Sharpness")
gray = QPushButton("Gray")
saturation = QPushButton("Saturation")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")

file_list = QListWidget()

# Dropdown box

filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("Left")
filter_box.addItem("Right")
filter_box.addItem("Mirror")
filter_box.addItem("Sharpen")
filter_box.addItem("B/W")
filter_box.addItem("Color")
filter_box.addItem("Contrast")
filter_box.addItem("Blur")

picture_box = QLabel("Image will appear here")

# App Design
master_layout = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()
col3 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(filter_box)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(gray)
col1.addWidget(saturation)
col1.addWidget(contrast)
col1.addWidget(blur)

col2.addWidget(picture_box)

col3.addWidget(file_list)

master_layout.addLayout(col1, 10)
master_layout.addLayout(col2, 70)
master_layout.addLayout(col3, 20)

# App Functionality

working_directory = ""

# Filter files and extensions
def filter(files, extensions):
    results = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)

# Choose current work directory
def getWorkDirectory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    extensions = ['.jpg', '.jpeg', 'png', 'svg']
    filenames = filter(os.listdir(working_directory), extensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)

btn_folder.clicked.connect(getWorkDirectory)

# Start/Execution
main_window.setLayout(master_layout)
main_window.show()
app.exec_()
