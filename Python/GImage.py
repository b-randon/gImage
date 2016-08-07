import sys
import os
import copy
from PySide.QtGui import *
from PySide.QtCore import *
from main_window import Ui_MainWindow
from settings_window import Ui_Form

class GCommand():
    def __init__(self, attr1 = None, attr2 = None, attr3 = None):
        if attr1 is None:
            self.command = ""
        else:
            self.command = attr1

        if attr2 is None:
            self.numArgs = 0
        else:
            self.numArgs = attr2

        if attr3 is None:
            self.args = []
        else:
            self.args = attr3

        def pushArg(self, arg):
            self.args.append(arg)
            self.numArgs += 1

        def popArg(self):
            self.args.pop()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Class Variables
        self.original_img = QImage()
        self.grayscale_img = QImage()
        self.generated_image = QImage()
        self.saved_grayscale_img = QImage()

        self.original_scene = QGraphicsScene()
        self.gray_scene = QGraphicsScene()
        self.generated_scene = QGraphicsScene()
        self.isNewFile = 0

        #Menu Bar Action
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.setStatusTip('Open File')
        self.actionOpen.triggered.connect(self.showOpenDialog)

        self.actionSave.setShortcut('Ctrl+S')
        self.actionSave.setStatusTip('Save File')
        self.actionSave.triggered.connect(self.saveFile)

        self.actionSave_As.setStatusTip('Save File As')
        self.actionSave_As.triggered.connect(self.showSaveDialog)

        # Image Toolbar
        self.brightness_slider.valueChanged.connect(self.changeSliderBrightness)
        self.contrast_slider.valueChanged.connect(self.contrast_spinbox.setValue)
        self.color_slider.valueChanged.connect(self.color_spinbox.setValue)
        self.size_slider.valueChanged.connect(self.size_spinbox.setValue)

        self.brightness_spinbox.valueChanged.connect(self.changeSpinboxBrightness)
        self.contrast_spinbox.valueChanged.connect(self.contrast_slider.setValue)
        self.color_spinbox.valueChanged.connect(self.color_slider.setValue)
        self.size_spinbox.valueChanged.connect(self.size_slider.setValue)

        self.submit_button.pressed.connect(self.changeSettings)

        # GCode Toolbar
        self.gcode_button.pressed.connect(self.generateGcode)

        # Tab Functions
        self.image_tabs.currentChanged.connect(self.onChange)
        self.show()

    def onChange(self, argTabIndex):
        if self.image_tabs.currentIndex() == 1:
            # Generate the Grayscale Image if Needed
            if self.isNewFile:
                self.isNewFile = 0

                if self.original_img.allGray():
                    self.grayscale_img = self.original_img.copy()
                    tmp_pixmap = QPixmap(self.grayscale_img)
                    self.scene.addPixmap(tmp_pixmap)
                    self.gray_image.setScene(self.scene)
                    self.gray_image.show()
                else:
                    self.convertToGrayScale()

    def showOpenDialog(self):
        if self.tabWidget.currentIndex() == 0:
            file_name,_ = QFileDialog.getOpenFileName(self, 'Open file',
                                          '/', "Image files (*.jpg *.jpeg *.gif *.bmp);;GCode Files (*.gcode *.gco *.txt")
        else:
            file_name,_ = QFileDialog.getOpenFileName(self, 'Open file',

                                          '/', "GCode Files (*.gcode *.gco *.txt);;Image files (*.jpg *.jpeg *.gif *.bmp)")
        file_ext = os.path.splitext(file_name)[1]
        if file_ext in (".jpg", ".gif", ".bmp"):
            # Open the Image File
            self.original_img.load(file_name)
            self.isNewFile = 1

            # Create the Scene and Add it to the View
            img_pix = QPixmap(self.original_img)
            self.original_scene.addPixmap(img_pix)
            self.ysize_spinbox.setValue(self.original_img.height())
            self.xsize_spinbox.setValue(self.original_img.width())
            self.original_image.setScene(self.original_scene)
            self.original_image.show()
            self.image_tabs.setCurrentIndex(0)
        else:
            text = open(file_name).read()
            self.plainTextEdit.setPlainText(text)
            self.plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)

    def showSaveDialog(self):
        print "Save File"

    def saveFile(self):
        print "Save"

    def changeSliderBrightness(self):
        self.brightness_spinbox.setValue(self.brightness_slider.value() / float(10))

    def changeSpinboxBrightness(self):
        self.brightness_slider.setValue(self.brightness_spinbox.value() * 10)

    def changeSettings(self):
        # Change the Job Status
        self.job_label.setText("Changing Image Settings")
        self.job_label.repaint()

        self.grayscale_img = self.saved_grayscale_img.copy()

        for i in range(0, self.grayscale_img.width()):
            # Update the Progress Bar
            if i > 0:
                self.job_progressbar.setValue(int((float(i) / self.saved_grayscale_img.width()) * 100))
            for j in range(0, self.saved_grayscale_img.height()):
                color = QColor(self.saved_grayscale_img.pixel(i, j))

                if (color.red() * self.brightness_spinbox.value()) < 256:
                    tmp_red = color.red() * self.brightness_spinbox.value()
                else:
                    tmp_red = 255
                if (color.green() * self.brightness_spinbox.value()) < 256:

                    tmp_green = color.green() * self.brightness_spinbox.value()
                else:
                    tmp_green = 255

                if (color.blue() * self.brightness_spinbox.value() < 256):
                    tmp_blue = color.blue() * self.brightness_spinbox.value()
                else:
                    tmp_blue = 255

                self.grayscale_img.setPixel(i, j, qRgb(tmp_red, tmp_green, tmp_blue))
                QCoreApplication.processEvents()

        tmp_pixmap = QPixmap(self.grayscale_img)
        self.gray_scene.addPixmap(tmp_pixmap)
        self.gray_image.setScene(self.gray_scene)

        self.job_label.setText("Finished")
        self.job_progressbar.setValue(100)

    def convertToGrayScale(self):
        # Convert the Image to Grayscale

        # Change the Job Status
        self.job_label.setText("Converting Image to Grayscale")
        self.job_label.repaint()

        self.grayscale_img = self.original_img.copy()

        for i in range(0, self.original_img.width()):
            # Update the Progress Bar
            if i > 0:
                self.job_progressbar.setValue(int((float(i) / self.original_img.width()) * 100))
            for j in range(0, self.original_img.height()):
                color = self.original_img.pixel(i, j)
                gray = qGray(color)
                self.grayscale_img.setPixel(i, j, qRgb(gray, gray, gray))
                QCoreApplication.processEvents()
        self.saved_grayscale_img = self.grayscale_img.copy()

        pixmap = QPixmap(self.grayscale_img)
        temp_scene = QGraphicsScene()
        temp_scene.addPixmap(pixmap)
        self.gray_image.setScene(temp_scene)
        self.gray_image.show()

        self.job_label.setText("Finished")
        self.job_progressbar.setValue(100)

    def generateGcode(self):
        # Change the Job Status
        self.job_label.setText("Generating Gcode")
        self.job_label.repaint()
        # Convert the Image to g-code
        for i in range(0, self.img.width()):
            # Update the Progress Bar
            if i > 0:
                self.job_progressbar.setValue(int((float(i) / self.img.width()) * 100))
            for j in range(0, self.img.height()):
                color = QColor(self.img.pixel(i, j))
                print color.red()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
