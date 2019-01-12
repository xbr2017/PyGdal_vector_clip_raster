# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/11/4 23:17'

from osgeo import ogr
import matplotlib.pyplot as plt

from ospybook.vectorplotter import VectorPlotter


point = ogr.Geometry(ogr.wkbPoint)  # 构建几何类型:点
point.AddPoint(59.5, 11.5)          # 创建点01
x, y = point.GetX(), point.GetY()   # Python的任性赋值方式
# 调用VectorPlotter类
vp = VectorPlotter(True)
vp.plot(point, 'bo')      # 画出蓝色圆点
point.AddPoint(59.5, 13)  # 在点01基础上添加点02
vp.plot(point, 'rs')      # 画出红色方点

plt.show()   # 少了这句话则图像不显示