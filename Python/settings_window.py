# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\B\Desktop\git\gImage\UI\settings_window.ui'
#
# Created: Fri Dec 02 22:57:01 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(412, 300)
        Form.setMaximumSize(QtCore.QSize(500, 300))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.frame_3 = QtGui.QFrame(self.tab)
        self.frame_3.setGeometry(QtCore.QRect(0, 10, 221, 201))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bedlength_line = QtGui.QLineEdit(self.frame_3)
        self.bedlength_line.setObjectName("bedlength_line")
        self.gridLayout_2.addWidget(self.bedlength_line, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.laseron_line = QtGui.QLineEdit(self.frame_3)
        self.laseron_line.setObjectName("laseron_line")
        self.gridLayout_2.addWidget(self.laseron_line, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.frame_3)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.frame_3)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.idle_line = QtGui.QLineEdit(self.frame_3)
        self.idle_line.setObjectName("idle_line")
        self.gridLayout_2.addWidget(self.idle_line, 7, 1, 1, 1)
        self.focus_line = QtGui.QLineEdit(self.frame_3)
        self.focus_line.setObjectName("focus_line")
        self.gridLayout_2.addWidget(self.focus_line, 3, 1, 1, 1)
        self.laserpwr_line = QtGui.QLineEdit(self.frame_3)
        self.laserpwr_line.setObjectName("laserpwr_line")
        self.gridLayout_2.addWidget(self.laserpwr_line, 5, 1, 1, 1)
        self.laseroff_line = QtGui.QLineEdit(self.frame_3)
        self.laseroff_line.setObjectName("laseroff_line")
        self.gridLayout_2.addWidget(self.laseroff_line, 6, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.frame_3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 6, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.frame_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.frame_3)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.frame_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 5, 0, 1, 1)
        self.bedwidth_line = QtGui.QLineEdit(self.frame_3)
        self.bedwidth_line.setObjectName("bedwidth_line")
        self.gridLayout_2.addWidget(self.bedwidth_line, 1, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.frame_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 7, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.frame_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 7, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 2, 1, 1)
        self.verticalLayoutWidget = QtGui.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(240, 20, 101, 89))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_33 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_33.setObjectName("label_33")
        self.verticalLayout_4.addWidget(self.label_33)
        self.baud_rate_combo = QtGui.QComboBox(self.verticalLayoutWidget)
        self.baud_rate_combo.setObjectName("baud_rate_combo")
        self.verticalLayout_4.addWidget(self.baud_rate_combo)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.calibrate_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.calibrate_button.setObjectName("calibrate_button")
        self.verticalLayout_4.addWidget(self.calibrate_button)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame = QtGui.QFrame(self.tab_2)
        self.frame.setGeometry(QtCore.QRect(220, 10, 161, 181))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_16 = QtGui.QLabel(self.frame)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_2.addWidget(self.label_16)
        self.startgcode_edit = QtGui.QTextEdit(self.frame)
        self.startgcode_edit.setObjectName("startgcode_edit")
        self.verticalLayout_2.addWidget(self.startgcode_edit)
        self.label_17 = QtGui.QLabel(self.frame)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_2.addWidget(self.label_17)
        self.endgcode_edit = QtGui.QTextEdit(self.frame)
        self.endgcode_edit.setObjectName("endgcode_edit")
        self.verticalLayout_2.addWidget(self.endgcode_edit)
        self.frame_2 = QtGui.QFrame(self.tab_2)
        self.frame_2.setGeometry(QtCore.QRect(10, 10, 191, 181))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.minpwr_line = QtGui.QLineEdit(self.frame_2)
        self.minpwr_line.setObjectName("minpwr_line")
        self.gridLayout_4.addWidget(self.minpwr_line, 1, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.frame_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)
        self.label_14 = QtGui.QLabel(self.frame_2)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 3, 0, 1, 1)
        self.feedrate_line = QtGui.QLineEdit(self.frame_2)
        self.feedrate_line.setObjectName("feedrate_line")
        self.gridLayout_4.addWidget(self.feedrate_line, 3, 1, 1, 1)
        self.label_13 = QtGui.QLabel(self.frame_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)
        self.maxpwr_line = QtGui.QLineEdit(self.frame_2)
        self.maxpwr_line.setObjectName("maxpwr_line")
        self.gridLayout_4.addWidget(self.maxpwr_line, 2, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.frame_2)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 3, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addmaterial_button = QtGui.QPushButton(self.frame_2)
        self.addmaterial_button.setObjectName("addmaterial_button")
        self.horizontalLayout.addWidget(self.addmaterial_button)
        self.delmaterial_button = QtGui.QPushButton(self.frame_2)
        self.delmaterial_button.setObjectName("delmaterial_button")
        self.horizontalLayout.addWidget(self.delmaterial_button)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 2, 1, 1)
        self.material_combobox = QtGui.QComboBox(self.frame_2)
        self.material_combobox.setObjectName("material_combobox")
        self.gridLayout_4.addWidget(self.material_combobox, 0, 0, 1, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget = QtGui.QWidget(self.tab_3)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 111, 109))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.yautosize_line = QtGui.QLineEdit(self.gridLayoutWidget)
        self.yautosize_line.setObjectName("yautosize_line")
        self.gridLayout_3.addWidget(self.yautosize_line, 5, 1, 1, 1)
        self.xautosize_line = QtGui.QLineEdit(self.gridLayoutWidget)
        self.xautosize_line.setObjectName("xautosize_line")
        self.gridLayout_3.addWidget(self.xautosize_line, 2, 1, 1, 1)
        self.label_20 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 2, 0, 1, 1)
        self.label_21 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 5, 0, 1, 1)
        self.label_19 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_19.setObjectName("label_19")
        self.gridLayout_3.addWidget(self.label_19, 5, 2, 1, 1)
        self.label_18 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 2, 2, 1, 1)
        self.autoset_radio = QtGui.QRadioButton(self.gridLayoutWidget)
        self.autoset_radio.setObjectName("autoset_radio")
        self.gridLayout_3.addWidget(self.autoset_radio, 0, 0, 1, 3)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.accept_button = QtGui.QPushButton(Form)
        self.accept_button.setObjectName("accept_button")
        self.horizontalLayout_2.addWidget(self.accept_button)
        self.close_button = QtGui.QPushButton(Form)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout_2.addWidget(self.close_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Focus Distance", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Bed Length", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Laser On Cmd.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "Laser Off Cmd.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Bed Width", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Form", "Laser Pwr. Cmd.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Form", "On Idle Delay", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Form", "s", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_33.setText(QtGui.QApplication.translate("Form", "Baud Rate", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrate_button.setText(QtGui.QApplication.translate("Form", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Form", "Machine", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("Form", "Starting Gcode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("Form", "Ending Gcode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Form", "Min Power", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Form", "Feedrate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("Form", "Max Power", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("Form", "mm/s", None, QtGui.QApplication.UnicodeUTF8))
        self.addmaterial_button.setText(QtGui.QApplication.translate("Form", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.delmaterial_button.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "Gcode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("Form", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("Form", "y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("Form", "Pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("Form", "Pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.autoset_radio.setText(QtGui.QApplication.translate("Form", "Auto Set Size", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Form", "Application", None, QtGui.QApplication.UnicodeUTF8))
        self.accept_button.setText(QtGui.QApplication.translate("Form", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.close_button.setText(QtGui.QApplication.translate("Form", "Close", None, QtGui.QApplication.UnicodeUTF8))

