# -*- coding:utf-8 -*-
import os
from PIL import Image

def splitimage(src, halfw, halfh, dstpath): # 分割图片
    img = Image.open(src)
    w, h = img.size

    s = os.path.split(src)
    if dstpath == '':
        dstpath = s[0]
    fn = s[1].split('.')
    basename = fn[0]
    ext = fn[-1]

    box = ( h // 2 - halfh, w // 2 - halfw,h // 2 + halfh, w // 2 + halfw, )
    pic_cut_name = os.path.join(dstpath, basename + '_cut' + '.' + ext)
    # print pic_cut_name
    img.crop(box).save(os.path.join(dstpath, basename + '_cut' + '.' + ext), ext)
	
	
if __name__ == '__main__':
	# src = input('请输入图片文件路径：')
	src = "test.png"
	if os.path.isfile(src):
		print '************'
		# print os.getcwd()
		# dstpath = input('请输入图片输出目录（不输入路径则表示使用源图片所在目录）：')
		dstpath = r"C:\Users\zhuwenjing\Desktop\a1" # 目标文件夹名称
		if os.path.exists(dstpath) == False:
			os.makedirs(dstpath)  # 创建目标文件夹
		if dstpath == '':
			dstpath = os.getcwd()
		if (dstpath == '') or os.path.exists(dstpath):
			halfh = input('请输入切割后图片高的一半：')
			halfw = input('请输入切割后图片宽的一半：')
			if halfh > 0 and halfw > 0:
				splitimage(src, halfh, halfw, dstpath)
			else:
				print('无效的行列切割参数！')
		else:
			print('图片输出目录 %s 不存在！' % dstpath)