import glob
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
import cv2
import numpy as np
from NardeLbl_designer import Ui_MainWindow as UiMain
import functools
import logging
import sys
from display import *
import os
from sample import *


logging.basicConfig(filename='nardelbl.log', level=logging.DEBUG)


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.mw = MainWindow()
        self.mw.show()


class MainWindow(qtw.QMainWindow):
    sgl_update_src = qtc.pyqtSignal(np.ndarray, Sample)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xlog_enabled = True
        self.xlog_level = logging.getLogger().getEffectiveLevel()
        self.xlog_quiet = False
        self.ui = UiMain()
        self.ui.setupUi(self)

        img: np.ndarray = np.zeros((100, 100, 3),  np.uint8)
        qimg = qtg.QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qtg.QImage.Format.Format_RGB888)
        qpix = qtg.QPixmap.fromImage(qimg)
        self.ui.lbl_display.setPixmap(qpix)
        self.files = []
        self.sample :Sample
        self.selected_bbox :BBox
        self.classes = []
        self.selected_class = ''
        self.imgdir = ''
        self.colors = ('red', 'green', 'blue')
        self.selected_color = self.colors[0]
        self.ui.cbox_box_color.addItems(self.colors)

        lbl = self.ui.lbl_display
        slider = self.ui.hsldr_scale
        hzsb = self.ui.hsb_display
        vtsb = self.ui.vsb_display
        self.display = Display(lbl, slider, hzsb, vtsb)
        self.display_qthread = qtc.QThread()
        self.display.moveToThread(self.display_qthread)
        self.display_qthread.start()
        self.connect_signals()

    def connect_signals(self):
        self.ui.hsldr_scale.valueChanged.connect(self.on_zoom_slider_value_changed)
        self.display.sgl_msg.connect(self.on_sgl_msg)
        self.ui.btn_select_image_dir.clicked.connect(self.load_image_dir)
        self.ui.btn_select_class_file.clicked.connect(self.load_classes_file)
        self.ui.btn_save.clicked.connect(self.save_annotations)
        self.sgl_update_src.connect(self.display.set_src_and_sample)
        self.display.sgl_did_display.connect(self.update_display_pixmap)

    def _block_signals(func):
        @functools.wraps(func)
        def wrapper(*args):
            args[0].blockSignals(True)
            func(*args)
            args[0].blockSignals(False)
        return wrapper

    @staticmethod
    @_block_signals
    def _setValue_no_signal(widget, value):
        widget.setValue(value)

    @staticmethod
    @_block_signals
    def _setChecked_no_signal(widget, state: int):
        widget.setChecked(state)

    @staticmethod
    @_block_signals
    def _setText_no_signal(widget, text):
        widget.setText(str(text))

    # --------------------------------------------------------------
    # Buttons
    # --------------------------------------------------------------
    @qtc.pyqtSlot()
    def load_image_dir(self):
        qfd = qtw.QFileDialog()
        options = qtw.QFileDialog.options(qfd)
        options |= qtw.QFileDialog.Option.ShowDirsOnly
        directory = qfd.getExistingDirectory(self, "Select Directory", options=options)
        if directory:
            print("Selected Directory:", directory)
        self.imgdir = directory
        self.ui.ledit_image_dir.setText(directory)
        files :list[str] = []
        extensions = ['.png', '.bmp', '.jpeg', '.jpg']
        for ext in extensions:
            files.extend(glob.glob(os.path.join(directory, f'*{ext}')))
        for file in files:
            self.files.append(file)
            i = file.rfind('\\')
            filename = file[i+1:]
            self.ui.lstw_files.addItem(filename)
        self.load_image_and_annotations(files[0])

    def load_image_and_annotations(self, imgpath: str):
        img = cv2.imread(imgpath)
        h, w, _ = img.shape
        self.sample = Sample(imgpath, w, h)
        self.ui.lstw_bboxes.clear()
        self.ui.lstw_bboxes.addItems(self.sample.get_lstw_list())
        self.sgl_update_src.emit(img, self.sample)

    @qtc.pyqtSlot()
    def load_classes_file(self):
        path, _ = qtw.QFileDialog.getOpenFileName(self, 'Select classes file', os.curdir, '*.txt')
        self.classes_file = path
        self.classes = []
        with open(path, 'r') as txt:
            lines = txt.readlines()
        for line in lines:
            if line != '' and len(line) != 0:
                self.classes.append(line)
        self.ui.cbox_class.clear()
        self.ui.cbox_class.addItems(self.classes)

    @qtc.pyqtSlot()
    def save_annotations(self):
        if self.sample == 0:
            self.xlog('No file loaded.\n', logging.INFO)
            return
        txt = self.sample.path
        with open(txt, 'w') as txt:
            txt.writelines(self.sample.bboxes2lines())
        self.xlog(f'Saved annotations to {txt}', logging.INFO)

    # --------------------------------------------------------------
    # Display Loop
    # --------------------------------------------------------------
    @qtc.pyqtSlot(qtg.QPixmap)
    def update_display_pixmap(self, pixmap: qtg.QPixmap):
        self.ui.lbl_display.setPixmap(pixmap)

    # --------------------------------------------------------------
    # Event callbacks
    # --------------------------------------------------------------

    # --- UI -------------------------------------------------------
    @qtc.pyqtSlot(int)
    def on_zoom_slider_value_changed(self, v: int):
        zoom = float(v / 100.0)
        self.ui.lbl_scale.setText(f'x{zoom:.2f}')

    # --------------------------------------------------------------
    # Logging & Console
    # --------------------------------------------------------------
    def console(self, s):
        self.ui.ptxt_console.appendPlainText(f'{s}')

    @qtc.pyqtSlot(str)
    def on_sgl_msg(self, msg):
        self.console(msg)

    def xlog(self, msg: str, level: int = logging.DEBUG):
        if level > logging.DEBUG:
            self.console(msg)
        if level < self.xlog_level:
            return
        if not self.xlog_quiet:
            print(msg)
        if not self.xlog_enabled:
            return
        logging.log(level, msg)


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec())
