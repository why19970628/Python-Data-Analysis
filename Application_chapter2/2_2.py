import numpy as np #导入 NumPy 库
# 代码 2-21
arr = np.arange(12)  #创建一维数组
print('创建的一维数组为：',arr)
print('新的一维数组为：',arr.reshape(3,4))  #设置数组的形状
print('数组维度为：',arr.reshape(3,4).ndim)  #查看数组维度

# 代码 2-22
arr = np.arange(12).reshape(3,4)
print('创建的二维数组为：',arr)
print('数组展平后为：',arr.ravel())

# 代码 2-23
print('数组展平为：',arr.flatten())  #横向展平
print('数组展平为：',arr.flatten('F'))  #纵向展平

# 代码 2-24
arr1 = np.arange(12).reshape(3,4)
print('创建的数组1为：',arr1)

arr2 = arr1*3
print('创建的数组2为：',arr2)
print('横向组合为：',np.hstack((arr1,arr2)))  #hstack函数横向组合 ==concatenate((arr1,arr2),axis=1)

# 代码 2-25
print('纵向组合为：',np.vstack((arr1,arr2)))  #vstack函数纵向组合

# 代码 2-27
arr = np.arange(16).reshape(4,4)
print('2-27创建的二维数组为：',arr)
print('横向分割为：',np.hsplit(arr, 2))  #hsplit函数横向分割 #np.split(arr, 2, axis=1))

# 代码 2-28
print('纵向分割为：',np.vsplit(arr, 2))  #vsplit函数纵向分割  #np.split(arr, 2, axis=0))

# 代码 2-29
print('横向分割为：',np.split(arr, 2, axis=1))  #split函数横向分割
print('纵向分割为：',np.split(arr, 2, axis=0))  #split函数纵向分割

