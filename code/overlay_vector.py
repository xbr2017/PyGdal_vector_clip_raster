# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/11/5 11:45'

from osgeo import ogr
import matplotlib.pyplot as plt

from ospybook.vectorplotter import VectorPlotter

water_ds = ogr.Open(r'D:\osgeopy-data\US\wtrbdyp010.shp')
water_lyr = water_ds.GetLayer(0)
water_lyr.SetAttributeFilter('WaterbdyID = 1011327')
marsh_feat = water_lyr.GetNextFeature()
marsh_geom = marsh_feat.geometry().Clone()
# 调用VectorPlotter类
vp = VectorPlotter(True)
vp.plot(marsh_geom, 'b')

nola_ds = ogr.Open(r'D:\osgeopy-data\Louisiana\NOLA.shp')
nola_lyr = nola_ds.GetLayer(0)
nola_feat = nola_lyr.GetNextFeature()
nola_geom = nola_feat.geometry().Clone()
vp.plot(nola_geom, fill=False, ec='red', ls='dashed', lw=3)

intersection = marsh_geom.Intersection (nola_geom)
vp.plot(intersection, 'yellow', hatch='x')

plt.show()   # 少了这句话则图像不显示

water_lyr.SetAttributeFilter("Feature != 'Lake'")
water_lyr.SetSpatialFilter(nola_geom)
wetlands_area = 0
for feat in water_lyr:
    intersect = feat.geometry().Intersection (nola_geom)
    wetlands_area += intersect.GetArea()

pcnt = wetlands_area / nola_geom.GetArea()

print(u'重叠面积所占比为{:.1%}'.format(pcnt))
