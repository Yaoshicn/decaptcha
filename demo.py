# __author__ = 'Yaoshi'
# -*- coding: utf-8 -*-
import os,sys
from PIL import Image,ImageEnhance,ImageFilter,ImageGrab

def Change_Image(Docu_Name,Dist):
    im = Handle_Image(Docu_Name,Dist)
    X_Value=Cut_X(im)
    Y_Value=Cut_Y(im)

    ims = []
    Image_Value=[]
    Image_Values=[]
    Image_Value_Row=[]
    for k in range(4):
        im1= im.crop((X_Value[(2*k)],Y_Value[(2*k)],(X_Value[(2*k+1)]+1),(Y_Value[(2*k+1)]+1))) #切割图像为4个子图像
        ims.append(im1)
        for j in range(Y_Value[(2*k)],(Y_Value[(2*k+1)]+1)):
            for i in range(X_Value[(2*k)],(X_Value[(2*k+1)]+1)):
                if im.getpixel((i,j))==0:#黑色像素的值是0
                    Image_Value_Row.append(1)
                else:
                    Image_Value_Row.append(0)
            Image_Value.append(Image_Value_Row)#
            Image_Value_Row=[]#

        Image_Values.append(Image_Value)
        Image_Value=[]

    return Image_Values #返回切割后各个图像对应的黑白像素的0-1值所存储在其中的三维数组。

#处理图片以便后续的0-1二值化
def Handle_Image(Docu_Name,Dist):
    im = Image.open('%s'%(Dist+Docu_Name)+'.png') #打开对应目录的png格式的验证码图片
    im=im.convert('RGB')
    for j in range(im.size[1]):
        for i in range(im.size[0]):
            Gray = Change_Gray(im.getpixel((i,j)))  #灰度化
            im.putpixel([i,j],(Gray,Gray,Gray))
            if i==0 or i==(im.size[0]-1): #将图片的第一行和最后一行设为白色。
                im.putpixel([i,j],(255,255,255))
            if j==0 or j==(im.size[1]-1):#将图片的第一列和最后一列设为白色。
                im.putpixel([i,j],(255,255,255))
    enhancer = ImageEnhance.Contrast(im) #增加对比对
    im = enhancer.enhance(2)
    enhancer = ImageEnhance.Sharpness(im) #锐化
    im = enhancer.enhance(2)
    enhancer = ImageEnhance.Brightness(im) #增加亮度
    im = enhancer.enhance(2)
    #im=im.convert('L').filter(ImageFilter.DETAIL) #滤镜效果
    im = im.convert('1') #转为黑白图片

    im = Clear_Point(im) #清除周围8个像素都是白色的孤立噪点
    im = Clear_Point_Twice(im) #清除两个孤立的噪点：周围8个像素中有7个是白色，而唯一的黑色像素对应的他的邻域（他周围的8个像素）中唯一的黑色像素是自身。
    im = Clear_Point_Third(im) #清除第三种噪点：左右都是3个（含）以上的空白列，自身相邻的3个列上的X值投影不大于3.

    return im

#改变灰度，查文献后发现据说按照下面的R，G，B数值的比例进行调整，图像的灰度最合适。
def Change_Gray(RGB_Value):
    Gray = int((RGB_Value[0]*299+RGB_Value[1]*587+RGB_Value[2]*114)/1000)
    return Gray

#清除单个孤立点
def Clear_Point(im):
    for j in range(1,(im.size[1]-1)):
        for i in range(1,(im.size[0]-1)):
            if im.getpixel((i,j))==0 and im.getpixel(((i-1),(j-1)))==255  and im.getpixel((i,(j-1)))==255  and im.getpixel(((i+1),(j-1)))==255  and im.getpixel(((i-1),j))==255  and im.getpixel(((i+1),j))==255  and im.getpixel(((i-1),(j+1)))==255  and im.getpixel((i,(j+1)))==255  and im.getpixel(((i+1),(j+1)))==255:
                im.putpixel([i,j],255)
    return im

#TODO 检查一下符号
def Clear_Point_Twice(im):
    for j in range(1,(im.size[1]-1)):
        for i in range(1,(im.size[0]-1)):
            if im.getpixel((i,j))==0 and ( im.getpixel(((i-1),(j-1)))+im.getpixel((i,(j-1)))+im.getpixel(((i+1),(j-1)))+im.getpixel(((i-1),j))+im.getpixel(((i+1),j))+im.getpixel(((i-1),(j+1)))+im.getpixel((i,(j+1)))+im.getpixel(((i+1),(j+1)))) == 255*7:
                if im.getpixel(((i+1),j))==0: #因为扫描的顺序是从上到下，从左到右，噪点只能是在自身像素的后面和下面，也就是只有4个可能性而已，而不是8个，可以减少一半的代码。
                    m=i+1
                    n=j
                    if ( im.getpixel(((m-1),(n-1)))+im.getpixel((m,(n-1)))+im.getpixel(((m+1),(n-1)))+im.getpixel(((m-1),n))+im.getpixel(((m+1),n))+im.getpixel(((m-1),(n+1)))+im.getpixel((m,(n+1)))+im.getpixel(((m+1),(n+1)))) == 255*7:
                       im.putpixel([i,j],255)
                       im.putpixel([m,n],255)
                elif im.getpixel(((i-1),(j+1)))==0:
                    m=i-1
                    n=j+1
                    if ( im.getpixel(((m-1),(n-1)))+im.getpixel((m,(n-1)))+im.getpixel(((m+1),(n-1)))+im.getpixel(((m-1),n))+im.getpixel(((m+1),n))+im.getpixel(((m-1),(n+1)))+im.getpixel((m,(n+1)))+im.getpixel(((m+1),(n+1)))) == 255*7:
                       im.putpixel([i,j],255)
                       im.putpixel([m,n],255)
                elif im.getpixel((i,(j+1)))==0:
                    m=i
                    n=j+1
                    if ( im.getpixel(((m-1),(n-1)))+im.getpixel((m,(n-1)))+im.getpixel(((m+1),(n-1)))+im.getpixel(((m-1),n))+im.getpixel(((m+1),n))+im.getpixel(((m-1),(n+1)))+im.getpixel((m,(n+1)))+im.getpixel(((m+1),(n+1)))) == 255*7:
                       im.putpixel([i,j],255)
                       im.putpixel([m,n],255)
                elif im.getpixel(((i+1),(j+1)))==0:
                    m=i+1
                    n=j+1
                    if ( im.getpixel(((m-1),(n-1)))+im.getpixel((m,(n-1)))+im.getpixel(((m+1),(n-1)))+im.getpixel(((m-1),n))+im.getpixel(((m+1),n))+im.getpixel(((m-1),(n+1)))+im.getpixel((m,(n+1)))+im.getpixel(((m+1),(n+1)))) == 255*7:
                       im.putpixel([i,j],255)
                       im.putpixel([m,n],255)
    return im

#依据图片像素颜色计算X轴投影
def Caculate_X(im):
    Image_Value=[]
    for i in range(im.size[0]):
        Y_pixel=0
        for j in range(im.size[1]):
            if im.getpixel((i,j))==0:
                temp_value=1
            else:
                temp_value=0
            Y_pixel = Y_pixel temp_value
        Image_Value.append(Y_pixel)
    return Image_Value

def Set_White_Y(im,List_Black):
    for j in range(im.size[1]):
        for i in range(List_Black[0],(List_Black[(len(List_Black)-1)] 1)):
            im.putpixel([i,j],255)
    return im

#清除第三种残余的孤立点
def Clear_Point_Third(im):
    Image_Value = Caculate_X(im)
    List01=[]
    List_Black=[]
    List03=[]
    for i in range(len(Image_Value)): #从左到右扫描
        if Image_Value[i] ==0 and len(List_Black) == 0 : #X轴投影是0，说明是空白列，黑色列的列表是空值，说明当前列是黑色列的左侧
            List01.append(i)
        elif  Image_Value[i] >0 : #X周投影大于0的列，即扫描到了黑色列
            List_Black.append(i)
        elif Image_Value[i] ==0 and len(List_Black)>0 and len(List_Black)<=3:# 黑色列的列表的长度大于0，不大于3个空白字符，现在的X轴投影为0，说明现在扫描到了孤立噪点所在的黑色列右侧的空白列
            List03.append(i)
            if len(List03)==3:#空白列为3列
                    im = Set_White_Y(im,List_Black) #逐次将多列设为全白
                    List01=[]
                    List_Black=[]
                    List03=[]
        elif Image_Value[i] ==0 and len(List_Black)>3: #当前是空白列，黑色列的数量大于3，说明扫描到了数字所在部分（不是噪点）的右侧空白列。
            List01=[]
            List_Black=[]
            List03=[]
            List01.append(i)
    return im

#纵向切割，依据X轴的投影，将图片切割为4张图片，并返回切割点的坐标
def Cut_X(im):
    Image_Value = Caculate_X(im)
    X_value=[]
    List0=[]
    List1=[]
    ListRow0=[]
    ListRow1=[]
    for i in range(len(Image_Value)):
        if Image_Value[i] ==0 and len(ListRow1)==0: #数字左侧的空白列
            ListRow0.append(i)
        elif Image_Value[i] ==0 and len(ListRow1)>0: #数字右侧的空白列
            List1.append(ListRow1)
            ListRow1=[]
            ListRow0.append(i)
        elif Image_Value[i] >0 and len(ListRow0)>0 : #数字列
            List0.append(ListRow0)
            ListRow0=[]
            ListRow1.append(i)
        elif Image_Value[i] >0 and len(ListRow0)==0: #数字列
            ListRow1.append(i)
    if len(List1)==1 : #如果只有1个数字右侧的空白列，放弃切割
        for i in range(4):
            X_value.append(1+12*i)#
            X_value.append(12*i+12)
    elif len(List1)==2 :    #如果只有2个数字右侧的空白列，放弃切割
        for i in range(4):
            X_value.append(1+12*i)#
            X_value.append(12*i+12)
    elif len(List1)==3 : #如果有3个数字右侧的空白列，将数字列中最长的那段值进行拆分，拆分点在X轴投影的大于第五位后的第一个最低点。
         Max_index = Max_Index(List1)
        for i in range(len(List1)):
            if i == Max_index:
                index = Cut_Two(List1[i],Image_Value)
                X_value.append(List1[i][0])
                X_value.append(List1[i][index])
                X_value.append(List1[i][(index+1)])
                X_value.append(List1[i][(len(List1[i])-1)])
            else:
                X_value.append(List1[i][0])
                X_value.append(List1[i][(len(List1[i])-1)])
    elif len(List1)==4 : #4个空白列
        for i in range(len(List1)):
            X_value.append(List1[i][0])
            X_value.append(List1[i][(len(List1[i])-1)])
    elif len(List1)==5 : #如果有5个数字右侧的空白列，取长度最长的4段。
        Min_index = Min_Index(List1)
        for i in range(len(List1)):
            if i <> Min_index:
                X_value.append(List1[i][0])
                X_value.append(List1[i][(len(List1[i])-1)])
    elif len(List1)>5 : #大于5个直接放弃切割
        for i in range(4):
            X_value.append(1+12*i)
            X_value.append(12*i+12)
    return X_value

#返回矩阵各行最大值位置的函数，以便找到有颜色的列中X轴投影最大的地方
def Max_Index(List1):
    Max = 0
    Max_index=0
    for i in range(len(List1)):
        if len(List1[i])>Max:
            Max=len(List1[i])
            Max_index=i
    return Max_index

#返回矩阵各行最小值位置的函数，以便找到有颜色的列中X轴投影最小的地方
def Min_Index(List1):
    Min = 50
    Min_index=0
    for i in range(len(List1)):
        if len(List1[i])            Min=len(List1[i])
            Min_index=i
    return Min_index

#分割两个紧挨的数字
def Cut_Two(ListRow,Image_Value):
    index = 0
    start = 0
    if len(ListRow)>=15:
        start = 3
    for i in range((1+start),(len(ListRow)-1)):
        if Image_Value[ListRow[i]]<= Image_Value[ListRow[(i+1)]] and Image_Value[ListRow[i]]<=2:#
            index = i
            break

    return index

#横向切割 4张图片，4次投影，并返回切割点的坐标
def Cut_Y(im):
    Y_value=[]
    Image_Value=[]
    Cut_Xs=Cut_X(im)
    for k in range(4):
        Image_Value=[]
        for j in range(im.size[1]):
            X_pixel=0
            for i in range(Cut_Xs[(2*k)],(Cut_Xs[(2*k+1)]+1)):
                if im.getpixel((i,j))==0:
                    X_pixel = X_pixel+1
            Image_Value.append(X_pixel)
        for i in range(len(Image_Value)):
            if Image_Value[i]>0:
                Y_value.append(i)
                break
        for i in range((len(Image_Value)-1),0,(-1)):
            if Image_Value[i]>0:
                Y_value.append(i)
                break

    return Y_value

#切割完毕后，将4个子图片的像素颜色信息写入到文本文件
def Write_ImageFile(Docu_Name,Image_Value,Dist):
    f=open('%s' % (Dist+Docu_Name+'.txt'),'w')
    f.write(str(Image_Value))
    f.close()

def Write_Txt(Dist):
    ''' txt文件的写入格式
    #文件名
    a=[]
    Image_Libs.append(a)
    '''
    Big_Txt = Document_Name()
    fw = open ('%s' %(Dist+Big_Txt+'.txt'),'a')
    Array=[]
    for item in os.listdir(Dist): # 遍历指定目录
        if os.path.isfile(Dist+item) and item.endswith('.txt') and len(item)<20: # 判断是否为.txt文件
            f = open((Dist+item),'r') # 打开文件
            line=f.readline()
            for i in range(2): #为了保障比对时的成功率，每个素材要写入2次，这样可以提高比对成功率。
                fw.write('#')
                fw.write(item)
                fw.write('\n')
                fw.write('a=')
                fw.write(line)
                fw.write('\nImage_Libs.append(a)\n')
                Array.append(int(item[0]))
            f.close()
    a={}
    for i in Array:
        if Array.count(i)>0:
            a[i]=Array.count(i)
    b=[]
    b.append(a[0])
      for i in range(1,len(a)):
        b.append(( a[i]+b[i-1] )) #生成一个从0到9，依次存储各个数字的累积个数的数组。
    b=[0]+b
    fw.write('\n')
    fw.write('Rank_Index=')
    fw.write(str(b))
    fw.close()

#由于我这里使用二维数组进行比对，所以为了方便的获取二维数组中的部分内容，定义了一个取这些内容的函数，参数 i,j是行的起始和终止列，参数k，m是列的起始和终止列
def Get_Array(Image_Value,i,j,k,m):
    Result_Array=[]
    for n in range(k,(m+1)):
            Result_Array.append(Image_Value[n][i:(j+1)])
    return Result_Array

#为了进行二维数组的相似度的比较，需要定义一个计算矩阵（就是二维数组）距离的函数，注意，由于二维数组的长宽会不同，为了消除这个长宽的影响，矩阵距离要除以矩阵的长乘宽。
def Caculate_Distance(Image_Value,Image_Lib):
    Result_Num =0
    for i in range(len(Image_Value)):
        for j in range(len(Image_Value[0])):
            Result_Num=Result_Num+abs(Image_Value[i][j]-Image_Lib[i][j]) #矩阵距离就是所有元素的差的绝对值的和
    return round((float(Result_Num)/float(len(Image_Value)*len(Image_Value[0]))),3)

#主函数，通过计算矩阵距离来排序后判断是哪个数字
def Rank(Result_Calculate,Result_Index,Width_Image,Image_Value):
    Result_Num = '0'
    Result_Maps ={} #这里要用到字典，以便进行排序
    for i in range(len(Result_Calculate)):
        Result_Maps[Result_Index[i]]=Result_Calculate[i]
    Result_Map = sorted(Result_Maps.iteritems(), key=lambda d:d[1])
    temp =[]
    for i in range(len(Result_Calculate)):
        temp.append((Get_Realnum(Result_Index[i],IL.Rank_Index),Result_Calculate[i]))
    Result_Temp =[]
    for i in range(5):#取前5位
        Result_Temp.append(Get_Realnum(Result_Map[i][0],IL.Rank_Index))

    a = Rank_modify(Width_Image,Result_Map,IL.Rank_Index,Result_Temp)
    a = Rank_Num(Image_Value,a)
    a_sort = Sort_Modify(a,Result_Temp)

    Result_Num = str(a_sort[0][0])

    return Result_Num

#根据矩阵距离值进行判断修正
def Rank_modify(Width_Image,Result_Map,Rank_Index,Result_Temp):
    a = {0:0.0,1:0.0,2:0.0,3:0.0,4:0.0,5:0.0,6:0.0,7:0.0,8:0.0,9:0.0}
    for i in Result_Temp:
        if Result_Temp.count(i)>0:
            a[i]=round(float(Result_Temp.count(i))/float(len(Result_Temp)),2)#
    if Width_Image<6: #如果子图片的宽度小于6，图片数字是1的概率就加0.2
        a[1]=round((a[1]+0.2),2)

    for i in range(len(Result_Map)):
        if Result_Map[i][1]<=0.1 and Result_Map[i][1]>0.05 : #如果矩阵距离很小，说明相似度很高，要人为加大其概率
            a[(Get_Realnum(Result_Map[i][0],Rank_Index))]=round((a[(Get_Realnum(Result_Map[i][0],Rank_Index))]+0.2),2)
        elif Result_Map[i][1]<=0.05 : #如果矩阵距离很小，说明相似度很高，要人为加大其概率
            a[(Get_Realnum(Result_Map[i][0],Rank_Index))]=round((a[(Get_Realnum(Result_Map[i][0],Rank_Index))]+0.4),2)
    return a

#依据图形修正
def Rank_Num(Image_Value,a):
    X_Value = Get_X(Image_Value)
    Y_Value = Get_Y(Image_Value)

    X_Average = MS.Average(X_Value)
    Y_Average = MS.Average(Y_Value)
    X_Std = MS.Std(X_Value)
    Y_Std = MS.Std(Y_Value)
    X_MaxIndex = MS.Get_MaxIndex(X_Value)
    Y_MaxIndex = MS.Get_MaxIndex(Y_Value)
    if X_Std<=1.0 and Y_Std<=1.0:  #图像是1时X，Y轴投影的统计特性
        a[1]=round((a[1]+0.2),2)
    elif Y_Std<=1.0 and abs(X_MaxIndex-round(float(len(Image_Value[0]))/2.0,2))<=2:
        a[1]=round((a[1]+0.2),2) #图像是1时X，Y轴投影的统计特性
    elif X_Std>2.0 and Y_Std>2.0 and X_MaxIndex > round(float(len(Image_Value[0]))/2.0,2) and Y_MaxIndex < round(float(len(Image_Value))/2.0,2) :
        a[7]=round((a[7]+0.2),2) #图像是7时X，Y轴投影的统计特性

    return a

#按照排序先后进行修正
def Sort_Modify(a,Result_Temp):
    a_sort=sorted(a.iteritems(), key=lambda d:d[1], reverse=True)
    if a_sort[0][1]==a_sort[1][1]:
        for i in range(len(Result_Temp)):
            if Result_Temp[i]== a_sort[0][0] or Result_Temp[i]== a_sort[1][0]: #如果前5位中有2个都是2次出现的数字，提高出现在最前面的数字的概率
                if Result_Temp[i]== a_sort[0][0]:
                    a[a_sort[0][0]] = a[a_sort[0][0]] + 0.1
                elif Result_Temp[i]== a_sort[1][0]:
                    a[a_sort[1][0]] = a[a_sort[1][0]] + 0.1
                break
    a_sort=sorted(a.iteritems(), key=lambda d:d[1], reverse=True)
    return a_sort

#x轴投影
def Get_X(Image_Value):
    X_Value =[]
    for i in range(len(Image_Value[0])):#51
        Y_pixel=0
        for j in range(len(Image_Value)):
            Y_pixel = Y_pixel +Image_Value[j][i]
        X_Value.append(Y_pixel)
    return X_Value#51

#Y轴投影
def Get_Y(Image_Value):
    Y_Value =[]
    for j in range(len(Image_Value)):#16
        X_pixel=0
        for i in range(len(Image_Value[0])):
            X_pixel = X_pixel +Image_Value[j][i]
        Y_Value.append(X_pixel)
    return Y_Value