# decaptcha
通过简单的图像识别算法来完成验证码识别，打算把机器学习中的分类算法全部使用一遍
## 前期准备
### Image(图像处理库)
- [jpeg](http://www.ijg.org/files/)
- [zlib](http://www.zlib.net)
- [PIL](http://effbot.org/imagingbook/introduction.htm#using-the-image-class)

### numpy(数学处理库)

### ImageEnhance(图像处理库)
```Python
enhancer = ImageEnhance.Contrast(img)  # 增加对比对
img = enhancer.enhance(2)
enhancer = ImageEnhance.Sharpness(img)  # 锐化
img = enhancer.enhance(2)
enhancer = ImageEnhance.Brightness(img)  # 增加亮度
img = enhancer.enhance(2)
```
## 图像处理
### 静态图片
#### 1.图片清除噪点
#### 2.图片清除干扰线
#### 3.图片切割
#### 4.信息输出
### 动态图片
#### 1.按帧转存 GIF
#### 2.读取每个 GIF 的 Duration 属性
#### 3.找到 Duration 最长的图片，后同静态图片处理
## 验证码识别
### KNN
```Python
# kNN algorithm
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]  # changed
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
```
### SVM
根据算法的性质，我们把问题设定成一个二分类问题：识别数字1和9（当然也可以是其他的任意两个数字）
- http://www.csie.ntu.edu.tw/~cjlin/libsvm/index.html?js=1#svm-toy-js
- http://www.pami.sjtu.edu.cn/people/gpliu/document/libsvm_src.pdf

## 使用方法
1. 爬取验证码
2. 对图像做处理并切分
3. 手工标注数据
4. 导入训练集
5. 使用测试集

