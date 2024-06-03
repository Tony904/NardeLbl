import os
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw


class BBox(qtc.QObject):

    def __init__(self, imgw :int, imgh: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.visible = True
        self._selected = False
        self.imgw = imgw
        self.imgh = imgh
        self.lbl :int = 0
        self.left :int = 0
        self.right :int = 0
        self.top :int = 0
        self.bottom :int = 0
        # relative
        self.cx :float = 0
        self.cy :float = 0
        self.w :float = 0
        self.h :float = 0

    @property
    def selected(self):
        return self._selected

    def yolo2rect(self):
        imgw = self.imgw
        imgh = self.imgh
        x = int((self.cx - self.w / 2.) * imgw)
        y = int((self.cy - self.h / 2.) * imgh)
        w = int(self.w * imgw)
        h = int(self.h * imgh)
        self.left = x
        self.top = y
        self.right = x + w
        self.bottom = y + h
        return self.left, self.top, self.right, self.bottom

    def rect2yolo(self):
        imgw = self.imgw
        imgh = self.imgh
        left = self.left
        right = self.right
        top = self.top
        bottom = self.bottom
        w: float = (right - left) / imgw
        h: float = (bottom - top) / imgh
        cx: float = ((right - left) / 2 + left) / imgw
        cy: float = ((bottom - top) / 2 + top) / imgh
        self.w = w
        self. h = h
        self.cx = cx
        self.cy = cy
        return cx, cy, w, h

    def parse_yolo_line(self, line: str):
        s = line.split(' ')
        lbl = int(s[0])
        cx = float(s[1])
        cy = float(s[2])
        w = float(s[3])
        h = float(s[4])
        self.lbl = lbl
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.yolo2rect()

    def yolo_line(self):
        lbl = self.lbl
        cx = self.cx
        cy = self.cy
        w = self.w
        h = self.h
        return f'{lbl} {cx} {cy} {w} {h}'
    
    def update_vertex(self, point, vertexStr):
        if point is None or vertexStr is None:
            return
        x, y = point
        xstr, ystr = vertexStr
        retXstr = xstr
        retYstr = ystr
        # print(f'\nxstr = {xstr} ystr = {ystr}')
        # print(f'left = {self.left} right = {self.right} top = {self.top} bottom = {self.bottom}')
        if xstr is 'left':
            if abs(x - self.right) > 1:
                if x > self.right:
                    self.left = self.right
                    self.right = x
                    retXstr = 'right'
                else:
                    self.left = x
        elif xstr is 'right':
            if abs(x - self.left) > 1:
                if x < self.left:
                    self.right = self.left
                    self.left = x
                    retXstr = 'left'
                else:
                    self.right = x
        if ystr is 'top':
            if abs(y - self.bottom) > 1:
                if y > self.bottom:
                    self.top = self.bottom
                    self.bottom = y
                    retYstr = 'bottom'
                else:
                    self.top = y
        elif ystr is 'bottom':
            if abs(y - self.top) > 1:
                if y < self.top:
                    self.bottom = self.top
                    self.top = y
                    retYstr = 'top'
                else:
                    self.bottom = y
        self.rect2yolo()
        # print(f'left = {self.left} right = {self.right} top = {self.top} bottom = {self.bottom}')
        # print(f'x = {x} y = {y} retXstr = {retXstr} retYstr = {retYstr}')
        return (retXstr, retYstr)
    
    def apply_nudge(self, nudges):
        if nudges is None:
            return
        if nudges[0] != 0:
            print('left')
            print(self.left)
            self.left += nudges[0]
            self.left = max(0, self.left)
            self.left = min(self.imgw, self.left)
            print(self.left)
        elif nudges[1] != 0:
            print('top')
            print(self.top)
            self.top += nudges[1]
            self.top = max(0, self.top)
            self.top = min(self.imgh, self.top)
            print(self.top)
        elif nudges[2] != 0:
            print('right')
            print(self.right)
            self.right += nudges[2]
            self.right = max(0, self.right)
            self.right = min(self.imgw, self.right)
            print(self.right)
        elif nudges[3] != 0:
            print('bottom')
            print(self.bottom)
            self.bottom += nudges[3]
            self.bottom = max(0, self.bottom)
            self.bottom = min(self.imgh, self.bottom)
            print(self.bottom)
        print('\n')
        self.rect2yolo()



class Sample(qtc.QObject):

    def __init__(self, filepath: str, imgw :int, imgh :int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = filepath
        self.bboxes :list[BBox] = None
        self.imgw = imgw
        self.imgh = imgh
        if os.path.exists(filepath):
            self.load_bboxes()
            print(f'Successfully loaded annotations for {filepath}')
        else:
            print(f'{filepath} does not exist.')
        self._selected_bbox :BBox = None
        self.vertex_grab_radius = 10
        self._box_grab_percent :float = 0.5

    @property
    def bbox_selected(self):
        return self._selected_bbox is not None
    
    @property
    def selected_bbox(self) -> BBox:
        return self._selected_bbox
    
    def deselect(self):
        if self.bbox_selected:
            self._selected_bbox._selected = False
            self._selected_bbox = None

    def txtpath(self):
        i = self.path.rfind('.')
        minus_ext = self.path[:i]
        return minus_ext + '.txt'
    
    def justfilename(self):
        i = self.path.rfind('\\')
        return self.path[i+1:]
    
    def bboxes2lines(self):
        lines = []
        for bbox in self.bboxes:
            lines.append(bbox.yolo_line() + '\n')
        return lines

    def load_bboxes(self):
        lines = []
        self.bboxes = []
        with open(self.txtpath(), 'r') as txt:
            lines = txt.readlines()
        for line in lines:
            if line != '' and len(line) != 0:
                bbox = BBox(self.imgw, self.imgh)
                bbox.parse_yolo_line(line)
                self.bboxes.append(bbox)

    
    def get_lstw_list(self):
        lst = []
        for b in self.bboxes:
            s = f'{b.lbl} {b.left} {b.right} {b.top} {b.bottom}'
            lst.append(s)
        return lst
    
    def set_selected(self, bbox :BBox):
        if bbox is self._selected_bbox:
            return
        if self.bbox_selected:
            self._selected_bbox._selected = False
        self._selected_bbox = bbox
        bbox._selected = True
