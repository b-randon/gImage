import sys
import os
import yaml
import serial
import time

from PySide.QtGui import *
from PySide.QtCore import *
from main_window import Ui_MainWindow
from settings_window import Ui_Form

baud_rates = [
    "9600",
    "38400",
    "115200",
    "230400",
    "250000",
    "256000"
]

class PrinterControl(QThread):
    rxSignal = Signal(str)
    txSignal = Signal(str)

    def __init__(self, args=None):
        QThread.__init__(self)
        self.running = True

        if args is not None:
            self.commands = args[0]
            self.port = args[1]

    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def run(self, *args, **kwargs):
        if self.port is None:
            print "Not Connect to Printer"

        while(1):
            if self.processGcode:
                # Try to Send the Next Command
                for i in self.commands:
                    if not self.running:
                        return
                    if (len(i) > 0) and (i != "\n"):
                        print i
                        self.rxSignal.emit(i)
                        self.port.write(str(i))

                        # Poll for the Response
                        response = self.port.readline()
                        self.txSignal.emit(response)

            else:
                # Send Any Pending Commands
                if self.



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Class Variables
        self.original_img = QImage()
        self.grayscale_img = QImage()
        self.generated_img = QImage()
        self.saved_grayscale_img = QImage()
        self.scene = QGraphicsScene()
        self.settingsDialog = QDialog(self)
        self.settingsUI = Ui_Form()
        self.settingsUI.setupUi(self.settingsDialog)
        self.serial_port = None
        self.printerThread = None

        if not os.path.exists('.\config'):
            os.makedirs('.\config')
            self.createConfigFile()
        else:
            if not os.path.isfile('.\config\config.yaml'):
                self.createConfigFile()

        # Read the Settings
        tmp_file = open('.\config\config.yaml', 'r')
        self.settings = yaml.safe_load(tmp_file)
        tmp_file.close()

        self.original_scene = QGraphicsScene()
        self.gray_scene = QGraphicsScene()
        self.generated_scene = QGraphicsScene()
        self.isNewFile = 0

        materials = self.settings['Gcode']['Materials']
        current_material = self.settings['Gcode']['Current']

        if self.settings['Gcode']['Materials']:
            self.material_combobox.addItem(current_material)
            self.over_min_pwr_edit.setText(str(self.settings['Gcode']['Materials'][current_material]['low_power']))
            self.over_max_pwr_edit.setText(
                str(self.settings['Gcode']['Materials'][current_material]['high_power']))
            self.over_feedrate_edit.setText(
                str(self.settings['Gcode']['Materials'][current_material]['feedrate']))

        for key, value in materials.iteritems():
            print key
            if key != current_material:
                self.material_combobox.addItem(key)

        # Menu Bar Action
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.setStatusTip('Open File')
        self.actionOpen.triggered.connect(self.showOpenDialog)

        self.actionSave.setShortcut('Ctrl+S')
        self.actionSave.setStatusTip('Save File')
        self.actionSave.triggered.connect(self.saveFile)

        self.actionSave_As.setStatusTip('Save File As')
        self.actionSave_As.triggered.connect(self.showSaveDialog)

        self.actionSettings.triggered.connect(self.showSettingsDialog)

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
        self.connect_button.pressed.connect(self.connectPrinter)

        # Tab Functions
        self.image_tabs.currentChanged.connect(self.onImageTabChange)
        self.tabWidget.currentChanged.connect(self.onMainTabChange)

        self.show()

    def RxHandler(self, message):
        self.comm_text_edit.insertPlainText("[TX]:" + message + "\n")

    def TxHandler(self, message):
        self.comm_text_edit.insertPlainText("RX]:" + message + "\n")

    def connectPrinter(self):
        port = self.usb_combo.currentText()

        if not port:
            print "No Port Selected"
            self.gcode_job_label.setText("No Port Selected")
        else:
            if str(self.connect_button.text()) == "Disconnect":
                if self.serial_port is not None:
                    self.serial_port.close()
                self.connect_button.setText("Connected")
                return
            else:
                try:
                    self.serial_port = serial.Serial(
                        port=str(self.usb_combo.currentText()),
                        baudrate=self.settings['Machine']['baud_rate'])
                except serial.SerialException:
                    self.gcode_job_label.setText("Could Not Connect")
                    return

            self.gcode_job_label.setText("Connected")
            self.connect_button.setText("Disconnect")

            # Grab the Current G-Code Commands
            gcode = self.plainTextEdit.toPlainText()
            gcode = gcode.split("\n")
            self.printerThread = PrinterControl((gcode, self.serial_port))
            # Connect Thread Signals
            self.printerThread.rxSignal.connect(self.RxHandler)
            self.printerThread.txSignal.connect(self.TxHandler)

            self.printerThread.start()

    def createConfigFile(self):
        print "Creating Config File"
        self.yaml_config_file = open('.\config\config.yaml', 'w+')
        settings = {'Machine': {'bed_length': 0, 'bed_width': 0, 'focus_distance': 0, 'laser_on_cmd': '',
                                'laser_pwr_cmd': '', 'laser_off_cmd': '', 'on_idle_delay': '', 'baud_rate': 9600},
                    'Gcode': {'Materials': {}, 'Current': '', 'start_gcode': '', 'end_gcode':''},
                    'Application': {'Auto_Size':'', 'xsize':'', 'ysize':''}}

        yaml.dump(settings, self.yaml_config_file)
        self.yaml_config_file.close()

    def onMainTabChange(self, argTabIndex):
        self.usb_combo.clear()
        if self.tabWidget.currentIndex() == 1:
            # Update the COM Ports List
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(256)]
            elif sys.platform.startswith('linux'):
                ports = glob.glob('/dev/tty[A-Za-z]*')
            else:
                print sys.platform + " Not Currently Supports"
                return

            port_list = []
            for port in ports:
                try:
                    s = serial.Serial(port)
                    s.close()
                    port_list.append(port)
                except (OSError, serial.SerialException):
                    pass

            self.usb_combo.addItems(port_list)

    def onImageTabChange(self, argTabIndex):
        if self.image_tabs.currentIndex() == 1:
            # Generate the Grayscale Image if Needed
            if self.isNewFile:
                self.isNewFile = 0

                if self.original_img.allGray():
                    self.grayscale_img = self.original_img.copy()
                    tmp_pixmap = QPixmap(self.grayscale_img)
                    self.scene.addPixmap(tmp_pixmap)
                    self.gray_image.setScene(self.scene)
                    self.gray_image.fitInView(self.gray_scene.sceneRect())
                    self.gray_image.show()
                else:
                    self.convertToGrayScale()

        if self.image_tabs.currentIndex() == 2:
            self.generatePrinterImage()

    def fillBoxes(self):
        if self.settings['Gcode']['Materials']:

            #Don't Trigger the Line Edit Signals
            self.settingsUI.maxpwr_line.blockSignals(1)
            self.settingsUI.minpwr_line.blockSignals(1)
            self.settingsUI.feedrate_line.blockSignals(1)

            self.settingsUI.minpwr_line.setText(
                self.settings['Gcode']['Materials'][self.settingsUI.material_combobox.currentText()]['low_power'])
            self.settingsUI.maxpwr_line.setText(
                self.settings['Gcode']['Materials'][self.settingsUI.material_combobox.currentText()]['high_power'])
            self.settingsUI.feedrate_line.setText(
                self.settings['Gcode']['Materials'][self.settingsUI.material_combobox.currentText()]['feedrate'])

            #Allow Signals Again
            self.settingsUI.maxpwr_line.blockSignals(0)
            self.settingsUI.minpwr_line.blockSignals(0)
            self.settingsUI.feedrate_line.blockSignals(0)


    def delMaterial(self):
        if self.settings['Gcode']['Materials']:
            del self.settings['Gcode']['Materials'][self.settingsUI.material_combobox.currentText()]
            self.settingsUI.material_combobox.removeItem(self.settingsUI.material_combobox.currentIndex())

    def addMaterial(self):
        text, ok = QInputDialog.getText(self, 'Material Name',
                                              'Enter the Material Name')
        if ok:
            #Add the Material to the Settings and Combobox
            self.settings['Gcode']['Materials'][str(text)] = dict(low_power='0', high_power='0', feedrate='0')
            print self.settings
            self.settingsUI.material_combobox.addItem(text)

    def setMinPower(self):
        self.settings['Gcode']['Materials'][self.settingsUI.material_combobox.currentText()]['low_power'] =\
            str(self.settingsUI.minpwr_line.text())
        self.settings['Gcode']['Materials'][self.settingsUI.material_combobox.currentText()]['high_power'] =\
            str(self.settingsUI.maxpwr_line.text())
        self.settings['Gcode']['Materials'][self.settingsUI.material_combobox.currentText()]['feedrate'] =\
            str(self.settingsUI.feedrate_line.text())

    def showSettingsDialog(self):
        # Populate the Fields
        tmp_file = open('.\config\config.yaml', 'r')
        self.settings = yaml.safe_load(tmp_file)
        tmp_file.close()

        self.settingsUI.bedlength_line.setText(str(self.settings['Machine']['bed_length']))
        self.settingsUI.bedwidth_line.setText(str(self.settings['Machine']['bed_width']))
        self.settingsUI.focus_line.setText(str(self.settings['Machine']['focus_distance']))
        self.settingsUI.laseron_line.setText(str(self.settings['Machine']['laser_on_cmd']))
        self.settingsUI.laserpwr_line.setText(str(self.settings['Machine']['laser_pwr_cmd']))
        self.settingsUI.laseroff_line.setText(str(self.settings['Machine']['laser_off_cmd']))
        self.settingsUI.idle_line.setText(str(self.settings['Machine']['on_idle_delay']))

        self.settingsUI.startgcode_edit.setText(self.settings['Gcode']['start_gcode'])
        self.settingsUI.endgcode_edit.setText(self.settings['Gcode']['end_gcode'])

        self.settingsUI.baud_rate_combo.clear()
        self.settingsUI.baud_rate_combo.addItems(baud_rates)

        if self.settings['Machine']['baud_rate'] is not None:
            index = self.settingsUI.baud_rate_combo.findText(str(self.settings['Machine']['baud_rate']), Qt.MatchFixedString)
            if index >= 0:
                self.settingsUI.baud_rate_combo.setCurrentIndex(index)


        if self.settings['Application']['Auto_Size'] == 'True':
            self.settingsUI.autoset_radio.setChecked(1)
            self.settingsUI.xautosize_line.setText(str(self.settings['Application']['xsize']))
            self.settingsUI.yautosize_line.setText(str(self.settings['Application']['ysize']))

        materials = self.settings['Gcode']['Materials']
        current_material = self.settings['Gcode']['Current']

        if self.settings['Gcode']['Materials']:
            self.settingsUI.material_combobox.addItem(current_material)
            self.settingsUI.minpwr_line.setText(str(self.settings['Gcode']['Materials'][current_material]['low_power']))
            self.settingsUI.maxpwr_line.setText(str(self.settings['Gcode']['Materials'][current_material]['high_power']))
            self.settingsUI.feedrate_line.setText(str(self.settings['Gcode']['Materials'][current_material]['feedrate']))

        for key, value in materials.iteritems():
            if key != current_material:
                self.settingsUI.material_combobox.addItem(key)

        # Connect the Widgets
        self.settingsUI.accept_button.pressed.connect(self.acceptSettings)
        self.settingsUI.close_button.pressed.connect(self.settingsDialog.close)
        self.settingsUI.material_combobox.currentIndexChanged.connect(self.fillBoxes)
        self.settingsUI.addmaterial_button.pressed.connect(self.addMaterial)
        self.settingsUI.delmaterial_button.pressed.connect(self.delMaterial)
        self.settingsUI.minpwr_line.textChanged.connect(self.setMinPower)
        self.settingsUI.maxpwr_line.textChanged.connect(self.setMinPower)
        self.settingsUI.feedrate_line.textChanged.connect(self.setMinPower)

        self.settingsDialog.show()

    def acceptSettings(self):
        # Update the Yaml File
        self.settings['Gcode']['Current'] = str(self.settingsUI.material_combobox.currentText())
        self.settings['Gcode']['start_gcode'] = str(self.settingsUI.startgcode_edit.toPlainText())
        self.settings['Gcode']['end_gcode'] = str(self.settingsUI.endgcode_edit.toPlainText())

        self.settings['Machine']['bed_length'] = str(self.settingsUI.bedlength_line.text())
        self.settings['Machine']['bed_width'] = str(self.settingsUI.bedwidth_line.text())
        self.settings['Machine']['focus_distance'] = str(self.settingsUI.focus_line.text())
        self.settings['Machine']['laser_off_cmd'] = str(self.settingsUI.laseroff_line.text())
        self.settings['Machine']['laser_on_cmd'] = str(self.settingsUI.laseron_line.text())
        self.settings['Machine']['laser_pwr_cmd'] = str(self.settingsUI.laserpwr_line.text())
        self.settings['Machine']['on_idle_delay'] = str(self.settingsUI.idle_line.text())
        self.settings['Machine']['baud_rate'] = int(self.settingsUI.baud_rate_combo.currentText())

        self.settings['Application']['Auto_Size'] = str(self.settingsUI.autoset_radio.isChecked())
        self.settings['Application']['xsize'] = str(self.settingsUI.xautosize_line.text())
        self.settings['Application']['ysize'] = str(self.settingsUI.yautosize_line.text())

        self.material_combobox.clear()

        items = [self.settingsUI.material_combobox.itemText(i) for i in range(self.settingsUI.material_combobox.count())]
        self.material_combobox.addItems(items)

        # Populate the Fields
        tmp_file = open('.\config\config.yaml', 'w')
        yaml.dump(self.settings, tmp_file)
        tmp_file.close()

        self.settingsDialog.close()

    def showOpenDialog(self):
        if self.tabWidget.currentIndex() == 0:
            file_name,_ = QFileDialog.getOpenFileName(self, 'Open file',
                                          '/', "Image files (*.jpg *.jpeg *.gif *.bmp);;GCode Files (*.gcode *.gco *.txt")
        else:
            file_name,_ = QFileDialog.getOpenFileName(self, 'Open file',

                                          '/', "GCode Files (*.gcode *.gco *.txt);;Image files (*.jpg *.jpeg *.gif *.bmp)")
        print file_name
        if file_name:
            file_ext = os.path.splitext(file_name)[1]
            if file_ext in (".jpg", ".gif", ".bmp"):
                # Open the Image File
                self.original_img.load(file_name)

                if self.settings['Application']['Auto_Size'] == 'True':
                    self.original_img = self.original_img.scaled(int(self.settings['Application']['xsize']), int(self.settings['Application']['ysize']), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

                self.isNewFile = 1

                # Create the Scene and Add it to the View
                img_pix = QPixmap(self.original_img)
                self.original_scene.clear()

                self.original_scene.addPixmap(img_pix)
                self.original_scene.setSceneRect(0, 0, self.original_img.width(), self.original_img.height())
                self.ysize_spinbox.setValue(self.original_img.height())
                self.xsize_spinbox.setValue(self.original_img.width())
                self.original_image.setScene(self.original_scene)

                self.original_image.fitInView(self.original_scene.sceneRect(), Qt.KeepAspectRatio)
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

                if (color.blue() * self.brightness_spinbox.value()) < 256:
                    tmp_blue = color.blue() * self.brightness_spinbox.value()
                else:
                    tmp_blue = 255

                factor = (259 * (self.contrast_spinbox.value() + 255)) / float(255 * (259 - self.contrast_spinbox.value()))

                tmp_red = factor * (tmp_red - 128) + 128
                tmp_green = factor * (tmp_green - 128) + 128
                tmp_blue = factor * (tmp_blue - 128) + 128

                if tmp_red > 255:
                    tmp_red = 255
                elif tmp_red < 0:
                    tmp_red = 0

                if tmp_green > 255:
                    tmp_green = 255
                elif tmp_green < 0:
                    tmp_green = 0

                if tmp_blue > 255:
                    tmp_blue = 255
                elif tmp_blue < 0:
                    tmp_blue = 0

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
        temp_scene.setSceneRect(0, 0, self.grayscale_img.width(), self.grayscale_img.height())
        self.gray_image.setScene(temp_scene)
        self.gray_image.fitInView(temp_scene.sceneRect(), Qt.KeepAspectRatio)
        self.gray_image.show()

        self.job_label.setText("Finished")
        self.job_progressbar.setValue(100)

    def generatePrinterImage(self):

        self.generated_img = QImage(int(self.settings['Machine']['bed_width']) + 2, int(self.settings['Machine']['bed_width']) + 2, QImage.Format_RGB888)

        # Change the Job Status
        self.job_label.setText("Generating Printer Image")
        self.job_label.repaint()

        for i in range(0, self.generated_img.width()):
            for j in range(0, self.generated_img.height()):
                self.generated_img.setPixel(i, j, qRgb(255, 255, 255))

        for i in range(0, int(self.settings['Machine']['bed_width']) + 1):
            self.generated_img.setPixel(i, 0, qRgb(0, 0, 0))

        for i in reversed(range(0, int(self.settings['Machine']['bed_width']) + 1)):
            self.generated_img.setPixel(i, int(self.settings['Machine']['bed_length']) + 1, qRgb(0, 0, 0))

        for i in range(0, int(self.settings['Machine']['bed_length']) + 1):
            self.generated_img.setPixel(0, i, qRgb(0, 0, 0))

        for i in reversed(range(0, int(self.settings['Machine']['bed_length']) + 1)):
            self.generated_img.setPixel(int(self.settings['Machine']['bed_width']) + 1, i, qRgb(0, 0, 0))

        gcode = self.plainTextEdit.toPlainText()
        gcode_lines = gcode.split("\n")

        x = 0
        y = 0
        power = -1
        for i in gcode_lines:
            if "G1 X" in i:
                x = float(i[4:])
            elif "G1 Y" in i:
                y = float(i[4:])
            elif self.settings['Machine']['laser_pwr_cmd'] in i:
                power = 255 - int(i[len(self.settings['Machine']['laser_pwr_cmd']):])

            if(power > 0):
                self.generated_img.setPixel(x + 1, y + 1, qRgb(power, power, power))


        pixmap = QPixmap(self.generated_img)
        temp_scene = QGraphicsScene()
        temp_scene.addPixmap(pixmap)
        temp_scene.setSceneRect(0, 0, self.generated_img.width(), self.generated_img.height())
        self.generated_image.setScene(temp_scene)
        self.generated_image.fitInView(temp_scene.sceneRect(), Qt.KeepAspectRatio)
        self.generated_image.show()

        self.job_label.setText("Finished")
        self.job_progressbar.setValue(100)

    def generateGcode(self):

        if not self.resolution_edit.text():
            return

        resolution = float(self.resolution_edit.text())

        if not self.original_img:
            print "No Image"
            return

        if not self.material_combobox.currentText():
            return



        if not self.grayscale_img:
            self.convertToGrayScale()
            self.isNewFile = False

        gcode = ''

        # Change the Job Status
        self.job_label.setText("Generating Gcode")
        self.job_label.repaint()

        #g-code Header
        gcode += self.settings['Gcode']['start_gcode'] + "\n\n"

       #Feedrate
        if not self.settings['Gcode']['Current']:
            print "No Material Selected"
            return

        gcode += self.settings['Machine']['laser_on_cmd'] + "\n"
        gcode += "G1 " + self.settings['Gcode']['Materials'][self.material_combobox.currentText()]['feedrate'] + "\n"

        old_color = -1
        yCoord = 0
        xCoord = 0

        current_material = self.settings['Gcode']['Current']


        min_pwr = int(self.settings['Gcode']['Materials'][current_material]['low_power'])
        max_pwr = int(self.settings['Gcode']['Materials'][current_material]['high_power'])

        #Loop Through All of the Pixels
        for i in range(0, self.original_img.height()):
            #Write to the Temp File to Save Memory
            yCoord += resolution
            gcode += "G1 Y" + str(yCoord) + "\n"

            # Update the Progress Bar
            if i > 0:
                self.job_progressbar.setValue(int((float(i) / self.original_img.width()) * 100))

            xCoord = 0

            for j in range(0, self.grayscale_img.width()):
                xCoord += resolution
                gcode += "G1 X" + str(xCoord) + "\n"
                color = QColor(self.grayscale_img.pixel(j, i))

                red = 255 - color.red()
                if red < min_pwr:
                    red = min_pwr
                if red > max_pwr:
                    red = max_pwr

                if old_color != red:
                    old_color = red
                    gcode +=  self.settings['Machine']['laser_pwr_cmd'] + str(red) + "\n"

        gcode += self.settings['Machine']['laser_off_cmd'] + "\n"

        #g-code Footer
        gcode += self.settings['Gcode']['end_gcode']

        print len(gcode)

        self.job_label.setText("Finished")
        self.job_progressbar.setValue(100)

        self.plainTextEdit.appendPlainText(gcode)
        self.tabWidget.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)

