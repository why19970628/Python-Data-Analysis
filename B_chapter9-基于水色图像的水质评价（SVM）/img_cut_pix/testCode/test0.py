# -*- coding:utf-8 -*-


from PIL import Image
import cv2
import numpy as np
import os
from pandas import DataFrame

def color_moments(filename):
    img = cv2.imread(filename)
    if img is None:
        return
    # Convert BGR to HSV colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Split the channels - h,s,v
    h, s, v = cv2.split(hsv)
    # Initialize the color feature
    color_feature = []
    # N = h.shape[0] * h.shape[1]
    # The first central moment - average
    h_mean = np.mean(h)  # np.sum(h)/float(N)
    s_mean = np.mean(s)  # np.sum(s)/float(N)
    v_mean = np.mean(v)  # np.sum(v)/float(N)
    color_feature.extend([h_mean, s_mean, v_mean])
    # The second central moment - standard deviation
    h_std = np.std(h)  # np.sqrt(np.mean(abs(h - h.mean())**2))
    s_std = np.std(s)  # np.sqrt(np.mean(abs(s - s.mean())**2))
    v_std = np.std(v)  # np.sqrt(np.mean(abs(v - v.mean())**2))
    color_feature.extend([h_std, s_std, v_std])
    # The third central moment - the third root of the skewness
    h_skewness = np.mean(abs(h - h.mean())**3)
    s_skewness = np.mean(abs(s - s.mean())**3)
    v_skewness = np.mean(abs(v - v.mean())**3)
    h_thirdMoment = h_skewness**(1./3)
    s_thirdMoment = s_skewness**(1./3)
    v_thirdMoment = v_skewness**(1./3)
    color_feature.extend([h_thirdMoment, s_thirdMoment, v_thirdMoment])

    return color_feature

# 获取当前工作目录及子目录下所有图片文件的绝对路径
def getimgdir():
    imgdirs = []
    imgTypes = [".png", ".jpg", ".bmp"]
    presentfiles = os.getcwd()#获得当前工作目录
    for root, dirs, files in os.walk("."):
        r = root[2:]
        for afile in files:
            ffile = presentfiles+"\\"+r + "\\" + afile
            if ffile[ffile.rindex("."):].lower() in imgTypes:
                imgdirs.append(ffile)
    return imgdirs

'''将图片切割成（2*halfw）*（2*halfh）像素的文件，并返回切割后的文件的绝对路径
src是待切割的文件的绝对路径，halfw是切割后图片的宽度的一半, 
halfh是切割后图片的长度的一半，dstpath是切割后图片的保存路径'''
def splitimage(src, halfw, halfh, dstpath):
    img = Image.open(src)
    w, h = img.size

    s = os.path.split(src)
    if dstpath == '':
        dstpath = s[0]
    fn = s[1].split('.')
    basename = fn[0]
    ext = fn[-1]

    box = (h // 2 - halfh, w // 2 - halfw, h // 2 + halfh, w // 2 + halfw)
    pic_cut_name = os.path.join(dstpath, basename + '_cut' + '.' + ext)
    img.crop(box).save(os.path.join(dstpath, basename + '_cut' + '.' + ext), ext)
    return pic_cut_name
# x = [[]]
# for i in getimgdir():
#     im = color_moments(i)
#     x.append(im)
# del x[0]
# df =  DataFrame(x,columns=list('abcdefghi'))
# print x
# print df

# 输出图片输出目录
def saveimg(dstpath):
    if (os.path.exists(dstpath) == False) and  dstpath != '': # 若输入的路径不存在，则创建该目录
        os.makedirs(dstpath)  # 创建目标文件夹
    if dstpath == '': #不输入路径(直接回车）则表示使用源图片所在目录
        dstpath = os.getcwd()
    return dstpath


# 待切割的图片所在的目录（多个图片所在的目录，是个列表格式）
waitcut = getimgdir()
# 输入图片输出路径（若不存在，则新建目录）
dstpath = saveimg(raw_input('请输入图片输出目录：'))
for i in waitcut:#所有图片文件路径
    halfh = input('请输入切割后图片高的一半：')
    halfw = input('请输入切割后图片宽的一半：')
    if halfh > 0 and halfw > 0:
        filename = splitimage(i, halfh, halfw, dstpath)
        print filename
        # pixs = color_moments(filename)
        # print pixs
    else:
        print('无效的行列切割参数！')
