# __author__ = 'guchaojie'
# -*- coding: utf-8 -*-
import ImageGrab  # from PIL
import time
import numpy as np
import string
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata
import os


def intToBin(i):
    """ 把整型数转换为双字节 """
    # 先分成两部分,高8位和低8位
    i1 = i % 256
    i2 = int(i / 256)
    # 合成小端对齐的字符串
    return chr(i1) + chr(i2)


def getheaderAnim(im):
    """ 生成动画文件头 """
    bb = "GIF89a"
    bb += intToBin(im.size[0])
    bb += intToBin(im.size[1])
    bb += "\x87\x00\x00"  # 使用全局颜色表
    return bb


def getAppExt(loops=0):
    """ 应用扩展,默认为0,为0是表示动画是永不停止
    """
    bb = "\x21\xFF\x0B"  # application extension
    bb += "NETSCAPE2.0"
    bb += "\x03\x01"
    if loops == 0:
        loops = 2 ** 16 - 1
    bb += intToBin(loops)
    bb += '\x00'  # end
    return bb


def getGraphicsControlExt(duration=0.1):
    """ 设置动画时间间隔 """
    bb = '\x21\xF9\x04'
    bb += '\x08'  # no transparancy
    bb += intToBin(int(duration * 100))  # in 100th of seconds
    bb += '\x00'  # no transparant color
    bb += '\x00'  # end
    return bb


def _writeGifToFile(fp, images, durations, loops):
    """ 把一系列图像转换为字节并存入文件流中"""
    # 初始化
    frames = 0
    previous = None
    for im in images:
        if not previous:
            # 第一个图像
            # 获取相关数据
            palette = getheader(im)[1]  # 取第一个图像的调色板
            data = getdata(im)
            imdes, data = data[0], data[1:]
            header = getheaderAnim(im)
            appext = getAppExt(loops)
            graphext = getGraphicsControlExt(durations[0])

            # 写入全局头
            fp.write(header)
            fp.write(palette)
            fp.write(appext)

            # 写入图像
            fp.write(graphext)
            fp.write(imdes)
            for d in data:
                fp.write(d)

        else:
            # 获取相关数据
            data = getdata(im)
            imdes, data = data[0], data[1:]
            graphext = getGraphicsControlExt(durations[frames])

            # 写入图像
            fp.write(graphext)
            fp.write(imdes)
            for d in data:
                fp.write(d)
                # 准备下一个回合
        previous = im.copy()
        frames += 1

    fp.write(";")  # 写入完成
    return frames


def writeGif(filename, images, duration=0.1, loops=0, dither=1):
    """
    writeGif(filename, images, duration=0.1, loops=0, dither=1)
    从输入的图像序列中创建GIF动画
    images 是一个PIL Image [] 或者 Numpy Array
    """
    images2 = []
    # 先把图像转换为PIL格式
    for im in images:

        if isinstance(im, Image.Image):  # 如果是PIL Image
            images2.append(im.convert('P', dither=dither))

        elif np and isinstance(im, np.ndarray):  # 如果是Numpy格式
            if im.dtype == np.uint8:
                pass
            elif im.dtype in [np.float32, np.float64]:
                im = (im * 255).astype(np.uint8)
            else:
                im = im.astype(np.uint8)
            # 转换
            if len(im.shape) == 3 and im.shape[2] == 3:
                im = Image.fromarray(im, 'RGB').convert('P', dither=dither)
            elif len(im.shape) == 2:
                im = Image.fromarray(im, 'L').convert('P', dither=dither)
            else:
                raise ValueError("图像格式不正确")
            images2.append(im)

        else:
            raise ValueError("未知图像格式")

    # 检查动画播放时间
    durations = [duration for im in images2]
    # 打开文件
    fp = open(filename, 'wb')
    # 写入GIF
    try:
        n = _writeGifToFile(fp, images2, durations, loops)
    finally:
        fp.close()
    return n


# 将多帧位图合成为一幅gif图像
def images2gif(images, giffile, durations=0.05, loops=1):
    seq = []
    for i in range(len(images)):
        im = Image.open(images[i])
        background = Image.new('RGB', im.size, (255, 255, 255))
        background.paste(im, (0, 0))
        seq.append(background)
    frames = writeGif(giffile, seq, durations, loops)
    print frames, 'images has been merged to', giffile


# 将gif图像每一帧拆成独立的位图
def gif2images(filename, distDir='.', type='bmp'):
    if not os.path.exists(distDir):
        os.mkdir(distDir)
    print 'splitting', filename,
    im = Image.open(filename)
    im.seek(0)  # skip to the second frame
    cnt = 0
    type = string.lower(type)
    mode = 'RGB'  # image modea
    if type == 'bmp' or type == 'png':
        mode = 'P'  # image mode
    im.convert(mode).save(distDir + '/%d.' % cnt + type)
    cnt += 1
    try:
        while 1:
            im.seek(im.tell() + 1)
            im.convert(mode).save(distDir + '/%d.' % cnt + type)
            cnt += 1
    except EOFError:
        pass  # end of sequence
    white = (255, 255, 255)
    preIm = Image.open(distDir + '/%d.' % 0 + type).convert('RGB')
    size = preIm.size
    prePixs = preIm.load()
    for k in range(1, cnt):
        print '.',
        im = Image.open(distDir + '/%d.' % k + type).convert('RGB')
        pixs = im.load()
        for i in range(size[0]):
            for j in range(size[1]):
                if pixs[i, j] == white:
                    pixs[i, j] = prePixs[i, j]
        preIm = im
        prePixs = preIm.load()
        im.convert(mode).save(distDir + '/%d.' % k + type)
    print '\n', filename, 'has been split to directory: [', distDir, ']'
    return cnt  # 总帧数


if __name__ == '__main__':
    frames = gif2images('', distDir='tmp', type='png')
    images = []
    for i in range(frames - 1, -1, -1):
        images.append('tmp/%d.png' % i)
        # images2gif(images, 'save.gif', durations=0.05)
