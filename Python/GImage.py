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
    progressSignal = Signal(int)
    createImageSignal = Signal(str)

    def __init__(self, args=None):
        QThread.__init__(self)
        self.running = True
        self.isJobRunning = False

        if args is not None:
            self.commands = args[0]
            self.port = args[1]

    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def jobRunning(self):
        return self.isJobRunning

    def startJob(self):
        print "Start Job"
        self.isJobRunning = True

    def pauseJob(self):
        print "Pause Job"
        self.isJobRunning = False

    def stopJob(self):
        print "Stop Job"
        self.isJobRunning = False

    def calibrate(self, gcode):
        self.commands = gcode
        self.isJobRunning = True

    def run(self, *args, **kwargs):

        if self.port is None:
            print "Not Connected to Printer"

        while(1):
            if not self.running:
                return

            if self.isJobRunning:
                totalSent = 0.0
                # Try to Send the Next Command
                self.progressSignal.emit(0)
                for i in self.commands:
                    totalSent += 1

                    self.progressSignal.emit(int(float(totalSent/len(self.commands)) * 100))
                    if not self.running:
                        return
                    if self.isJobRunning == 2:
                        continue
                    elif self.isJobRunning == 0:
                        break

                    if (len(i) > 0) and (i != "\n"):
                        self.txSignal.emit(i + "\n")
                        self.port.write(str(i) + "\n")

                        self.createImageSignal.emit(str(i))

                        # Poll for the Response
                        response = ""
                        i = 0
                        while True:
                            response = self.port.readline()
                            i += 1
                            if "\n" not in response:
                                if i > 5:
                                    self.rxSignal.emit("Timeout\n")
                                    break
                            elif "busy" in response:
                                print "Busy"
                                #Wait for a Bit
                                if i > 5:
                                    self.rxSignal.emit("Processing Timeout\n")
                                    break
                            else:
                                break

                        self.rxSignal.emit(response)
                self.isJobRunning = False
            else:
                # Send Any Pending Commands
                response = self.port.readline()
                if response:
                    self.rxSignal.emit(response)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Class Variables
        self.original_img = QImage()
        self.grayscale_img = QImage()
        self.generated_img = QImage()
        self.saved_grayscale_img = QImage()
        self.generated_img_2 = QImage()

        self.scene = QGraphicsScene()
        self.settingsDialog = QDialog(self)
        self.settingsUI = Ui_Form()
        self.settingsUI.setupUi(self.settingsDialog)

        #Settings Menu Setup
        self.settingsUI.calibrate_button.setDisabled(True)

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

        self.temp_x = 0
        self.temp_y = 0
        self.temp_power = 0

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
        self.send_button.pressed.connect(self.sendCommand)

        # GCode Toolbar
        self.gcode_button.pressed.connect(self.generateGcode)
        self.connect_button.pressed.connect(self.connectPrinter)
        self.job_start_button.pressed.connect(self.startJob)
        self.job_pause_button.pressed.connect(self.pauseJob)
        self.job_stop_button.pressed.connect(self.stopJob)

        # Tab Functions
        self.image_tabs.currentChanged.connect(self.onImageTabChange)
        self.tabWidget.currentChanged.connect(self.onMainTabChange)

        self.show()

# Button Handlers
    def startJob(self):
        if self.printerThread is None:
            self.gcode_job_label.setText("Not Connected")
        else:
            if not self.printerThread.jobRunning():
                self.printerThread.startJob()

    def pauseJob(self):
        if self.printerThread is not None:
            self.gcode_job_label.setText("Not Connected")
            self.printerThread.pauseJob()

    def stopJob(self):
        if self.printerThread is not None:
            self.gcode_job_label.setText("Not Connected")
            self.printerThread.stopJob()

    def sendCommand(self):
        self.TxHandler(str(self.command_edit.text()) + "\n")
        self.serial_port.write(str(self.command_edit.text()) + "\n")
        self.command_edit.clear()

    def RxHandler(self, message):
        self.comm_text_edit.setTextColor(QColor(150, 0, 0))
        self.comm_text_edit.insertPlainText("[RX]:" + message)
        self.comm_text_edit.moveCursor(QTextCursor.End)

    def TxHandler(self, message):
        self.comm_text_edit.setTextColor(QColor(0, 150, 0))
        self.comm_text_edit.insertPlainText("\n[TX]:" + message)
        self.comm_text_edit.moveCursor(QTextCursor.End)

    def updateGcodeImage(self, command):
        if "G1 X" in command:
            self.temp_x = float(command[4:])
        elif "G1 Y" in command:
            self.temp_y = float(command[4:])
        elif self.settings['Machine']['laser_pwr_cmd'] in command:
            self.temp_power = 255 - int(command[len(self.settings['Machine']['laser_pwr_cmd']):])

        if self.temp_power > 0:
            if self.temp_x < self.generated_img_2.width() and self.temp_y < self.generated_img_2.height():
                self.generated_img_2.setPixel(self.temp_x, self.temp_y, qRgb(self.temp_power, self.temp_power, self.temp_power))

        print self.temp_power

        pixmap = QPixmap(self.generated_img_2)
        temp_scene = QGraphicsScene()
        temp_scene.addPixmap(pixmap)
        temp_scene.setSceneRect(0, 0, self.generated_img_2.width(), self.generated_img_2.height())
        self.generated_image_2.setScene(temp_scene)
        self.generated_image_2.show()

    def disconnectPrinter(self):
        if str(self.connect_button.text()) == "Connected":
            if self.serial_port is not None:
                self.serial_port.close()
            self.connect_button.setText("Connected")
            self.connect_button.pressed.connect(self.connectPrinter)

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
                        baudrate=self.settings['Machine']['baud_rate'],
                        timeout=5)
                except serial.SerialException:
                    self.gcode_job_label.setText("Could Not Connect")
                    return

            self.gcode_job_label.setText("Connected")
            self.connect_button.setText("Disconnect")
            self.connect_button.pressed.connect(self.disconnectPrinter)

            # Grab the Current G-Code Commands
            gcode = self.plainTextEdit.toPlainText()
            gcode = gcode.split("\n")
            self.printerThread = PrinterControl((gcode, self.serial_port))
            # Connect Thread Signals
            self.printerThread.rxSignal.connect(self.RxHandler)
            self.printerThread.txSignal.connect(self.TxHandler)
            self.printerThread.progressSignal.connect(self.progressBar.setValue)
            self.printerThread.createImageSignal.connect(self.updateGcodeImage)

            self.settingsUI.calibrate_button.setDisabled(False)

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
        self.settingsUI.calibrate_button.pressed.connect(self.startCalibration)
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
                                          '/', "Image files (*.jpg *.jpeg *.gif *.bmp *.png);;GCode Files (*.gcode *.gco *.txt")
        else:
            file_name,_ = QFileDialog.getOpenFileName(self, 'Open file',

                                          '/', "GCode Files (*.gcode *.gco *.txt);;Image files (*.jpg *.jpeg *.gif *.bmp *.png)")
        print file_name
        if file_name:
            file_ext = os.path.splitext(file_name)[1]
            if file_ext in (".jpg", ".gif", ".bmp", ".png"):
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

    def startCalibration(self):

        # Generate the Gcode Commands
        tempGcode = []
        tempGcode.append("G28")
        tempGcode.append("G1 F" + self.settings['Gcode']['Materials'][self.material_combobox.currentText()]['feedrate'] + "\n")

        current_material = self.settings['Gcode']['Current']

        max_pwr = int(self.settings['Gcode']['Materials'][current_material]['high_power'])
        max_pwr - max_pwr * 0.8

        for i in range(0, 21):
            tempGcode.append("G1 Y%02.2f" % (i * 2))
            tempGcode.append("M400")
            tempGcode.append("M42 P4 S180")
            tempGcode.append("G1 X50.0")
            tempGcode.append("M400")
            tempGcode.append("M42 P4 S0")
            tempGcode.append("G1 X00.0")
            tempGcode.append("G1 Z%02.2f" % ((i+1) * 0.5))

        tempGcode.append("G28")
        tempGcode.append("M42 P4 S0")

        # Restart the Printer Thread
        self.printerThread.calibrate(tempGcode)

    def generatePrinterImage(self):

        if not self.resolution_edit.text():
            return

        resolution = float(self.resolution_edit.text())

        self.generated_img = QImage(((int(self.settings['Machine']['bed_width']) + 2) * (1/resolution)), ((int(self.settings['Machine']['bed_length']) + 2) * (1/resolution)), QImage.Format_RGB888)

        # Change the Job Status
        self.job_label.setText("Generating Printer Image")
        self.job_label.repaint()

        self.generated_img.fill(qRgb(255, 255, 255))

        for i in range(0, self.generated_img.width()):
            for j in range(0, int(1/resolution)):
                self.generated_img.setPixel(i, j, qRgb(0, 0, 0))

        for i in reversed(range(0, self.generated_img.width() - 1)):
            for j in range(0, int(1 / resolution)):
                self.generated_img.setPixel(i, (self.generated_img.height() - j) - 1, qRgb(0, 0, 0))

        for i in range(0, self.generated_img.height()):
            for j in range(0, int(1 / resolution)):
                self.generated_img.setPixel(j, i, qRgb(0, 0, 0))

        for i in reversed(range(0, self.generated_img.height() - 1)):
            for j in range(0, int(1 / resolution)):
                self.generated_img.setPixel((self.generated_img.width() - j) - 1, i, qRgb(0, 0, 0))

        gcode = self.plainTextEdit.toPlainText()
        gcode_lines = gcode.split("\n")

        x = 0
        y = 0
        counter = 0
        power = -1
        for i in gcode_lines:
            counter += 1
            # Update the Progress Bar
            if counter > 0:
                self.job_progressbar.setValue((counter / len(gcode_lines)) * 100)

            if "G1 X" in i:
                x = float(i[4:]) * (1/resolution)
            elif "G1 Y" in i:
                y = float(i[4:]) * (1/resolution)
            elif self.settings['Machine']['laser_pwr_cmd'] in i:
                power = 255 - int(i[len(self.settings['Machine']['laser_pwr_cmd']):])

            if power > 0:
                if x < self.generated_img.width() and y < self.generated_img.height():
                    self.generated_img.setPixel(x + (1/resolution), ((self.generated_img.height() - (1/resolution)) - y) , qRgb(power, power, power))

        pixmap = QPixmap(self.generated_img)
        temp_scene = QGraphicsScene()
        temp_scene.addPixmap(pixmap)
        temp_scene.setSceneRect(0, 0, self.generated_img.width(), self.generated_img.height())
        self.generated_image.setScene(temp_scene)
        self.generated_image.fitInView(temp_scene.sceneRect(), Qt.KeepAspectRatio)
        self.generated_image.show()

        pixmap = QPixmap(self.generated_img_2)
        temp_scene = QGraphicsScene()
        temp_scene.addPixmap(pixmap)
        temp_scene.setSceneRect(0, 0, self.generated_img_2.width(), self.generated_img_2.height())
        self.generated_image_2.setScene(temp_scene)
        self.generated_image_2.fitInView(temp_scene.sceneRect(), Qt.KeepAspectRatio)
        self.generated_image_2.show()

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
        self.plainTextEdit.clear()

        # Change the Job Status
        self.job_label.setText("Generating Gcode")
        self.job_label.repaint()

        #g-code Header
        gcode += self.settings['Gcode']['start_gcode'] + "\n\n"

        #Set the Focal Distance for the Z Axis
        gcode += "G1 Z%02.01i" % float(self.settings['Machine']['focus_distance']) + "\n"

       #Feedrate
        if not self.settings['Gcode']['Current']:
            print "No Material Selected"
            return

        gcode += self.settings['Machine']['laser_on_cmd'] + "\n"
        gcode += "G1 F" + self.settings['Gcode']['Materials'][self.material_combobox.currentText()]['feedrate'] + "\n"

        old_color = -1
        yCoord = 0.0
        xCoord = 0.0

        current_material = self.settings['Gcode']['Current']


        min_pwr = int(self.settings['Gcode']['Materials'][current_material]['low_power'])
        max_pwr = int(self.settings['Gcode']['Materials'][current_material]['high_power'])

        i = 0
        direction = 1

        #Loop Through All of the Pixels
        for i in range(0, self.original_img.height()):
            gcode += "G1 Y" + str(yCoord) + "\n"

            # Update the Progress Bar
            if i > 0:
                self.job_progressbar.setValue(int((float(i) / self.original_img.width()) * 100))

            for j in range(0, self.original_img.width()):

                gcode += "G1 X" + str(xCoord) + "\n"

                if direction > 0:
                    color = QColor(self.grayscale_img.pixel(((self.original_img.width() - 1) - j),
                                                            (self.original_img.height() - 1) - i))
                else:
                    color = QColor(self.grayscale_img.pixel(j,
                                                            (self.original_img.height() - 1) - i))

                red = 255 - color.red()
                if red < min_pwr:
                    red = min_pwr
                if red > max_pwr:
                    red = max_pwr

                if old_color != red:
                    old_color = red

                    #Wait for the Movement Commands to Finish First Before Changing the Power
                    gcode += "M400\n"
                    gcode +=  self.settings['Machine']['laser_pwr_cmd'] + str(red) + "\n"

                if direction > 0:
                    xCoord += resolution
                else:
                    xCoord -= resolution

                xCoord = round(xCoord, 3)

            if direction > 0:
                xCoord -= resolution
            else:
                xCoord += resolution

            direction = direction * -1
            yCoord += resolution
            yCoord = round(yCoord, 3)

            #Turn Off the Laser When Moving in the Y Direction
            gcode += "M400\n"
            gcode += self.settings['Machine']['laser_pwr_cmd'] + "0" + "\n"

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

