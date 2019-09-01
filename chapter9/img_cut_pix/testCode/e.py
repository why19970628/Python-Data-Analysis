# -*- coding:utf-8 -*-
import os

# 获取指定文件夹下的文件名
def getimgdir_designed(imgfilename):
    if os.path.exists(imgfilename)== False:
        print '你设定的指定文件夹不存在！'
        return None
    imgdirs = []
    imgTypes = [".png", ".jpg", ".bmp"]
    presentfiles = imgfilename#获得当前工作目录
    for root, dirs, files in os.walk(presentfiles):
        for afile in files:
            ffile = presentfiles + "\\" + afile
            if ffile[ffile.rindex("."):].lower() in imgTypes:#返回子字符串 str 在字符串中最后出现的位置，如果没有匹配的字符串会报异常，你可以指定可选参数[beg:end]设置查找的区间
                imgdirs.append(ffile)
    return imgdirs

doc = r'C:\Users\zhuwenjing\Desktop\test\pic'
print getimgdir_designed(doc)