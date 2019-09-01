# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import os
from PIL import Image
import cv2
import numpy as np

def splitimage(src, halfw, halfh, dstpath):  # 分割图片
    img = Image.open(src)
    w, h = img.size

    s = os.path.split(src)
    if dstpath == '':
        dstpath = s[0]
    fn = s[1].split('.')
    basename = fn[0]
    ext = fn[-1]

    box = (w // 2 - halfw, h // 2 - halfh, w // 2 + halfw, h // 2 + halfh)
    pic_cut_name = os.path.join(dstpath, basename + '_cut' + '.' + ext)
    img.crop(box).save(os.path.join(dstpath, basename + '_cut' + '.' + ext), ext)
    return pic_cut_name

# Compute low order moments(1,2,3)
def color_moments(filename): # 颜色矩方法进行特征提取
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


# src = input('请输入图片文件路径：')
src = "test.png"
if os.path.isfile(src):
    # dstpath = input('请输入图片输出目录（不输入路径则表示使用源图片所在目录）：')
    dstpath = r"C:\Users\zhuwenjing\Desktop"
    if (dstpath == '') or os.path.exists(dstpath):
        halfh = int(input('请输入切割后图片行高的一半：'))
        halfw = int(input('请输入切割后图片列宽的一半：'))
        if halfh > 0 and halfw > 0:
            filename = splitimage(src, halfh, halfw, dstpath)
            pixs = color_moments(filename)
            print pixs
        else:
            print('无效的行列切割参数！')
    else:
        print('图片输出目录 %s 不存在！' % dstpath)
