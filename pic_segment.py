# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 16:12:01 2021

@author: 19215
"""


#import pixellib
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from pixellib.semantic import semantic_segmentation
#segment_image = semantic_segmentation()
#segment_image.load_ade20k_model("deeplabv3_xception65_ade20k.h5")
#segment_image.segmentAsAde20k("C:/Users/19215/Desktop/1.jpg", output_image_name= "C:/Users/19215/Desktop/output2.jpg")



'''批量处理''' 
ImageReadPath = 'D:/交运比赛/全景静态图/1_嘉定区/10_曹安公路/'  #读取路径
ImageSavePath = 'C:/Users/19215/Desktop/segment/' #存储路径
filelist = os.listdir(ImageReadPath)
print(len(filelist))

for img_name in filelist:
    img_path = ImageReadPath + img_name
    out_path = ImageSavePath + img_name    
    print(img_path)
    print(out_path)
    segment_image = semantic_segmentation()
    segment_image.load_ade20k_model("deeplabv3_xception65_ade20k.h5")
    segment_image.segmentAsAde20k(img_path, output_image_name = out_path)
    