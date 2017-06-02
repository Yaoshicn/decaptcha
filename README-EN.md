# Decaptcha
This simple Python programme can help recognize captcha. The main function is implemented by some machine learning algorithms.

## How to?
1. Get the captcha using a crawler
2. Image processing
3. Label the training sample 
4. Load the training set
5. Test with test set

## Before You Start
1. Image (Lib for Processing Images)
    - [jpeg](http://www.ijg.org/files/)
    - [zlib](http://www.zlib.net)
    - [PIL](http://effbot.org/imagingbook/introduction.htm#using-the-image-class)

2. numpy (Lib for Handling Math Problems)

3. ImageEnhance (Lib for Processing Images)
```Python
enhancer = ImageEnhance.Contrast(img)    # Increase contrase
img = enhancer.enhance(2)
enhancer = ImageEnhance.Sharpness(img)   # Sharper image
img = enhancer.enhance(2)
enhancer = ImageEnhance.Brightness(img)  # Increase brightness
img = enhancer.enhance(2)
```

## How to Handle with a Captcha

### For Statical Image
1. Remove image noise
2. Clear interference line
3. Cutting picture
4. Output information

### For GIF
1. Save the GIF frame by frame
2. Get the durations between every 2 frame
3. The target frame may have the longest pause time

## Algorithms for Recognizing
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
SVM can help recognize two different characters, such as "1" and "2". 

## References
- http://www.csie.ntu.edu.tw/~cjlin/libsvm/index.html?js=1#svm-toy-js
- http://www.pami.sjtu.edu.cn/people/gpliu/document/libsvm_src.pdf
- Machine Learning in Action

## License
MIT
