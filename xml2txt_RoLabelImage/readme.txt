### 1.roLabelImage标注带旋转目标的标注文件：

roLabelImage标注后的原格式：
<annotation verified="no">
<folder>images</folder>
<filename>20221110152509911</filename>
<path>/home/donggua/下载/baolong/images/20221110152509911.jpg</path>
<source>
<database>Unknown</database>
</source>
<size>
<width>1856</width>
<height>1184</height>
<depth>3</depth>
</size>
<segmented>0</segmented>
<object>
<type>robndbox</type>
<name>X</name>
<pose>Unspecified</pose>
<truncated>0</truncated>
<difficult>0</difficult>
<robndbox>
<cx>1177.8051</cx>
<cy>447.7748</cy>
<w>76.3248</w>
<h>93.2381</h>
<angle>1.294981</angle>
</robndbox>
</object>
</annotation>


转化后的格式：【x1,y1,x2,y2,x3,y3,x4,y4,calssName,difficult】前8个坐标依次为矩形框四个顶点的xy坐标
1212.3 398.4 1233.1 471.8 1122.6 423.8 1143.3 497.2 X 0