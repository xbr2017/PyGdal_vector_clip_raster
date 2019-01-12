# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/11/4 23:33'

from osgeo import ogr
import matplotlib.pyplot as plt

from ospybook.vectorplotter import VectorPlotter

ring = ogr.Geometry(ogr.wkbLinearRing)  # 构建几何类型:线
ring.AddPoint(58, 38.5)  # 添加点01
ring.AddPoint(53, 6)     # 添加点02
ring.AddPoint(99.5, 19)  # 添加点03
ring.AddPoint(73, 42)    # 添加点04
yard = ogr.Geometry(ogr.wkbPolygon)  # 构建几何类型:多边形
yard.AddGeometry(ring)
yard.CloseRings()
# 调用VectorPlotter类
vp = VectorPlotter(True)
vp.plot(yard, fill=False, edgecolor='blue')
ring = yard.GetGeometryRef(0)
for i in range(ring.GetPointCount()):
    ring.SetPoint(i, ring.GetX(i) - 5, ring.GetY(i))
vp.plot(yard, fill=False, ec='red', linestyle='dashed')
plt.show()   # 少了这句话则图像不显示