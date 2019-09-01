# -*- coding:utf-8 -*-


from PIL import Image
import cv2
import numpy as np
import os
from pandas import DataFrame

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
def getimgdir(): # 获取当前目录下所有图片路径
    imgdirs = []
    imgTypes = [".png", ".jpg", ".bmp"]
    presentfiles = os.getcwd()#获得当前工作目录
    for root, dirs, files in os.walk("."):
        r = root[2:]
        for afile in files:
            if r != '':
                ffile = presentfiles+"\\"+r + "\\" + afile
            else:
                ffile = presentfiles + "\\"  + afile
            # print ffile

            if ffile[ffile.rindex("."):].lower() in imgTypes:
                print ffile
                imgdirs.append(ffile)
    return imgdirs

	
if __name__ == '__main__':	
	x = [[]]
	for i in getimgdir():
		im = color_moments(i)
		x.append(im)
	del x[0]
	df =  DataFrame(x,columns=list('abcdefghi'))
	print x
	print df

