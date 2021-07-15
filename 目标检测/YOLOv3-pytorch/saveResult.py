'''
用来遍历测试集。
'''
import os

testPath = r'./img'
savePath = r'./result'

temp_jpg = os.listdir(testPath)
total_jpg = []
for jpg in temp_jpg:
    if jpg.endswith(".jpg"):
        total_jpg.append(jpg)

num = len(total_jpg)
list=range(num)

ftest = open(os.path.join(savePath,'test.txt'), 'w')

for i in list:
    name = total_jpg[i][:-4]+'\n'
    ftest.write(name)

ftest.close()