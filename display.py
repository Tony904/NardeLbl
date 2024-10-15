import logging
import cv2
import numpy as np
import math
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
import time
from sample import Sample, BBox


class Display(qtc.QObject):
    sgl_did_display = qtc.pyqtSignal(qtg.QPixmap)
    sgl_do_display = qtc.pyqtSignal()
    sgl_msg = qtc.pyqtSignal(str)
    sgl_bbox_updated = qtc.pyqtSignal()
    sgl_display_in_focus = qtc.pyqtSignal()
    sgl_display_out_focus = qtc.pyqtSignal()
    sgl_selection_changed = qtc.pyqtSignal(int)

    def __init__(self, lbl: qtw.QLabel, slider: qtw.QSlider, hzsb: qtw.QScrollBar, vtsb: qtw.QScrollBar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xlog_enabled = True
        self.xlog_level = logging.getLogger().getEffectiveLevel()
        self.xlog_quiet = False

        self.ndarray_dtype = np.uint8
        self.sample :Sample
        self.src: np.ndarray = np.zeros((100, 100, 3), self.ndarray_dtype)
        self.lbl :qtw.QLabel = lbl
        self.lbl.mousePressEvent = self._mousePressEvent
        self.lbl.mouseMoveEvent = self._mouseMoveEvent
        self.lbl.wheelEvent = self._wheelEvent
        self.lbl.keyPressEvent = self._keyPressEvent
        self.lbl.focusInEvent = self._focusInEvent
        self.lbl.focusOutEvent = self._focusOutEvent
        self.lbl.mouseReleaseEvent = self._mouseReleaseEvent
        self.click_coords = None  # (mouse x, mouse y)
        self.right_clicked = False
        self.right_click_held = False
        self.cursorX = 0
        self.cursorY = 0
        self.cursorXdelta = 0
        self.cursorYdelta = 0
        self.wheeldelta = 0
        self.vsbVal = 0
        self.hsbVal = 0
        self.scale = 1
        self.color = (0, 0, 255)  # red
        self.vertexStr = None
        self.keyPressed = False
        self.keyNudge = [0, 0, 0, 0]  # left, top, right, bottom
        self.anchor = None
        self.copy_box = False
        self.time = time.time()
        self.copy_box_cooldown = 1
        self.delete_selected = False
        self.states = States()
        self.hzsb :qtw.QScrollBar = hzsb
        self.vtsb :qtw.QScrollBar = vtsb
        self.slider :qtw.QSlider = slider
        slider.setValue(100)
        self.transform: tuple[int, int, int, int, int, int, float] = (100, 100, 0, 100, 0, 100, 1.)
        self.display_in_focus = False
        self.sgl_do_display.connect(self._do_display, type=qtc.Qt.ConnectionType.QueuedConnection)

    def _wheelEvent(self, event: qtg.QWheelEvent):
        delta = event.angleDelta().y()
        delta = delta / abs(delta)
        self.wheeldelta = delta

    def _focusInEvent(self, event :qtg.QFocusEvent):
        self.sgl_display_in_focus.emit()

    def _focusOutEvent(self, event :qtg.QFocusEvent):
        self.right_click_held = False
        self.sgl_display_out_focus.emit()

    def _mousePressEvent(self, event :qtg.QMouseEvent):
        if event.button() == qtc.Qt.MouseButton.LeftButton:
            self.click_coords = (event.pos().x(), event.pos().y())
            self.right_clicked = False
            self.xlog(f'click_coords set to ({event.pos().x()}, {event.pos().y()})')
            return
        elif event.button() == qtc.Qt.MouseButton.RightButton:
            self.click_coords = None
            self.right_clicked = True
            self.right_click_held = True
            self.xlog(f'click_coords set to None.')
            return
        
    def _mouseReleaseEvent(self, event :qtg.QMouseEvent):
        if event.button() == qtc.Qt.MouseButton.RightButton:
            print('Right mouse released.')
            self.right_click_held = False
            self.cursorXdelta = 0
            self.cursorYdelta = 0

    def _mouseMoveEvent(self, event :qtg.QMouseEvent):
        x = event.pos().x()
        y = event.pos().y()
        if self.right_click_held:
            self.cursorXdelta = x - self.cursorX
            self.cursorYdelta = y - self.cursorY
        self.cursorX = x
        self.cursorY = y
        

    def _keyPressEvent(self, event :qtg.QKeyEvent):
        print(f'Key pressed: {event.key()}')
        if event.key() == qtc.Qt.Key.Key_T:
            t = time.time()
            if t - self.time > self.copy_box_cooldown:
                self.copy_box = True
                self.time = t
            else:
                print(f'Box creation on cooldown. {t - self.time}')
        elif event.key() == qtc.Qt.Key.Key_Delete:
                self.delete_selected = True
        elif event.key() == qtc.Qt.Key.Key_Q:  # Outward Left
            self.keyNudge[0] = -1
        elif event.key() == qtc.Qt.Key.Key_W:  # Outward Top
            self.keyNudge[1] = -1
        elif event.key() == qtc.Qt.Key.Key_E:  # Outward Right
            self.keyNudge[2] = 1
        elif event.key() == qtc.Qt.Key.Key_R:  # Outward Bottom
            self.keyNudge[3] = 1
        elif event.key() == qtc.Qt.Key.Key_A:  # Inward Left
            self.keyNudge[0] = 1
        elif event.key() == qtc.Qt.Key.Key_S:  # Inward Top
            self.keyNudge[1] = 1
        elif event.key() == qtc.Qt.Key.Key_D:  # Inward Right
            self.keyNudge[2] = -1
        elif event.key() == qtc.Qt.Key.Key_F:  # Inward Bottom
            self.keyNudge[3] = -1
        self.keyPressed = True

    def _do_display(self):
        if self.src is None:
            self.sgl_do_display.emit()
            return
        src = self.src.copy()
        transform = self._calculate_transform_and_set_scrollbars(src)
        self.transform = transform
        img = self._transform_src_image(src, transform)
        img = self._draw_boxes(img, transform)
        qimg = qtg.QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qtg.QImage.Format.Format_BGR888)
        qpix = qtg.QPixmap.fromImage(qimg)
        self.sgl_did_display.emit(qpix)
        self.sgl_do_display.emit()

    def _draw_boxes(self, img: np.ndarray, transform: tuple[int, int, int, int, int, int, float]) -> np.ndarray:
        precrop_h, precrop_w, y1, y2, x1, x2, scale = transform
        img_h, img_w, _ = img.shape
        color = self.color
        curX = self.cursorX
        curY = self.cursorY
        adjustedCurX = round((curX + x1) / scale)
        adjustedCurY = round((curY + y1) / scale)
        vertex = None
        vertexStr = None
        changed = False
        left_clicked = self.click_coords is not None
        if left_clicked:
            clickX = self.click_coords[0]
            clickY = self.click_coords[1]
            adjustedClickX = round((clickX + x1) / scale)
            adjustedClickY = round((clickY + y1) / scale)
        if self.right_clicked:
            self.sample.deselect()
            self.states.dragging_box = False
            self.states.dragging_vertex = False
            self.states.box_selected = False
            self.lbl.setCursor(qtc.Qt.CursorShape.ArrowCursor)
        if self.delete_selected:
            self.sample.delete_selected()
            self.delete_selected = False
            self.lbl.setCursor(qtc.Qt.CursorShape.ArrowCursor)
        if self.copy_box:
            if not self.sample.bbox_selected:
                cx = adjustedCurX / self.sample.imgw
                cy = adjustedCurY / self.sample.imgh
                self.sample.add_bbox(cx, cy)
                changed = True
                self.xlog('Created new box.', logging.INFO)
            else:
                self.xlog('Cannot create a new box while one is selected.', logging.INFO)
            self.copy_box = False
        for bbox in self.sample.bboxes:
            box_clicked = False
            if not bbox.visible:
                continue
            x :float = bbox.cx * precrop_w
            y :float = bbox.cy * precrop_h
            w :float = bbox.w * precrop_w
            h :float = bbox.h * precrop_h
            left = max(0, int(x - w / 2.) - x1)
            top = max(0, int(y - h / 2.) - y1)
            right = min(img_w, int(x + w / 2.) - x1)
            bottom = min(img_h, int(y + h / 2.) - y1)
            if (left > right or top > bottom):
                continue
            rect_thickness = 1
            if bbox.selected:
                if self.states.dragging_box:
                    if left_clicked:
                        self.states.dragging_box = False
                        x_shift = adjustedClickX - self.anchor[0] - bbox.left
                        y_shift = adjustedClickY - self.anchor[1] - bbox.top
                        self.anchor = None
                        changed = True
                    else:
                        x_shift = adjustedCurX - self.anchor[0] - bbox.left
                        y_shift = adjustedCurY - self.anchor[1] - bbox.top
                    if bbox.left + x_shift < 0:
                        x_shift = -bbox.left
                    if bbox.right + x_shift > self.sample.imgw:
                        x_shift = self.sample.imgw - bbox.right
                    if bbox.top + y_shift < 0:
                        y_shift = -bbox.top
                    if bbox.bottom + y_shift > self.sample.imgh:
                        y_shift = self.sample.imgh - bbox.bottom
                    bbox.update_box([x_shift, y_shift, x_shift, y_shift])
                if self.states.dragging_vertex:
                    if left_clicked:
                        self.states.dragging_vertex = False
                        x_update = adjustedClickX
                        y_update = adjustedClickY
                        changed = True
                    else:
                        x_update = adjustedCurX
                        y_update = adjustedCurY
                    self.vertexStr = bbox.update_vertex((x_update, y_update), self.vertexStr)
                elif not self.states.dragging_vertex and not self.states.dragging_box:
                    if left_clicked:
                        if self.states.hovering_over_box:
                            self.anchor = (adjustedClickX - bbox.left, adjustedClickY - bbox.top)
                            self.states.dragging_box = True
                        else:
                            vertex, vertexStr = self.check_vertexes(self.click_coords, left, right, top, bottom)
                            if vertex is not None:
                                self.vertexStr = vertexStr
                                self.states.dragging_vertex = True
                    else:  # bbox selected but not dragging anything
                        if self.keyPressed:
                            bbox.update_box(self.keyNudge)
                            self.keyNudge = [0, 0, 0, 0]
                            self.keyPressed = False
                            changed = True
                        elif self.in_box_grab_zone((curX, curY), left, right, top, bottom):
                            self.states.hovering_over_box = True
                            self.lbl.setCursor(qtc.Qt.CursorShape.OpenHandCursor)
                        else:
                            self.states.hovering_over_box = False
                            self.lbl.setCursor(qtc.Qt.CursorShape.ArrowCursor)
                            vertex, _ = self.check_vertexes((curX, curY), left, right, top, bottom)
                            if vertex is not None:
                                self.states.hovering_over_vertex = True
                                cv2.circle(img, vertex, 6, color, 6)
                            else:
                                self.states.hovering_over_vertex = False
            elif not self.sample.bbox_selected:
                if left_clicked:
                    if left < clickX:
                        if right > clickX:
                            if top < clickY:
                                if bottom > clickY:
                                    box_clicked = True
                                    self.sample.set_selected(bbox)
                                    self.sgl_selection_changed.emit(bbox.lbl)
            if bbox.selected:
                color = (0, 255, 0)  # green
            else:
                color = self.color
            cv2.rectangle(img, (left, top), (right, bottom), color, rect_thickness)
            if box_clicked:
                self.xlog(f'Box selected: {self.sample.selected_bbox.lbl} (mouse x, y = {clickX}, {clickY})')
        if changed:
            self.sgl_bbox_updated.emit()
        self.right_clicked = False
        self.click_coords = None
        return img
    
    def check_vertexes(self, point, left, right, top, bottom):
        if point is None:
            return None, 0
        x = point[0]
        y = point[1]
        r = self.sample.vertex_grab_radius
        vX = None
        vY = None
        vXstr = None
        vYstr = None
        if x < left - r:
            return None, None
        if x > right + r:
            return None, None
        if y < top - r:
            return None, None
        if y > bottom + r:
            return None, None
        if x > left + r:
            if x < right - r:
                return None, None
        if y > top + r:
            if y < bottom - r:
                return None, None
        if x <= left + r:
            vX = left
            vXstr = 'left'
        else:
            vX = right
            vXstr = 'right'
        if y <= top + r:
            vY = top
            vYstr = 'top'
        else:
            vY = bottom
            vYstr = 'bottom'
        return (vX, vY), (vXstr, vYstr)
    
    def in_box_grab_zone(self, point, left, right, top, bottom):
        if point is None:
            return False
        x = point[0]
        y = point[1]
        grabw = self.sample.box_grab_percent * (right - left)
        grabh = self.sample.box_grab_percent * (bottom - top)
        grabLeft = left + grabw / 2
        grabTop = top + grabh / 2
        grabRight = right - grabw / 2
        grabBottom = bottom - grabh / 2
        if x < grabLeft:
            return False
        if x > grabRight:
            return False
        if y < grabTop:
            return False
        if y > grabBottom:
            return False
        return True
    
    def _calculate_transform_and_set_scrollbars(self, src: np.ndarray) -> tuple[int, int, int, int, int, int, float]:
        h, w, _ = src.shape
        wheeldelta = self.wheeldelta
        self.wheeldelta = 0
        wheelMag = 25
        if self.scale < 1.25:
            wheelMag = 5
        self.slider.setValue(int(self.slider.value() + wheeldelta * wheelMag))
        scale: float = self.slider.value() / 100.0
        scaled_h: int = int(h * scale)
        scaled_w: int = int(w * scale)
        canvas_h: int = self.lbl.height()
        canvas_w: int = self.lbl.width()
        scale_changed = self.scale != scale
        if scale_changed:
            hsbRatio = self.hzsb.value() / max(1, self.hzsb.maximum())
            vsbRatio = self.vtsb.value() / max(1, self.vtsb.maximum())
        if self.right_click_held:
            self.vtsb.setValue(self.vtsb.value() - self.cursorYdelta)
            self.hzsb.setValue(self.hzsb.value() - self.cursorXdelta)
            self.cursorXdelta = 0
            self.cursorYdelta = 0
        newVtMax = max(0, scaled_h - canvas_h)
        newHzMax = max(0, scaled_w - canvas_w)
        if self.vtsb.value() > newVtMax:
            self.vtsb.setValue(newVtMax)
            self.vtsb.setMaximum(newVtMax)
        elif scale_changed:
            self.vtsb.setMaximum(newVtMax)
            self.vtsb.setValue(round(newVtMax * vsbRatio))
        if self.hzsb.value() > newHzMax:
            self.hzsb.setValue(newHzMax)
            self.hzsb.setMaximum(newHzMax)
        elif scale_changed:
            self.hzsb.setMaximum(newHzMax)
            self.hzsb.setValue(round(newHzMax * hsbRatio))
        self.scale = scale
        y1: int = self.vtsb.value()
        x1: int = self.hzsb.value()
        y2: int = y1 + min(canvas_h, scaled_h)
        x2: int = x1 + min(canvas_w, scaled_w)
        return scaled_h, scaled_w, y1, y2, x1, x2, scale

    def _transform_src_image(self, src: np.ndarray, transform: tuple[int, int, int, int, int, int, float]) -> np.ndarray:
        scaled_h, scaled_w, y1, y2, x1, x2, scale = transform
        img = cv2.resize(src, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
        return img[y1:y2, x1:x2].copy()
    
    @qtc.pyqtSlot(np.ndarray, Sample)
    def set_src_and_sample(self, src :np.ndarray, sample :Sample):
        self.src = src.copy()
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


class States:

    def __init__(self):
        self._box_selected = 0
        self._vertex_selected = 0
        self._hovering_over_box = 0
        self._hovering_over_vertex = 0
        self._dragging_box = 0
        self._dragging_vertex = 0

    @property
    def box_selected(self):
        return self._box_selected
    
    @box_selected.setter
    def box_selected(self, x):
        self._box_selected = x

    @property
    def vertex_selected(self):
        return self._vertex_selected
    
    @vertex_selected.setter
    def vertex_selected(self, x):
        self._vertex_selected = x
        if x:
            self._box_selected = True
            self._hovering_over_vertex = False
        
    @property
    def hovering_over_box(self):
        return self._hovering_over_box
    
    @hovering_over_box.setter
    def hovering_over_box(self, x):
        if x:
            if self._hovering_over_vertex:
                return
            if self._dragging_box:
                return
            if self._dragging_vertex:
                return
        self._hovering_over_box = x

    @property
    def hovering_over_vertex(self):
        return self._hovering_over_vertex
    
    @hovering_over_vertex.setter
    def hovering_over_vertex(self, x):
        self._hovering_over_vertex = x
        if x:
            self._hovering_over_box = False

    @property
    def dragging_vertex(self):
        return self._dragging_vertex
    
    @dragging_vertex.setter
    def dragging_vertex(self, x):
        if not self._dragging_vertex and x:
            print('Dragging vertex.')
        if self._dragging_vertex and not x:
            print('Stopped dragging vertex.')
        self._dragging_vertex = x
        if x:
            self._hovering_over_vertex = False
            self._dragging_box = False
    
    @property
    def dragging_box(self):
        return self._dragging_box
    
    @dragging_box.setter
    def dragging_box(self, x):
        self._dragging_box = x
        if x:
            self._hovering_over_box = False
            self._dragging_vertex = False
