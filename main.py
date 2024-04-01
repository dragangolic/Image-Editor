from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QListWidget, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter, ImageEnhance
import os
from PyQt5.QtGui import QPixmap


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
    return results


# Choose current work directory
def getWorkDirectory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    extensions = ['.jpg', '.jpeg', 'png', 'svg']
    filenames = filter(os.listdir(working_directory), extensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)


class Editor:
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = "edits/"

    def load_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()

    def save_image(self):
        path = os.path.join(working_directory, self.save_folder)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)

        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image = image.scaled(w, h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()

    def transformimage(self, transformation):
        transformations = {
                "Left": lambda image: image.transpose(Image.Transpose.ROTATE_90),
                "Right": lambda image: image.transpose(Image.Transpose.ROTATE_270),
                "Mirror": lambda image: image.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
                "Sharpen": lambda image: image.filter(ImageFilter.SHARPEN),
                "B/W": lambda image: image.convert("L"),
                "Color": lambda image: ImageEnhance.Color(image).enhance(1.2),
                "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(1.2),
                "Blur": lambda image: image.filter(ImageFilter.BLUR)
        }

        transform_function = transformations.get(transformation)
        if transform_function:
            self.image = transform_function(self.image)
            self.save_image()
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)


    def apply_filter(self, filter_name):
        if filter_name == "Original":
            self.image = self.original.copy()
        else:
            mapping = {
                "Left": lambda image: image.transpose(Image.Transpose.ROTATE_90),
                "Right": lambda image: image.transpose(Image.Transpose.ROTATE_270),
                "Mirror": lambda image: image.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
                "Sharpen": lambda image: image.filter(ImageFilter.SHARPEN),
                "B/W": lambda image: image.convert("L"),
                "Color": lambda image: ImageEnhance.Color(image).enhance(1.2),
                "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(1.2),
                "Blur": lambda image: image.filter(ImageFilter.BLUR)
            }
            filter_function = mapping.get(filter_name)
            # check if there is a value
            if filter_function:
                self.image = filter_function(self.image)
                self.save_image()
                image_path = os.path.join(working_directory, self.save_folder, self.filename)
                self.show_image(image_path)
            pass
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)


def handle_filter():
    if file_list.currentRow() >= 0:
        select_filter = filter_box.currentText()
        main.apply_filter(select_filter)


def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.load_image(filename)
        main.show_image(os.path.join(working_directory, main.filename))


main = Editor()

# Events
btn_folder.clicked.connect(getWorkDirectory)
file_list.currentRowChanged.connect(displayImage)
filter_box.currentTextChanged.connect(handle_filter)

btn_left.clicked.connect(lambda: main.transformimage("Left"))
btn_right.clicked.connect(lambda: main.transformimage("Right"))
mirror.clicked.connect(lambda: main.transformimage("Mirror"))
sharpness.clicked.connect(lambda: main.transformimage("Sharpen"))
gray.clicked.connect(lambda: main.transformimage("Gray"))
saturation.clicked.connect(lambda: main.transformimage("Color"))
contrast.clicked.connect(lambda: main.transformimage("Contrast"))
blur.clicked.connect(lambda: main.transformimage("Blur"))


# Start/Execution
main_window.setLayout(master_layout)
main_window.show()
app.exec_()
