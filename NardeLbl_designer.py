# Form implementation generated from reading ui file 'NardeLbl_designer.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(777, 523)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frme_left_frame = QtWidgets.QFrame(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_left_frame.sizePolicy().hasHeightForWidth())
        self.frme_left_frame.setSizePolicy(sizePolicy)
        self.frme_left_frame.setMaximumSize(QtCore.QSize(150, 16777215))
        self.frme_left_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frme_left_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frme_left_frame.setObjectName("frme_left_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frme_left_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_select_class_file = QtWidgets.QPushButton(parent=self.frme_left_frame)
        self.btn_select_class_file.setObjectName("btn_select_class_file")
        self.verticalLayout_2.addWidget(self.btn_select_class_file)
        self.ledit_class_file = QtWidgets.QLineEdit(parent=self.frme_left_frame)
        self.ledit_class_file.setObjectName("ledit_class_file")
        self.verticalLayout_2.addWidget(self.ledit_class_file)
        self._lbl_class = QtWidgets.QLabel(parent=self.frme_left_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._lbl_class.sizePolicy().hasHeightForWidth())
        self._lbl_class.setSizePolicy(sizePolicy)
        self._lbl_class.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._lbl_class.setObjectName("_lbl_class")
        self.verticalLayout_2.addWidget(self._lbl_class)
        self.cbox_class = QtWidgets.QComboBox(parent=self.frme_left_frame)
        self.cbox_class.setObjectName("cbox_class")
        self.verticalLayout_2.addWidget(self.cbox_class)
        self._lbl_box_color = QtWidgets.QLabel(parent=self.frme_left_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._lbl_box_color.sizePolicy().hasHeightForWidth())
        self._lbl_box_color.setSizePolicy(sizePolicy)
        self._lbl_box_color.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._lbl_box_color.setObjectName("_lbl_box_color")
        self.verticalLayout_2.addWidget(self._lbl_box_color)
        self.cbox_box_color = QtWidgets.QComboBox(parent=self.frme_left_frame)
        self.cbox_box_color.setObjectName("cbox_box_color")
        self.verticalLayout_2.addWidget(self.cbox_box_color)
        self.frme_controls = QtWidgets.QFrame(parent=self.frme_left_frame)
        self.frme_controls.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frme_controls.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frme_controls.setObjectName("frme_controls")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frme_controls)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self._lbl_controls = QtWidgets.QLabel(parent=self.frme_controls)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._lbl_controls.sizePolicy().hasHeightForWidth())
        self._lbl_controls.setSizePolicy(sizePolicy)
        self._lbl_controls.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self._lbl_controls.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._lbl_controls.setObjectName("_lbl_controls")
        self.verticalLayout_3.addWidget(self._lbl_controls)
        self._lbl_controls1 = QtWidgets.QLabel(parent=self.frme_controls)
        self._lbl_controls1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._lbl_controls1.setObjectName("_lbl_controls1")
        self.verticalLayout_3.addWidget(self._lbl_controls1)
        self._lbl_controls2 = QtWidgets.QLabel(parent=self.frme_controls)
        self._lbl_controls2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._lbl_controls2.setObjectName("_lbl_controls2")
        self.verticalLayout_3.addWidget(self._lbl_controls2)
        self.verticalLayout_2.addWidget(self.frme_controls)
        self.lstw_bboxes = QtWidgets.QListWidget(parent=self.frme_left_frame)
        self.lstw_bboxes.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.lstw_bboxes.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.lstw_bboxes.setObjectName("lstw_bboxes")
        self.verticalLayout_2.addWidget(self.lstw_bboxes)
        self.horizontalLayout.addWidget(self.frme_left_frame)
        self.frme_display = QtWidgets.QFrame(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_display.sizePolicy().hasHeightForWidth())
        self.frme_display.setSizePolicy(sizePolicy)
        self.frme_display.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frme_display.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frme_display.setObjectName("frme_display")
        self.gridLayout = QtWidgets.QGridLayout(self.frme_display)
        self.gridLayout.setObjectName("gridLayout")
        self.hsb_display = QtWidgets.QScrollBar(parent=self.frme_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hsb_display.sizePolicy().hasHeightForWidth())
        self.hsb_display.setSizePolicy(sizePolicy)
        self.hsb_display.setMinimumSize(QtCore.QSize(0, 20))
        self.hsb_display.setMaximum(100)
        self.hsb_display.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.hsb_display.setObjectName("hsb_display")
        self.gridLayout.addWidget(self.hsb_display, 2, 0, 1, 1)
        self.vsb_display = QtWidgets.QScrollBar(parent=self.frme_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vsb_display.sizePolicy().hasHeightForWidth())
        self.vsb_display.setSizePolicy(sizePolicy)
        self.vsb_display.setMinimumSize(QtCore.QSize(20, 0))
        self.vsb_display.setMaximum(100)
        self.vsb_display.setTracking(True)
        self.vsb_display.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.vsb_display.setObjectName("vsb_display")
        self.gridLayout.addWidget(self.vsb_display, 1, 1, 1, 1)
        self.lbl_display = QtWidgets.QLabel(parent=self.frme_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_display.sizePolicy().hasHeightForWidth())
        self.lbl_display.setSizePolicy(sizePolicy)
        self.lbl_display.setMouseTracking(True)
        self.lbl_display.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.lbl_display.setText("")
        self.lbl_display.setPixmap(QtGui.QPixmap("../OneDrive/Desktop/dev/T.jpg"))
        self.lbl_display.setScaledContents(False)
        self.lbl_display.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.lbl_display.setObjectName("lbl_display")
        self.gridLayout.addWidget(self.lbl_display, 1, 0, 1, 1)
        self.frme_scale = QtWidgets.QFrame(parent=self.frme_display)
        self.frme_scale.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frme_scale.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frme_scale.setObjectName("frme_scale")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frme_scale)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.hsldr_scale = QtWidgets.QSlider(parent=self.frme_scale)
        self.hsldr_scale.setMinimum(10)
        self.hsldr_scale.setMaximum(500)
        self.hsldr_scale.setProperty("value", 100)
        self.hsldr_scale.setTracking(True)
        self.hsldr_scale.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.hsldr_scale.setObjectName("hsldr_scale")
        self.horizontalLayout_2.addWidget(self.hsldr_scale)
        self.lbl_scale = QtWidgets.QLabel(parent=self.frme_scale)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl_scale.setFont(font)
        self.lbl_scale.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.lbl_scale.setObjectName("lbl_scale")
        self.horizontalLayout_2.addWidget(self.lbl_scale)
        self.gridLayout.addWidget(self.frme_scale, 0, 0, 1, 2)
        self.horizontalLayout.addWidget(self.frme_display)
        self.frme_right_frame = QtWidgets.QFrame(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_right_frame.sizePolicy().hasHeightForWidth())
        self.frme_right_frame.setSizePolicy(sizePolicy)
        self.frme_right_frame.setMaximumSize(QtCore.QSize(150, 16777215))
        self.frme_right_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frme_right_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frme_right_frame.setObjectName("frme_right_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frme_right_frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_save = QtWidgets.QPushButton(parent=self.frme_right_frame)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout_2.addWidget(self.btn_save, 5, 0, 1, 2)
        self.btn_prev_file = QtWidgets.QPushButton(parent=self.frme_right_frame)
        self.btn_prev_file.setObjectName("btn_prev_file")
        self.gridLayout_2.addWidget(self.btn_prev_file, 2, 0, 1, 1)
        self.lbl_resolution = QtWidgets.QLabel(parent=self.frme_right_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_resolution.sizePolicy().hasHeightForWidth())
        self.lbl_resolution.setSizePolicy(sizePolicy)
        self.lbl_resolution.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.lbl_resolution.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_resolution.setObjectName("lbl_resolution")
        self.gridLayout_2.addWidget(self.lbl_resolution, 3, 0, 1, 2)
        self.btn_select_image_dir = QtWidgets.QPushButton(parent=self.frme_right_frame)
        self.btn_select_image_dir.setObjectName("btn_select_image_dir")
        self.gridLayout_2.addWidget(self.btn_select_image_dir, 0, 0, 1, 2)
        self.lstw_files = QtWidgets.QListWidget(parent=self.frme_right_frame)
        self.lstw_files.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.lstw_files.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.lstw_files.setObjectName("lstw_files")
        self.gridLayout_2.addWidget(self.lstw_files, 4, 0, 1, 2)
        self.ledit_image_dir = QtWidgets.QLineEdit(parent=self.frme_right_frame)
        self.ledit_image_dir.setReadOnly(True)
        self.ledit_image_dir.setObjectName("ledit_image_dir")
        self.gridLayout_2.addWidget(self.ledit_image_dir, 1, 0, 1, 2)
        self.btn_next_file = QtWidgets.QPushButton(parent=self.frme_right_frame)
        self.btn_next_file.setObjectName("btn_next_file")
        self.gridLayout_2.addWidget(self.btn_next_file, 2, 1, 1, 1)
        self.ptxt_console = QtWidgets.QPlainTextEdit(parent=self.frme_right_frame)
        self.ptxt_console.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ptxt_console.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ptxt_console.setObjectName("ptxt_console")
        self.gridLayout_2.addWidget(self.ptxt_console, 6, 0, 1, 2)
        self.horizontalLayout.addWidget(self.frme_right_frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_select_class_file.setText(_translate("MainWindow", "Select Class File"))
        self._lbl_class.setText(_translate("MainWindow", "Class"))
        self._lbl_box_color.setText(_translate("MainWindow", "Box Color"))
        self._lbl_controls.setText(_translate("MainWindow", "Controls"))
        self._lbl_controls1.setText(_translate("MainWindow", "Q - Left     W - Up"))
        self._lbl_controls2.setText(_translate("MainWindow", "E - Right     R - Down"))
        self.lbl_scale.setText(_translate("MainWindow", " x1.00"))
        self.btn_save.setText(_translate("MainWindow", "Save Annotations"))
        self.btn_prev_file.setText(_translate("MainWindow", "Prev Img"))
        self.lbl_resolution.setText(_translate("MainWindow", "9999 x 9999"))
        self.btn_select_image_dir.setText(_translate("MainWindow", "Select Image Dir"))
        self.btn_next_file.setText(_translate("MainWindow", "Next Img"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
