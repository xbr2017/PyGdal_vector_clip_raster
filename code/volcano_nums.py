# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/11/6 12:17'

from osgeo import ogr

shp_ds = ogr.Open(r'D:\osgeopy-data\US')
volcano_lyr = shp_ds.GetLayer('us_volcanos_albers')  # 火山矢量数据
cities_lyr = shp_ds.GetLayer('cities_albers')  # 城市矢量数据
memory_driver = ogr.GetDriverByName('memory')
memory_ds = memory_driver.CreateDataSource('temp')
buff_lyr = memory_ds.CreateLayer('buffer')  # 创建缓冲区
buff_feat = ogr.Feature(buff_lyr.GetLayerDefn())
for volcano_feat in volcano_lyr:
    buff_geom = volcano_feat.geometry().Buffer(15000)  # 建立15KM的缓冲区
    tmp = buff_feat.SetGeometry(buff_geom)
    tmp = buff_lyr.CreateFeature(buff_feat)

result_lyr = memory_ds.CreateLayer('result')
# 将火山点与城市矢量进行重叠
buff_lyr.Intersection(cities_lyr, result_lyr)
# 统计15KM内城市的个数
print('Cities: {}'.format(result_lyr.GetFeatureCount()))

