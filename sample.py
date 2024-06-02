import os


class BBox:

    def __init__(self, imgw :int, imgh: int):
        self.visible = True
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


class Sample:

    def __init__(self, filepath: str, imgw :int, imgh :int):
        self.path = filepath
        self.bboxes :list[BBox] = None
        self.imgw = imgw
        self.imgh = imgh
        if os.path.exists(filepath):
            self.load_bboxes()
            print(f'Successfully loaded annotations for {filepath}')
        else:
            print(f'{filepath} does not exist.')

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
            lines.append(bbox.yolo_line())

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