import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
 
# 数据标签
classes = ['胶塞','推杆尾部','针尾部','嘴','歪嘴','螺口','小胶塞'] #需要修改
 
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    if w>=1:
        w=0.99
    if h>=1:
        h=0.99
    return (x,y,w,h)
 
def convert_annotation(rootpath,xmlname,mode):
    xmlpath = rootpath + '/Marked'
    xmlfile = os.path.join(xmlpath,xmlname)
    with open(xmlfile, "r", encoding='UTF-8') as in_file:
      txtname = xmlname[:-4]+'.txt'
      print(txtname)

      txtpath = rootpath +'/labels'  #生成的.txt文件会被保存在labels目录下
      
      if not os.path.exists(txtpath):
        os.makedirs(txtpath)
      txtfile = os.path.join(txtpath,txtname)
      with open(txtfile, "w+" ,encoding='UTF-8') as out_file:
        tree=ET.parse(in_file)
        root = tree.getroot()
        print(root)
        #labels = root.find('Labels')
        #w = int(labels.find('width').text)
        #h = int(labels.find('height').text)
        w=3072.0
        h=2048.0
        out_file.truncate()
        for obj in root.iter('Label'):

            cls = obj.find('Category')
            if cls==None:
                continue
            if cls not in classes ==1:
                continue

            cls=cls.text
            cls_id = classes.index(cls)
            xmlbox = obj.find('Bndbox')
            box = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bbox = convert((w,h), box)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bbox]) + '\n')
 
 
if __name__ == "__main__":
    rootpath='/home/donggua/文档/datasets/点键金塔50mL目标检测小胶塞/val'  ##需要修改的地方改成你的路径
    xmlpath=rootpath+'/Marked'##这就是xml的路径
    list=os.listdir(xmlpath)
    mode="train"
    for i in range(0,len(list)) :
        path = os.path.join(xmlpath,list[i])
        if ('.xml' in path)or('.XML' in path):
            convert_annotation(rootpath,list[i],mode)
            print('done', i)
        else:
            print('not xml file',i)