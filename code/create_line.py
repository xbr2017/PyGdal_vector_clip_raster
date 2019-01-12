# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/11/4 23:25'

from osgeo import ogr
import matplotlib.pyplot as plt

from ospybook.vectorplotter import VectorPlotter

line = ogr.Geometry(ogr.wkbLineString)  # 构建几何类型:线
line.AddPoint(54, 37)      # 添加点01
line.AddPoint(62, 35.5)    # 添加点02
line.AddPoint(70.5, 38)    # 添加点03
line.AddPoint(74.5, 41.5)  # 添加点04
# 调用VectorPlotter类
vp = VectorPlotter(True)
vp.plot(line, 'r-')

plt.show()   # 少了这句话则图像不显示
