# -*- coding:utf-8# -*- coding:utf-8 -*-


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

# 获取当前工作目录及子目录下所有图片文件的绝对路径，包含其所有子文件夹中的图片
def getimgdir(imgfilename):
    imgdirs = []
    imgTypes = [".png", ".jpg", ".bmp"]
    if imgfilename:
        presentfiles = imgfilename
    else:
        presentfiles = os.getcwd()  # 获得当前工作目录

    for root, dirs, files in os.walk("."):
        r = root[2:]
        for afile in files:
            if r != '':
                ffile = presentfiles + "\\" + r + "\\" + afile
            else:
                ffile = presentfiles + "\\" + afile

            if ffile[ffile.rindex("."):].lower() in imgTypes:
                imgdirs.append(ffile)
    return imgdirs

# 获取当前工作目录及子目录下所有图片文件的绝对路径 # 不包含下层文件夹中的图片
def getimgdir_designed(imgfilename):
    if os.path.exists(imgfilename)== False:# 若指定的文件夹不存在，则提示！
        print '你设定的指定文件夹不存在！'
        return None
    imgdirs = []
    imgTypes = [".png", ".jpg", ".bmp"]
    presentfiles = imgfilename#获得当前工作目录
    recursion = 0  # 控制递归深度，只递归当前目录
    for root, dirs, files in os.walk(presentfiles):
        for afile in files:
            ffile = presentfiles + "\\" + afile
            if ffile[ffile.rindex("."):].lower() in imgTypes:
                imgdirs.append(ffile)
        if (not recursion):
            break
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
    img.crop(box).save(pic_cut_name)
    return pic_cut_name

# 输出图片输出目录
def saveimg(dstpath):
    # if not dstpath or dstpath .isspace()
    if (os.path.exists(dstpath) == False) and  dstpath != '': # 若输入的路径不存在，则创建该目录
        os.makedirs(dstpath)  # 创建目标文件夹
    if dstpath == '': #不输入路径(直接回车）则表示使用源图片所在目录
        dstpath = os.getcwd()
    return dstpath


# 待切割的图片所在的目录（多个图片所在的目录，是个列表格式）
doc = r'D:\PycharmProjects\readwriteFiles\img_cut_pix'
# waitcut = getimgdir(doc) #注意：方式1、获取的当前工作目录下的所有图片文件(包含所有子文件夹的图片）
waitcut = getimgdir_designed(doc)#注意：方式2、获取指定目录下的图片文件(不包含子文件夹的图片，仅当前文件夹）

print waitcut

# 输入图片输出路径（若不存在，则新建目录）
dstpath = saveimg(raw_input('请输入图片输出目录：')) # 例如，输入：D:\PycharmProjects\readwriteFiles\img_cut_pix\pic_cut
resultlist = [[]]
while True:
    try:
        halfh = input('请输入切割后图片高的一半(数值）：')
        halfw = input('请输入切割后图片宽的一半（数值）：')
        print '正在批处理切割图片...'
        for i in waitcut:#所有图片文件路径
            filename = splitimage(i, halfh, halfw, dstpath)
            impix = color_moments(filename)
            resultlist.append(impix)
        print '图片切割完成！'
    except:# 此处异常包括 (1) 输入的是非数值型（2）输入的数值是非正数 ！注意：如果数值过大，不影响切割，会超出原图
        print "输入的字符不符合要求，请重新输入！"
    else:
        break
del resultlist[0]
columnsname= ['R通道一阶矩','G通道一阶矩','B通道一阶矩','R通道二阶矩','G通道二阶矩','B通道二阶矩',\
              'R通道三阶矩','G通道三阶矩','B通道三阶矩',]
df =  DataFrame(resultlist,columns=columnsname)

print df