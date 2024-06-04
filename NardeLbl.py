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
        self.filesi = 0
        self.classes = []
        self.sample :Sample = None
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
        self.display.sgl_bbox_updated.connect(self.update_sample_displays)
        self.display.sgl_display_in_focus.connect(self.on_display_in_focus)
        self.display.sgl_display_out_focus.connect(self.on_display_out_focus)
        self.ui.cbox_class.currentIndexChanged.connect(self.on_class_changed)
        self.display.sgl_selection_changed.connect(self.on_selection_changed)
        self.ui.btn_next_file.clicked.connect(self.load_next_image)
        self.ui.btn_prev_file.clicked.connect(self.load_prev_image)

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

    @staticmethod
    @_block_signals
    def _setCurrentIndex_no_signal(widget, i :int):
        widget.setCurrentIndex(i)

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

    def load_next_image(self):
        if len(self.files) == 0:
            return
        if self.filesi == len(self.files) - 1:
            return
        self.filesi = self.filesi + 1
        self.save_annotations()
        self.load_image_and_annotations(self.files[self.filesi])

    def load_prev_image(self):
        if len(self.files) == 0:
            return
        if self.filesi == 0:
            return
        self.filesi = self.filesi - 1
        self.save_annotations()
        self.load_image_and_annotations(self.files[self.filesi])

    def load_image_and_annotations(self, imgpath: str):
        img = cv2.imread(imgpath)
        if img is None:
            print(f'Failed to load file {imgpath}')
            return
        h, w, _ = img.shape
        self.sample = Sample(imgpath, w, h)
        self.sample.classes = self.classes
        self.update_sample_displays()
        self.sgl_update_src.emit(img, self.sample)

    def update_sample_displays(self):
        self.ui.lstw_bboxes.clear()
        if self.sample is None:
            return
        lst = self.sample.get_lstw_list()
        if lst is None:
            return
        self.ui.lstw_bboxes.addItems(lst)

    @qtc.pyqtSlot()
    def load_classes_file(self):
        path, _ = qtw.QFileDialog.getOpenFileName(self, 'Select classes file', os.curdir, '*.txt')
        self.classes_file = path
        self.classes = []
        line :str
        with open(path, 'r') as txt:
            lines = txt.readlines()
        for line in lines:
            line = line.strip()
            if line != '' and len(line) != 0:
                self.classes.append(line)
        self.ui.ledit_class_file.setText(path)
        self.ui.cbox_class.clear()
        self.ui.cbox_class.addItems(self.classes)
        if self.sample is not None:
            self.sample.classes = self.classes
        self.update_sample_displays()

    @qtc.pyqtSlot()
    def save_annotations(self):
        if self.sample == None:
            self.xlog('No file loaded.\n', logging.INFO)
            return
        stxt = self.sample.txtpath()
        with open(stxt, 'w') as txt:
            txt.writelines(self.sample.bboxes2lines())
        self.xlog(f'Saved annotations to {stxt}', logging.INFO)

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

    @qtc.pyqtSlot()
    def on_display_in_focus(self):
        self.ui.frme_display.setFrameShape(qtw.QFrame.Shape.Box)

    @qtc.pyqtSlot()
    def on_display_out_focus(self):
        self.ui.frme_display.setFrameShape(qtw.QFrame.Shape.StyledPanel)

    @qtc.pyqtSlot(int)
    def on_class_changed(self, i):
        if self.sample is None:
            return
        self.sample.selected_class = i
        self.update_sample_displays()

    @qtc.pyqtSlot(int)
    def on_selection_changed(self, i):
        self._setCurrentIndex_no_signal(self.ui.cbox_class, i)
        self.update_sample_displays()

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
