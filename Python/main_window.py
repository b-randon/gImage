# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\B\Desktop\git\gImage\UI\main_window.ui'
#
# Created: Thu Aug 11 23:12:15 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class MyGraphicsView(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
    def wheelEvent(self,event):
        adj = (event.delta()/120) * 0.1
        self.scale(1+adj,1+adj)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 645)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.image_tab = QtGui.QWidget()
        self.image_tab.setObjectName("image_tab")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.image_tab)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.image_tabs = QtGui.QTabWidget(self.image_tab)
        self.image_tabs.setObjectName("image_tabs")
        self.original_tab = QtGui.QWidget()
        self.original_tab.setObjectName("original_tab")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.original_tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.original_image = MyGraphicsView()
        self.original_image.setObjectName("original_image")
        self.horizontalLayout_4.addWidget(self.original_image)
        self.image_tabs.addTab(self.original_tab, "")
        self.gray_tab = QtGui.QWidget()
        self.gray_tab.setObjectName("gray_tab")
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.gray_tab)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.gray_image = MyGraphicsView()
        self.gray_image.setObjectName("gray_image")
        self.horizontalLayout_11.addWidget(self.gray_image)
        self.image_tabs.addTab(self.gray_tab, "")
        self.generated_tab = QtGui.QWidget()
        self.generated_tab.setObjectName("generated_tab")
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.generated_tab)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.generated_image = MyGraphicsView()
        self.generated_image.setObjectName("generated_image")
        self.horizontalLayout_10.addWidget(self.generated_image)
        self.image_tabs.addTab(self.generated_tab, "")
        self.horizontalLayout_6.addWidget(self.image_tabs)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.brightnes_label = QtGui.QLabel(self.image_tab)
        self.brightnes_label.setObjectName("brightnes_label")
        self.gridLayout_3.addWidget(self.brightnes_label, 0, 0, 1, 1)
        self.contrast_label = QtGui.QLabel(self.image_tab)
        self.contrast_label.setObjectName("contrast_label")
        self.gridLayout_3.addWidget(self.contrast_label, 2, 0, 1, 1)
        self.brightness_slider = QtGui.QSlider(self.image_tab)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(20)
        self.brightness_slider.setProperty("value", 10)
        self.brightness_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brightness_slider.setObjectName("brightness_slider")
        self.gridLayout_3.addWidget(self.brightness_slider, 1, 0, 1, 2)
        self.contrast_slider = QtGui.QSlider(self.image_tab)
        self.contrast_slider.setMinimum(-255)
        self.contrast_slider.setMaximum(255)
        self.contrast_slider.setProperty("value", 0)
        self.contrast_slider.setOrientation(QtCore.Qt.Horizontal)
        self.contrast_slider.setObjectName("contrast_slider")
        self.gridLayout_3.addWidget(self.contrast_slider, 4, 0, 1, 2)
        self.brightness_spinbox = QtGui.QDoubleSpinBox(self.image_tab)
        self.brightness_spinbox.setDecimals(1)
        self.brightness_spinbox.setMaximum(2.0)
        self.brightness_spinbox.setSingleStep(0.1)
        self.brightness_spinbox.setProperty("value", 1.0)
        self.brightness_spinbox.setObjectName("brightness_spinbox")
        self.gridLayout_3.addWidget(self.brightness_spinbox, 0, 1, 1, 1)
        self.contrast_spinbox = QtGui.QSpinBox(self.image_tab)
        self.contrast_spinbox.setMinimum(-255)
        self.contrast_spinbox.setMaximum(255)
        self.contrast_spinbox.setObjectName("contrast_spinbox")
        self.gridLayout_3.addWidget(self.contrast_spinbox, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.submit_button = QtGui.QPushButton(self.image_tab)
        self.submit_button.setObjectName("submit_button")
        self.verticalLayout.addWidget(self.submit_button)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.size_label = QtGui.QLabel(self.image_tab)
        self.size_label.setObjectName("size_label")
        self.gridLayout_5.addWidget(self.size_label, 2, 0, 1, 1)
        self.color_label = QtGui.QLabel(self.image_tab)
        self.color_label.setObjectName("color_label")
        self.gridLayout_5.addWidget(self.color_label, 0, 0, 1, 1)
        self.size_slider = QtGui.QSlider(self.image_tab)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(10)
        self.size_slider.setOrientation(QtCore.Qt.Horizontal)
        self.size_slider.setObjectName("size_slider")
        self.gridLayout_5.addWidget(self.size_slider, 3, 0, 1, 2)
        self.color_slider = QtGui.QSlider(self.image_tab)
        self.color_slider.setMinimum(0)
        self.color_slider.setMaximum(255)
        self.color_slider.setOrientation(QtCore.Qt.Horizontal)
        self.color_slider.setObjectName("color_slider")
        self.gridLayout_5.addWidget(self.color_slider, 1, 0, 1, 2)
        self.color_spinbox = QtGui.QSpinBox(self.image_tab)
        self.color_spinbox.setMaximum(255)
        self.color_spinbox.setObjectName("color_spinbox")
        self.gridLayout_5.addWidget(self.color_spinbox, 0, 1, 1, 1)
        self.size_spinbox = QtGui.QSpinBox(self.image_tab)
        self.size_spinbox.setMinimum(1)
        self.size_spinbox.setMaximum(10)
        self.size_spinbox.setObjectName("size_spinbox")
        self.gridLayout_5.addWidget(self.size_spinbox, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_5)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.square_button = QtGui.QToolButton(self.image_tab)
        self.square_button.setObjectName("square_button")
        self.horizontalLayout_7.addWidget(self.square_button)
        self.circle_button = QtGui.QToolButton(self.image_tab)
        self.circle_button.setObjectName("circle_button")
        self.horizontalLayout_7.addWidget(self.circle_button)
        self.eraser_button = QtGui.QToolButton(self.image_tab)
        self.eraser_button.setObjectName("eraser_button")
        self.horizontalLayout_7.addWidget(self.eraser_button)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rotate_left_button = QtGui.QToolButton(self.image_tab)
        self.rotate_left_button.setObjectName("rotate_left_button")
        self.horizontalLayout_2.addWidget(self.rotate_left_button)
        self.rotate_right_button = QtGui.QToolButton(self.image_tab)
        self.rotate_right_button.setObjectName("rotate_right_button")
        self.horizontalLayout_2.addWidget(self.rotate_right_button)
        self.flip_left_button = QtGui.QToolButton(self.image_tab)
        self.flip_left_button.setObjectName("flip_left_button")
        self.horizontalLayout_2.addWidget(self.flip_left_button)
        self.flip_right_button = QtGui.QToolButton(self.image_tab)
        self.flip_right_button.setObjectName("flip_right_button")
        self.horizontalLayout_2.addWidget(self.flip_right_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtGui.QLabel(self.image_tab)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 1, 1, 1)
        self.reslock_checkbox = QtGui.QCheckBox(self.image_tab)
        self.reslock_checkbox.setObjectName("reslock_checkbox")
        self.gridLayout_2.addWidget(self.reslock_checkbox, 1, 2, 1, 2)
        self.label_9 = QtGui.QLabel(self.image_tab)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.image_tab)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 1, 1, 1)
        self.resolution_edit = QtGui.QLineEdit(self.image_tab)
        self.resolution_edit.setObjectName("resolution_edit")
        self.gridLayout_2.addWidget(self.resolution_edit, 2, 2, 1, 1)
        self.ysize_spinbox = QtGui.QSpinBox(self.image_tab)
        self.ysize_spinbox.setMaximum(2160)
        self.ysize_spinbox.setObjectName("ysize_spinbox")
        self.gridLayout_2.addWidget(self.ysize_spinbox, 2, 0, 1, 1)
        self.xsize_spinbox = QtGui.QSpinBox(self.image_tab)
        self.xsize_spinbox.setMaximum(4096)
        self.xsize_spinbox.setObjectName("xsize_spinbox")
        self.gridLayout_2.addWidget(self.xsize_spinbox, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gcode_button = QtGui.QPushButton(self.image_tab)
        self.gcode_button.setObjectName("gcode_button")
        self.verticalLayout.addWidget(self.gcode_button)
        self.job_label = QtGui.QLabel(self.image_tab)
        self.job_label.setObjectName("job_label")
        self.verticalLayout.addWidget(self.job_label)
        self.job_progressbar = QtGui.QProgressBar(self.image_tab)
        self.job_progressbar.setProperty("value", 0)
        self.job_progressbar.setObjectName("job_progressbar")
        self.verticalLayout.addWidget(self.job_progressbar)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.horizontalLayout_6.setStretch(0, 10)
        self.horizontalLayout_6.setStretch(1, 1)
        self.tabWidget.addTab(self.image_tab, "")
        self.gcode_tab = QtGui.QWidget()
        self.gcode_tab.setObjectName("gcode_tab")
        self.horizontalLayout = QtGui.QHBoxLayout(self.gcode_tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gcode_tabs = QtGui.QTabWidget(self.gcode_tab)
        self.gcode_tabs.setObjectName("gcode_tabs")
        self.text_tab = QtGui.QWidget()
        self.text_tab.setObjectName("text_tab")
        self.gridLayout_7 = QtGui.QGridLayout(self.text_tab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.plainTextEdit = QtGui.QPlainTextEdit(self.text_tab)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_7.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.gcode_tabs.addTab(self.text_tab, "")
        self.job_gen_img_tab = QtGui.QWidget()
        self.job_gen_img_tab.setObjectName("job_gen_img_tab")
        self.gridLayout_9 = QtGui.QGridLayout(self.job_gen_img_tab)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.generated_image_2 = QtGui.QGraphicsView(self.job_gen_img_tab)
        self.generated_image_2.setObjectName("generated_image_2")
        self.gridLayout_9.addWidget(self.generated_image_2, 0, 0, 1, 1)
        self.gcode_tabs.addTab(self.job_gen_img_tab, "")
        self.comm_tab = QtGui.QWidget()
        self.comm_tab.setObjectName("comm_tab")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.comm_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtGui.QLabel(self.comm_tab)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.tansmit_text_edit = QtGui.QTextEdit(self.comm_tab)
        self.tansmit_text_edit.setObjectName("tansmit_text_edit")
        self.verticalLayout_4.addWidget(self.tansmit_text_edit)
        self.label_2 = QtGui.QLabel(self.comm_tab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.receive_text_edit = QtGui.QTextEdit(self.comm_tab)
        self.receive_text_edit.setObjectName("receive_text_edit")
        self.verticalLayout_4.addWidget(self.receive_text_edit)
        self.gcode_tabs.addTab(self.comm_tab, "")
        self.stats_tab = QtGui.QWidget()
        self.stats_tab.setObjectName("stats_tab")
        self.gcode_tabs.addTab(self.stats_tab, "")
        self.horizontalLayout.addWidget(self.gcode_tabs)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_8 = QtGui.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.override_checkbox = QtGui.QCheckBox(self.gcode_tab)
        self.override_checkbox.setObjectName("override_checkbox")
        self.gridLayout_8.addWidget(self.override_checkbox, 2, 0, 1, 1)
        self.material_combobox = QtGui.QComboBox(self.gcode_tab)
        self.material_combobox.setObjectName("material_combobox")
        self.gridLayout_8.addWidget(self.material_combobox, 1, 0, 1, 1)
        self.material_label = QtGui.QLabel(self.gcode_tab)
        self.material_label.setObjectName("material_label")
        self.gridLayout_8.addWidget(self.material_label, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_8)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.over_max_pwr_edit = QtGui.QLineEdit(self.gcode_tab)
        self.over_max_pwr_edit.setObjectName("over_max_pwr_edit")
        self.gridLayout_4.addWidget(self.over_max_pwr_edit, 3, 1, 1, 1)
        self.label_17 = QtGui.QLabel(self.gcode_tab)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 1, 2, 1, 1)
        self.max_pwr_label = QtGui.QLabel(self.gcode_tab)
        self.max_pwr_label.setObjectName("max_pwr_label")
        self.gridLayout_4.addWidget(self.max_pwr_label, 3, 0, 1, 1)
        self.feedrate_label = QtGui.QLabel(self.gcode_tab)
        self.feedrate_label.setObjectName("feedrate_label")
        self.gridLayout_4.addWidget(self.feedrate_label, 1, 0, 1, 1)
        self.over_feedrate_edit = QtGui.QLineEdit(self.gcode_tab)
        self.over_feedrate_edit.setObjectName("over_feedrate_edit")
        self.gridLayout_4.addWidget(self.over_feedrate_edit, 1, 1, 1, 1)
        self.over_min_pwr_edit = QtGui.QLineEdit(self.gcode_tab)
        self.over_min_pwr_edit.setObjectName("over_min_pwr_edit")
        self.gridLayout_4.addWidget(self.over_min_pwr_edit, 2, 1, 1, 1)
        self.min_pwr_label = QtGui.QLabel(self.gcode_tab)
        self.min_pwr_label.setObjectName("min_pwr_label")
        self.gridLayout_4.addWidget(self.min_pwr_label, 2, 0, 1, 1)
        self.eng_outline_checkbox = QtGui.QCheckBox(self.gcode_tab)
        self.eng_outline_checkbox.setObjectName("eng_outline_checkbox")
        self.gridLayout_4.addWidget(self.eng_outline_checkbox, 4, 0, 1, 3)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.pushButton = QtGui.QPushButton(self.gcode_tab)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem2)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.connect_button = QtGui.QPushButton(self.gcode_tab)
        self.connect_button.setObjectName("connect_button")
        self.gridLayout_6.addWidget(self.connect_button, 2, 0, 1, 3)
        self.job_start_button = QtGui.QPushButton(self.gcode_tab)
        self.job_start_button.setObjectName("job_start_button")
        self.gridLayout_6.addWidget(self.job_start_button, 4, 1, 1, 1)
        self.usb_combo = QtGui.QComboBox(self.gcode_tab)
        self.usb_combo.setObjectName("usb_combo")
        self.gridLayout_6.addWidget(self.usb_combo, 1, 0, 1, 3)
        self.label = QtGui.QLabel(self.gcode_tab)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 3)
        self.job_stop_button = QtGui.QPushButton(self.gcode_tab)
        self.job_stop_button.setObjectName("job_stop_button")
        self.gridLayout_6.addWidget(self.job_stop_button, 5, 1, 1, 2)
        self.job_pause_button = QtGui.QPushButton(self.gcode_tab)
        self.job_pause_button.setObjectName("job_pause_button")
        self.gridLayout_6.addWidget(self.job_pause_button, 4, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem3, 3, 1, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout_6)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem4)
        self.gcode_job_label = QtGui.QLabel(self.gcode_tab)
        self.gcode_job_label.setObjectName("gcode_job_label")
        self.verticalLayout_2.addWidget(self.gcode_job_label)
        self.progressBar = QtGui.QProgressBar(self.gcode_tab)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout.setStretch(1, 1)
        self.tabWidget.addTab(self.gcode_tab, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 31))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen = QtGui.QMenu(self.menuFile)
        self.menuOpen.setObjectName("menuOpen")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionGcode = QtGui.QAction(MainWindow)
        self.actionGcode.setObjectName("actionGcode")
        self.actionMachine = QtGui.QAction(MainWindow)
        self.actionMachine.setObjectName("actionMachine")
        self.actionApplication = QtGui.QAction(MainWindow)
        self.actionApplication.setObjectName("actionApplication")
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionRecent = QtGui.QAction(MainWindow)
        self.actionRecent.setEnabled(False)
        self.actionRecent.setObjectName("actionRecent")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionContents = QtGui.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.actionContents_2 = QtGui.QAction(MainWindow)
        self.actionContents_2.setObjectName("actionContents_2")
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuOpen.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuOpen.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionClose)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionContents_2)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.gcode_tabs.setCurrentIndex(0)
        self.image_tabs.setCurrentIndex(0)
        self.gcode_tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.image_tabs.setTabText(self.image_tabs.indexOf(self.original_tab), QtGui.QApplication.translate("MainWindow", "Original", None, QtGui.QApplication.UnicodeUTF8))
        self.image_tabs.setTabText(self.image_tabs.indexOf(self.gray_tab), QtGui.QApplication.translate("MainWindow", "Grayscale", None, QtGui.QApplication.UnicodeUTF8))
        self.image_tabs.setTabText(self.image_tabs.indexOf(self.generated_tab), QtGui.QApplication.translate("MainWindow", "Generated", None, QtGui.QApplication.UnicodeUTF8))
        self.brightnes_label.setText(QtGui.QApplication.translate("MainWindow", "Brightness", None, QtGui.QApplication.UnicodeUTF8))
        self.contrast_label.setText(QtGui.QApplication.translate("MainWindow", "Contrast", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_button.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.size_label.setText(QtGui.QApplication.translate("MainWindow", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.color_label.setText(QtGui.QApplication.translate("MainWindow", "Color", None, QtGui.QApplication.UnicodeUTF8))
        self.square_button.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.circle_button.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.eraser_button.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.rotate_left_button.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.rotate_right_button.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.flip_left_button.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.flip_right_button.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "X(px)", None, QtGui.QApplication.UnicodeUTF8))
        self.reslock_checkbox.setText(QtGui.QApplication.translate("MainWindow", "Aspect Lock", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "mm/px", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Y(px)", None, QtGui.QApplication.UnicodeUTF8))
        self.gcode_button.setText(QtGui.QApplication.translate("MainWindow", "Generate G-code", None, QtGui.QApplication.UnicodeUTF8))
        self.job_label.setText(QtGui.QApplication.translate("MainWindow", "No Job", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.image_tab), QtGui.QApplication.translate("MainWindow", "Image", None, QtGui.QApplication.UnicodeUTF8))
        self.gcode_tabs.setTabText(self.gcode_tabs.indexOf(self.text_tab), QtGui.QApplication.translate("MainWindow", "Gcode", None, QtGui.QApplication.UnicodeUTF8))
        self.gcode_tabs.setTabText(self.gcode_tabs.indexOf(self.job_gen_img_tab), QtGui.QApplication.translate("MainWindow", "Image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Transmit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Receive", None, QtGui.QApplication.UnicodeUTF8))
        self.gcode_tabs.setTabText(self.gcode_tabs.indexOf(self.comm_tab), QtGui.QApplication.translate("MainWindow", "Comm", None, QtGui.QApplication.UnicodeUTF8))
        self.gcode_tabs.setTabText(self.gcode_tabs.indexOf(self.stats_tab), QtGui.QApplication.translate("MainWindow", "Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.override_checkbox.setText(QtGui.QApplication.translate("MainWindow", "Override", None, QtGui.QApplication.UnicodeUTF8))
        self.material_label.setText(QtGui.QApplication.translate("MainWindow", "Material Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("MainWindow", "mm/s", None, QtGui.QApplication.UnicodeUTF8))
        self.max_pwr_label.setText(QtGui.QApplication.translate("MainWindow", "Max Power", None, QtGui.QApplication.UnicodeUTF8))
        self.feedrate_label.setText(QtGui.QApplication.translate("MainWindow", "Feedrate", None, QtGui.QApplication.UnicodeUTF8))
        self.min_pwr_label.setText(QtGui.QApplication.translate("MainWindow", "Min Power", None, QtGui.QApplication.UnicodeUTF8))
        self.eng_outline_checkbox.setText(QtGui.QApplication.translate("MainWindow", "Engrave Outline", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Generate G-Code", None, QtGui.QApplication.UnicodeUTF8))
        self.connect_button.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.job_start_button.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "USB Port", None, QtGui.QApplication.UnicodeUTF8))
        self.job_stop_button.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.job_pause_button.setText(QtGui.QApplication.translate("MainWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.gcode_job_label.setText(QtGui.QApplication.translate("MainWindow", "No Job", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gcode_tab), QtGui.QApplication.translate("MainWindow", "Gcode", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOpen.setTitle(QtGui.QApplication.translate("MainWindow", "Open Recent", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("MainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGcode.setText(QtGui.QApplication.translate("MainWindow", "Gcode", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMachine.setText(QtGui.QApplication.translate("MainWindow", "Machine", None, QtGui.QApplication.UnicodeUTF8))
        self.actionApplication.setText(QtGui.QApplication.translate("MainWindow", "Application", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRecent.setText(QtGui.QApplication.translate("MainWindow", "Recent", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionContents.setText(QtGui.QApplication.translate("MainWindow", "Contents", None, QtGui.QApplication.UnicodeUTF8))
        self.actionContents_2.setText(QtGui.QApplication.translate("MainWindow", "Contents", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
