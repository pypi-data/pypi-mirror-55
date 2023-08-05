# -*- coding:UTF-8 -*-
"""封装了cv2模块和numpy模块的一些图像处理的操作，需依赖cv2lib库
"""
import os
import math
import sys

#todo: support linux

try:
    import cv2
except ImportError:
    print('please install cv2 with pip')
    print('pip install opencv-python')
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print('please install cv2 with pip')
    print('pip install numpy')
    sys.exit(1)

LOAD_IMAGE_COLOR = 1 #cv2.CV_LOAD_IMAGE_COLOR
LOAD_IMAGE_GRAYSCALE = 0 #cv2.CV_LOAD_IMAGE_GRAYSCALE

COLOR_BGR2GRAY = 6 #cv2.COLOR_BGR2GRAY
COLOR_RGB2GRAY = 7 #cv2.COLOR_RGB2GRAY

def isNdarray(data):
    return isinstance(data, np.ndarray)

def imread(filePath, flags=LOAD_IMAGE_COLOR):
    if os.path.exists(filePath):
        return cv2.imread(filePath, flags)
    return None

def rotate(src, rotation):
    """围绕中心点旋转
    
    :type src: cvmat格式
    :param src: 图像数据
    :type rotation: int
    :param rotation: 当前旋转角度
    """
    if rotation <= 0:
        return src

    w = src.shape[1]
    h = src.shape[0]
    
    if w>h and (rotation==90 or rotation==270):
        return src
    
    rangle = np.deg2rad(rotation)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) 
    nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) 
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), rotation, 1.0)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0, 2] += rot_move[0]
    rot_mat[1, 2] += rot_move[1]
    return cv2.warpAffine(src, 
                          rot_mat, 
                          (int(math.ceil(nw)), int(math.ceil(nh))), 
                          flags=cv2.INTER_LANCZOS4)

def imdecode(src, flags=LOAD_IMAGE_COLOR):
    i = np.frombuffer(src, dtype='uint8')
    return cv2.imdecode(i, flags)

def imencode(postfix, image, params=[]):
    ok, data = cv2.imencode(postfix, image, params)
    if ok:
        return data
    return None

def imwrite(filePath, src):
    return cv2.imwrite(filePath, src)
        
def cvtColor(src, flags=COLOR_BGR2GRAY):
    return cv2.cvtColor(src, flags)
    
def filter2D(src, ddepth, kernel, *args):
    return cv2.filter2D(src, ddepth, kernel, *args)
    
def roi(src, rc):
    l, t, r, b = rc
    h,w = src.shape[:2]
    if (r-l) >= w:
        return src
    if (b-t) >= h:
        return src

    return src[t:b, l:r].copy()
    # data = cv2.cv.GetSubRect(cv2.cv.fromarray(src), (l, t, r - l, b - t))
    # if data:
    #     return np.asarray(data)
    # return None

def circle(src, pt, radius=5, color=(0, 0, 255), thickness=2):
    cv2.circle(src, pt, radius, color, thickness)
    return src

def rectangle(src, pt1, pt2, color=(0, 0, 255), thickness=2):
    cv2.rectangle(src, pt1, pt2, color, thickness)
    return src

def line(src, ptFrom, ptTo, color=(0, 0, 255), thickness=1):
    cv2.line(src, ptFrom, ptTo, color, thickness)
    return src

def resize(src, newWidth, newHeight):
    newImage = cv2.resize(src, (newWidth, newHeight))
    return newImage

def frombuffer(buff, dtype='uint8'):
    return np.frombuffer(buff, dtype=dtype)

def fromstring(string, dtype=np.uint8):
    return np.frombuffer(string, dtype=dtype)
    
def reshape(src, w, h, channels):
    return np.reshape(src, (h,w,channels))
     
def matchTemplate(image, template, method=cv2.TM_CCOEFF_NORMED):
    return cv2.matchTemplate(image, template, method) 

def minMaxLoc(loc):
    return cv2.minMaxLoc(loc)

def eval2(name):
    return eval(name)

def show(src, title='show'):
    cv2.namedWindow(title,2)
    cv2.imshow(title, src)
    cv2.waitKey()
    cv2.destroyAllWindows()
        
def npwhere(condition, *args):
    return np.where(condition, *args)

def createMsgImage(msg, width, height):
    """创建显示信息的图片"""
    img = np.zeros((height, width, 3), np.uint8)
    img[:, :] = (255, 255, 255)
    top = 20
    left = 20
    lines = msg.split('\n')
    row = len(lines)
    for i in range(row):
        line = lines[i]
        cv2.putText(img, line, (left, top + i * 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

    return imencode('.jpg',img)

if __name__ == '__main__':
    print((eval2('np.ndarray')))
    


