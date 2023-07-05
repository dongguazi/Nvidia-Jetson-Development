import torch
import pickle
import sys
import os
import cv2
import numpy as np
import os.path
import torch.utils.data as data
import torchvision.transforms as transforms
from PIL import Image
from xml.dom.minidom import Document
from tqdm import tqdm

#将高清图片，按照一定的宽高和步长进行切割出多个小图片，切割的同时对label进行判断处理，最后保存为新的iamge和label。
#切割后的图像大小可以按照对目标的检测框的大小进行统计得到，其次还要根据实际算力设备进行选择，较大的图片尺寸设备算力可能跟不上。
#xml的key要根据实际的xml文件进行改变，例如xml_ori.iter('object')  中的object。

if sys.version_info[0] ==2:
    import xml.etree.cElementTree as ET
else:
    import xml.etree.ElementTree as ET
origin_dir = '原图像存放地址'
target_dir1 = '分块图像存放地址'
annota_dir = '原boundingbox的xml文件存放地址'
target_dir2 = '分块boundingbox的xml文件存放地址'
def clip_img(No, oriname):
    from_name = os.path.join(origin_dir, oriname+'.jpg')
    img = cv2.imread(from_name)
    h_ori,w_ori, _ =img.shape#保存原图的大小
    img = cv2.resize(img, (2048, 2048))#可以resize也可以不resize，看情况而定
    h, w, _ = img.shape
    xml_name = os.path.join(annota_dir, oriname+'.xml')#读取每个原图像的xml文件
    xml_ori = ET.parse(xml_name).getroot()
    res = np.empty((0,5))#存放坐标的四个值和类别
    for obj in xml_ori.iter('object'):
        difficult = int(obj.find('difficult').text) == 1
        if difficult:
            continue
        name = obj.find('name').text.lower().strip()
        bbox = obj.find('bndbox')
        pts = ['xmin', 'ymin', 'xmax', 'ymax']
        bndbox = []
        for i, pt in enumerate(pts):
            cur_pt = int(bbox.find(pt).text) - 1
            cur_pt = int(cur_pt*h/h_ori) if i%2==1 else int(cur_pt * w / w_ori)
            bndbox.append(cur_pt)
        #label_idx = self.class_to_ind[name]
        bndbox.append(name)
        res = np.vstack((res, bndbox))
    i = 0
    win_size = 256#分块的大小
    stride = 128#重叠的大小，设置这个可以使分块有重叠
    for r in range(0, h - win_size, stride):
        for c in range(0, w - win_size, stride):
            flag = np.zeros([1,10])
            youwu = False
            xiefou = True
            tmp = img[r: r+win_size, c: c+win_size]
            for re in range(res.shape[0]):
                xmin,ymin,xmax,ymax,label = res[re]
                if int(xmin)>=c and int(xmax) <=c+win_size and int(ymin)>=r and int(ymax)<=r+win_size:
                    flag[0][re] = 1
                    youwu = True
                elif int(xmin)<c or int(xmax) >c+win_size or int(ymin) < r or int(ymax) > r+win_size:
                    pass
                else:
                    xiefou = False
                    break;
            if xiefou:#如果物体被分割了，则忽略不写入
                if youwu:#有物体则写入xml文件
                    doc = Document()
                    annotation = doc.createElement('annotation')
                    doc.appendChild(annotation)
                    for re in range(res.shape[0]):
                        xmin,ymin,xmax,ymax,label = res[re]
                        xmin=int(xmin)
                        ymin=int(ymin)
                        xmax=int(xmax)
                        ymax=int(ymax)
                        if flag[0][re] == 1:
                            xmin=str(xmin-c)
                            ymin=str(ymin-r)
                            xmax=str(xmax-c)
                            ymax=str(ymax-r)
                            object_charu = doc.createElement('object')
                            annotation.appendChild(object_charu)
                            name_charu = doc.createElement('name')
                            name_charu_text = doc.createTextNode(label)
                            name_charu.appendChild(name_charu_text)
                            object_charu.appendChild(name_charu)
                            dif = doc.createElement('difficult')
                            dif_text = doc.createTextNode('0')
                            dif.appendChild(dif_text)
                            object_charu.appendChild(dif)
                            bndbox = doc.createElement('bndbox')
                            object_charu.appendChild(bndbox)
                            xmin1 = doc.createElement('xmin')
                            xmin_text = doc.createTextNode(xmin)
                            xmin1.appendChild(xmin_text)
                            bndbox.appendChild(xmin1)
                            ymin1 = doc.createElement('ymin')
                            ymin_text = doc.createTextNode(ymin)
                            ymin1.appendChild(ymin_text)
                            bndbox.appendChild(ymin1)
                            xmax1 = doc.createElement('xmax')
                            xmax_text = doc.createTextNode(xmax)
                            xmax1.appendChild(xmax_text)
                            bndbox.appendChild(xmax1)
                            ymax1 = doc.createElement('ymax')
                            ymax_text = doc.createTextNode(ymax)
                            ymax1.appendChild(ymax_text)
                            bndbox.appendChild(ymax1)
                        else:
                            continue
                    xml_name = oriname+'_%3d.xml' % (i)
                    to_xml_name = os.path.join(target_dir2, xml_name)
                    with open(to_xml_name, 'wb+') as f:
                        f.write(doc.toprettyxml(indent="\t", encoding='utf-8'))
                    #name = '%02d_%02d_%02d_.bmp' % (No, int(r/win_size), int(c/win_size))
                    img_name = oriname+'_%3d.jpg' %(i)
                    to_name = os.path.join(target_dir1, img_name)
                    i = i+1
                    cv2.imwrite(to_name, tmp)


if __name__=="__main__":
    for No, name in tqdm(enumerate(os.listdir(origin_dir))):
        clip_img(No, name.rstrip('.jpg'))

