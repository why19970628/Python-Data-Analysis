import numpy as np
print(np.arange(0,1,0.01))
print(np.random.randn(100))
arr1=np.array([1,2,3,4])
arr2=np.array([2,3,4,5])
print(arr1+arr2)
print(arr1-arr2)
print(arr1*arr2)
print(arr1/arr2)
print(arr1**arr2)
print('矩阵乘',np.multiply(arr1,arr2))
a=[0,1,0,1]
b=[0,1,0,1]
c=np.bmat('a,b')
print(c)



#print(np.random.rand(10,5))