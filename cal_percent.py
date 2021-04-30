# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 20:36:09 2021

@author: 19215
"""

#import image
import numpy  as np
import ADE20k_labels
import imageio
#import matplotlib.pyplot as plt
# import np
from PIL import ImageFont 
from PIL import ImageDraw
import os
#import skimage.io as io
#from skimage import data_dir
try:
    from PIL import Image
except ImportError:
    import Image
    

def cal_percent(image):
    '''计算图像各颜色百分比'''
   
    rgb = {} #颜色字典
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):                               
            if ((color_label[tuple(image[row, col])] not in rgb) or (row == 0 and col == 0)):
                rgb[color_label[tuple(image[row, col])]] = [1, tuple(image[row, col])]  #color的name作为rgb字典的键，值是一个列表
            else: 
                rgb[color_label[tuple(image[row, col])]][0] = rgb[color_label[tuple(image[row, col])]][0] + 1

    num  = 0            
    for k in rgb:
        num = num + 1 #颜色数量
        rgb[k][0] = str('{:.4f}%'.format(rgb[k][0] / 1728)) 
        #rgb[k][0] = rgb[k][0] / 9600
    
    #print(rgb)
    return rgb, num

def change_rgb(image,color_list,color_label):  # 返回颜色字典里含有的rgb，相当于把字典里不存在的rgb转换成里面存在的rgb   
    for row in range(image.shape[0]): #垂直
        for col in range(image.shape[1]): #水平
            if(tuple(image[row,col]) not in color_label): #如果读取的当前像素点的rgb不在颜色字典中，将其转换
                for cur_color in color_list:
                    if(judge(cur_color,image[row,col])): #判断两个像素是否近似                    
                        image[row,col] = cur_color #进行转换                        
                        break
                    
                       
    return image #返回转换后的图像像素矩阵
                

def judge(color1,color2): #判断两个颜色是否很相近
    distance = 150  #阈值
    absR = color1[0] - color2[0];
    absG = color1[1] - color2[1];
    absB = color1[2] - color2[2]; 
    if(np.sqrt(np.square(absR)+np.square(absG)+np.square(absB))<distance):        
        return True
    else:
        return False


def write_image(img, write_contents, text_size=10):
    '''在图片中写上文字'''

    #设置字体(从windows/font中查找自己所需要的字体)
    fontpath = 'font/simsun.ttc'#（宋体）
    font = ImageFont.truetype(fontpath, text_size) #设置字体为ImageDeaw.draw()服务
    if type(img) is np.ndarray:
        image = Image.fromarray(img) #array转换成Image(反过来则使用np.array())
    else:
        image = img
    draw = ImageDraw.Draw(image)
    #绘制文字信息
    draw.text((0,0), write_contents, font=font, fill=(0, 0, 0))

    return img

def create_rectangle(shape, color, text, text_size=10):
    '''创建正方形'''

    rectangle = Image.new('RGB', shape, color)
    rectangle = write_image(rectangle, text, text_size)
    return rectangle

def legend(image, image1, text_size=10):
    ''' 创建图例 '''

    #计算图像的各颜色百分比
    shape = np.array(image).shape
    h = int(shape[1] / 4)
    #print(shape)

    rgb, num = cal_percent(np.asarray(image))  #先将jpeg格式转换为位图形式
    print(num)
    img = Image.new('RGB', (shape[1], int(num / 4+ 1) * 40), (96, 96, 96)) #第二个参数为（宽，高）
    img2 = Image.new('RGB', (shape[1], int(num / 4 + 1) * 40 + shape[0]), (255, 255, 255))
    print(img2) 

    #绘制图例
    for i, k in enumerate(rgb):
        if i % 4 == 0:
            count1 = 0
        else: 
            count1 = count1 + 1
        text = k + '(' + rgb[k][0] + ')'
        rectangle = create_rectangle((h, 30), rgb[k][1], text, text_size)
        coordination = (count1 * h+10*(i%4), 10 + int(i / 4) * 40) #第二个参数为（宽，高）
        img.paste(rectangle, coordination)
    
    #image = Image.open('C:/Users/19215/Desktop/output1.jpg')  #重新导入，因为之前转换色素有所变动
    
    img2.paste(image1, (0, 0))
               
    img2.paste(img, (0, shape[0]))
    #plt.imshow(img2)  #在右侧绘制出处理后的图片
    return img2

color_label = ADE20k_labels.ade20K_color2label #颜色字典
color_list = list(color_label) #将上面颜色元组转换为颜色列表
#image = Image.open('C:/Users/19215/Desktop/output1.jpg')
#image = change_rgb(np.array(image),color_list,color_label) # 不管rgb在不在颜色字典里面，都转换成颜色字典里的rgb
#image = legend(image)
#imageio.imsave('C:/Users/19215/Desktop/Apps/out.jpg', image)


'''批量处理'''
ImageReadPath = 'D:/交运比赛/全景静态图/1_嘉定区/segmented/10_曹安公路/'  #读取路径
ImageSavePath = 'C:/Users/19215/Desktop/calculated/' #存储路径
filelist = os.listdir(ImageReadPath)
print(len(filelist))
#str = ImageReadPath+'/*.jpg'
#coll_read = io.ImageCollection(ImageReadPath)   #图片集合
#print(len(coll_read))
for img_name in filelist:
    img_path = ImageReadPath + img_name
    img = Image.open(img_path)
    image = change_rgb(np.array(img), color_list, color_label)
    image = legend(image,img)
    imageio.imsave(ImageSavePath+img_name,image)

