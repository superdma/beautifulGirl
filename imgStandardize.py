import cv2
import os
import numpy as np
from PIL import Image
import shutil
import sys

#批量改变图片的格式和尺寸
image_size_width = 640
image_size_height = 580


#等待转换的图片存放地址
source_path=os.getcwd()+"\\img\\"
#转换后的图片格式
types='png'
#转换过格式的图片存放地址
target_path=os.getcwd()+"\\pngImg\\"
#转换过格式和尺寸的图片存放地址
final_path=os.getcwd()+"\\finalImg\\"

#如果没有转换后的图片存放文件夹，就创建对应的文件夹
if not os.path.exists(target_path):
    os.makedirs(target_path)
if not os.path.exists(final_path):
    os.makedirs(final_path)

#转变图片格式的函数
def changepng(source_path,types):
    files = []
    image_list=os.listdir(source_path)
    #print(image_list)
    files = [os.path.join(source_path, _) for _ in image_list]
    for index,jpg in enumerate(files):
        if index > 1000:
            break
        try:
            sys.stdout.write('\r>>Converting image %d/100 ' % (index))
            sys.stdout.flush()
            im = Image.open(jpg)
            png = os.path.splitext(jpg)[0] + "." + types
            im.save(png)
            #如果同名文件已经存在，则删除
            (filepath, tempfilename) = os.path.split(png)
            if os.path.exists(target_path + tempfilename):
                os.remove(target_path + tempfilename)
            shutil.move(png,target_path)
            #os.remove(png)
        except IOError as e:
            print('could not read:',jpg)
            print('error:',e)
            print('skip it\n')
    sys.stdout.write('Convert Over!\n')
    sys.stdout.flush()


#按照指定图像大小调整尺寸
def resize_image(image, height, width):
     top, bottom, left, right = (0, 0, 0, 0)

     #获取图像尺寸
     h, w, _ = image.shape

     #对于长宽不相等的图片，找到最长的一边
     longest_edge = max(h, w)

     #计算短边需要增加多上像素宽度使其与长边等长
     if h < longest_edge:
         dh = longest_edge - h
         top = dh // 2
         bottom = dh - top
     elif w < longest_edge:
         dw = longest_edge - w
         left = dw // 2
         right = dw - left
     else:
         pass

     #RGB颜色
     BLACK = [255,255,255]

     #给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
     constant = cv2.copyMakeBorder(image, top , bottom, left, right, cv2.BORDER_CONSTANT, value = BLACK)

     #调整图像大小并返回
     return cv2.resize(constant, (height, width))

#转化图片尺寸的函数

def changesize(target_path):
    image_lists = os.listdir(target_path)
    i = 0
    for file in image_lists:
        i=i+1
        print(os.getcwd()+"/"+file)
        split=os.path.splitext(file)
        filename,type=split
        image_file = target_path+file
        image_source = cv2.imdecode(np.fromfile(image_file,dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        image = resize_image(image_source, image_size_width, image_size_height)
        cv2.imencode('.png',image)[1].tofile(final_path+file)



changepng(source_path,types)
changesize(target_path)