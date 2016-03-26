# __author__ = 'guchaojie'
# -*- coding: utf-8 -*-
# This py file is to the split the captcha into single alphabet or number
from __future__ import division
import time
import urllib2
import socks
from sockshandler import SocksiPyHandler
from PIL import Image, ImageEnhance, ImageFilter, ImageGrab


class Decaptcha:
    def __init__(self, new_img_id, counter, number):
        while counter < number:
            print '正在处理第%d张' % counter
            tmp_file_name = self.crawler(counter)
            temp_img_id = self.img2binary(img=tmp_file_name, new_img_id=new_img_id, counter=counter)
            print '剪切得到数字个数:', temp_img_id - new_img_id
            new_img_id = temp_img_id
            counter += 1
            time.sleep(1)
        print '截取成功率:', new_img_id / (counter * 4)

    def crawler(self, counter):
        ip = ''
        port = 
        url = ''
        filename = "images/MJ%d.jpg" % counter
        opener = urllib2.build_opener(SocksiPyHandler(socks.SOCKS5, ip, port))
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')]
        response = opener.open(url)
        htmlData = response.read()
        f = open(filename, 'w')
        f.write(htmlData)
        f.close()
        return filename

    def add_background(self, image, counter):
        img = Image.open(image)
        x, y = img.size
        p = Image.new('RGBA', img.size, (255, 255, 255))
        p.paste(img, (0, 0, x, y), img)
        p.save("bk-images/MJbackground-%d.png" % counter, "PNG")
        return p

    def img2binary(self, img, new_img_id, counter):
        img = self.add_background(image=img, counter=counter)
        assert isinstance(img, Image.Image)
        img = img.filter(ImageFilter.MedianFilter(3))  # use median filter to de-noise
        img.save("filter-images/%d.png" % counter, "PNG")
        enhancer = ImageEnhance.Contrast(img)  # 增加对比对
        img = enhancer.enhance(2)
        enhancer = ImageEnhance.Sharpness(img)  # 锐化
        img = enhancer.enhance(2)
        enhancer = ImageEnhance.Brightness(img)  # 增加亮度
        img = enhancer.enhance(2)
        img = img.convert("L")  # transfer the image into gray-scale
        img.save("gray-images/%d.png" % counter, "PNG")
        length = img.size[0]
        width = img.size[1]  # find the length and the width of the image
        # print 'size-length:', length, 'width', width
        counter = 0
        num_of_valid_pix = []  # this data structure is to store the number of valid pixels for each column.
        pixdata = img.load()  # load the image data into the @pixdata
        # retrival all the pixels in the image
        for x in range(0, length):
            for y in range(0, width):
                # change the valve
                if pixdata[x, y] < 200:
                    counter += 1
                    pixdata[x, y] = 0  # reset the pixdata to binary form, 1 represents for valid pixel
                else:
                    pixdata[x, y] = 255  # reset the pixdata to binary form, 0 represents for invalid pixel
            num_of_valid_pix.append(counter)
            counter = 0  # this counter is used to count the number of the pixel for each row
        letter_col_id = []
        i = 0
        # the following part is to separate the letters out from the given CAPTCHA.
        while i in range(len(num_of_valid_pix)):
            letter_id = []  # @letter_id stores the cols for each letter
            # letter feature: there must be blank cols that contains no valid pixels in the column
            while num_of_valid_pix[i] != 0:
                letter_id.append(i)
                i += 1
            if letter_id:
                letter_col_id.append(letter_id)
            i += 1
        # check the num of lines for each letter
        numofLetters = len(letter_col_id)
        # this part is dealing with the saparated
        for j in range(numofLetters):
            colsForLetter = len(letter_col_id[j])
            # if colsForLetter in range(3, 25):
            if colsForLetter in range(5, 14):
                file = open("trainingdigit/demo%d.txt" % new_img_id, 'w')
                # listbuffer = []
                newimg = Image.new("L", (len(letter_col_id[j]), width))
                # newimg = newimg.load()
                for y in range(width):
                    # rowbuffer = []
                    i = 0
                    for x in letter_col_id[j]:
                        # rowbuffer.append(pixdata[x, y])
                        # newimg[i, y] = pixdata[x, y]
                        if pixdata[x, y] == 255:
                            file.write("0")  # 0 for there's a invalid digit
                        elif pixdata[x, y] == 0:
                            file.write("1")  # 1 for there's a valid digit
                        newimg.putpixel([i, y], pixdata[x, y])
                        i += 1
                    # listbuffer.append(rowbuffer)
                    file.write("\n")
                file.close()
                newimg.save("trainingdigit/letter_%d.png" % new_img_id, "PNG")
                new_img_id += 1
        return new_img_id


if __name__ == '__main__':
    handle_class = Decaptcha(new_img_id=0, counter=0, number=400)
