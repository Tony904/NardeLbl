import copy
import logging
import cv2
import numpy as np
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
import time
from sample import Sample, BBox


class Display(qtc.QObject):
    sgl_did_display = qtc.pyqtSignal(qtg.QPixmap)
    sgl_do_display = qtc.pyqtSignal()
    sgl_msg = qtc.pyqtSignal(str)

    def __init__(self, lbl: qtw.QLabel, slider: qtw.QSlider, hzsb: qtw.QScrollBar, vtsb: qtw.QScrollBar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xlog_enabled = True
        self.xlog_level = logging.getLogger().getEffectiveLevel()
        self.xlog_quiet = False

        self.ndarray_dtype = np.uint8
        self.sample :Sample
        self.bbox :BBox
        self.src: np.ndarray = np.zeros((100, 100, 3), self.ndarray_dtype)
        self.lbl :qtw.QLabel = lbl
        self.lbl.mousePressEvent = self._mousePressEvent
        self.lbl.mouseMoveEvent = self._mouseMoveEvent
        self.click_coords = None  # (mouse x, mouse y)
        self.cursorX = None
        self.cursorY = None
        self.selected_box = None
        self.editrect = EditRect()
        self.states = States()
        self.hzsb :qtw.QScrollBar = hzsb
        self.vtsb :qtw.QScrollBar = vtsb
        self.slider :qtw.QSlider = slider
        slider.setValue(100)
        self.transform: tuple[int, int, int, int, int, int] = (100, 100, 0, 100, 0, 100)
        self.redraw = True
        self.sgl_do_display.connect(self._do_display, type=qtc.Qt.ConnectionType.QueuedConnection)
        self.sgl_did_display.connect(self._do_display, type=qtc.Qt.ConnectionType.QueuedConnection)

    def _mousePressEvent(self, event :qtg.QMouseEvent):
        if event.button() == qtc.Qt.MouseButton.LeftButton:
            self.click_coords = (event.pos().x(), event.pos().y())
            self.xlog(f'click_coords set to ({event.pos().x()}, {event.pos().y()})')
            return
        if event.button() == qtc.Qt.MouseButton.RightButton:
            self.click_coords = None
            self.xlog(f'click_coords set to None.')
            return

    def _mouseMoveEvent(self, event :qtg.QMouseEvent):
        self.cursorX = event.pos().x()
        self.cursorY = event.pos().y()

    def _do_display(self):
        transform = self._calculate_transform_and_set_scrollbars()
        if not transform == self.transform:
            self.redraw = True
            self.transform = transform
        img = self._transform_src_image(transform)
        if self.redraw:
            img = self._draw_boxes(img, transform)
        qimg = qtg.QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qtg.QImage.Format.Format_BGR888)
        qpix = qtg.QPixmap.fromImage(qimg)
        # self.xlog('Did display.')
        self.sgl_did_display.emit(qpix)

    def _calculate_transform_and_set_scrollbars(self) -> tuple[int, int, int, int, int, int]:
        h, w, _ = self.src.shape
        scale: float = self.slider.value() / 100.0
        scaled_h: int = int(h * scale)
        scaled_w: int = int(w * scale)
        canvas_h: int = self.lbl.height()
        canvas_w: int = self.lbl.width()
        self.vtsb.setMaximum(max(0, scaled_h - canvas_h))
        self.hzsb.setMaximum(max(0, scaled_w - canvas_w))
        if self.vtsb.value() > self.vtsb.maximum():
            self.vtsb.setValue(self.vtsb.maximum())
        if self.hzsb.value() > self.hzsb.maximum():
            self.hzsb.setValue(self.hzsb.maximum())
        y1: int = self.vtsb.value()
        x1: int = self.hzsb.value()
        y2: int = y1 + min(canvas_h, scaled_h)
        x2: int = x1 + min(canvas_w, scaled_w)
        return scaled_h, scaled_w, y1, y2, x1, x2

    def _transform_src_image(self, transform: tuple[int, int, int, int, int, int]) -> np.ndarray:
        scaled_h, scaled_w, y1, y2, x1, x2 = transform
        img = cv2.resize(self.src, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
        return img[y1:y2, x1:x2].copy()

    def _draw_boxes(self, img: np.ndarray, transform: tuple[int, int, int, int, int, int]) -> np.ndarray:
        precrop_h, precrop_w, y1, y2, x1, x2 = transform
        img_h, img_w, _ = img.shape
        # x: float; y: float; w: float; h: float
        color = (0, 0, 255)  # red
        left_clicked = self.click_coords is not None
        box_selected = False
        for bbox in self.sample.bboxes:
            if not bbox.visible:
                continue
            x = bbox.cx * precrop_w
            y = bbox.cy * precrop_h
            w = bbox.w * precrop_w
            h = bbox.h * precrop_h
            left = max(0, int(x - w / 2.) - x1)
            top = max(0, int(y - h / 2.) - y1)
            right = min(img_w, int(x + w / 2.) - x1)
            bottom = min(img_h, int(y + h / 2.) - y1)
            if left >= right or top >= bottom:
                continue
            rect_thickness = 1
            if left_clicked:
                if left < self.click_coords[0]:
                    if right > self.click_coords[0]:
                        if top < self.click_coords[1]:
                            if bottom > self.click_coords[1]:
                                box_selected = True
                                rect_thickness = 3
                                self.selected_box = bbox
            cv2.rectangle(img, (left, top), (right, bottom), color, rect_thickness)
        if box_selected:
            self.states.box_selected = True
            self.xlog(f'Box selected: {self.selected_box.lbl} (mouse x, y = {self.click_coords[0]}, {self.click_coords[1]})')
        if left_clicked and not box_selected:
            self.states.box_selected = False
        else:
            self.click_coords = None
        return img
    
    @qtc.pyqtSlot(np.ndarray, Sample)
    def set_src_and_sample(self, src :np.ndarray, sample :Sample):
        self.src = src
        self.sample = sample
        self._do_display()

    def xlog(self, msg: str, level: int = logging.DEBUG):
        if level > logging.DEBUG:
            self.sgl_msg.emit(msg)
        if level < self.xlog_level:
            return
        if not self.xlog_quiet:
            print(msg)
        if not self.xlog_enabled:
            return
        logging.log(level, msg)


class EditRect:

    def __init__(self):
        self.left = None
        self.right = None
        self.bottom = None
        self.top = None


class States:

    def __init__(self):
        self._box_selected = 0
        self._hovering_over_box = 0
        self._hovering_over_vertex = 0
        self._vertex_selected = 0
        self._dragging_vertex = 0
        self._dragging_box = 0
        self._editing_box = 0

    @property
    def editing_box(self):
        return self._editing_box
    
    @editing_box.setter
    def editing_box(self, x):
        self._editing_box = x
        if not x:
            self._box_selected = False
            self._vertex_selected = False
            self._dragging_box = False
            self._dragging_vertex = False

    @property
    def box_selected(self):
        return self._box_selected
    
    @box_selected.setter
    def box_selected(self, x):
        self._box_selected = x
        self.editing_box = x

    @property
    def hovering_over_box(self):
        return self._hovering_over_box
    
    @hovering_over_box.setter
    def hovering_over_box(self, x):
        self._hovering_over_box = x

    @property
    def hovering_over_vertex(self):
        return self._hovering_over_vertex
    
    @hovering_over_vertex.setter
    def hovering_over_vertex(self, x):
        self._hovering_over_vertex = x

    @property
    def vertex_selected(self):
        return self._vertex_selected
    
    @vertex_selected.setter
    def vertex_selected(self, x):
        self._vertex_selected = x
        if x:
            self._editing_box = True

    @property
    def dragging_vertex(self):
        return self._dragging_vertex
    
    @dragging_vertex.setter
    def dragging_vertex(self, x):
        self._dragging_vertex = x
        if x:
            self._editing_box = True
    
    @property
    def dragging_box(self):
        return self._dragging_box
    
    @dragging_box.setter
    def dragging_box(self, x):
        self._dragging_box = x
        if x:
            self._editing_box = True
