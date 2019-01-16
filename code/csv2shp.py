# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/11/12 11:51'

from osgeo import ogr, osr

# 动物的GPS数据
csv_fn = r"D:\osgeopy-data\Galapagos\Galapagos Albatrosses.csv"
# 先定义好即将输出的shp文件
shp_fn = r"D:\osgeopy-data\Galapagos\albatross_dd.shp"
# 定义为WGS84坐标系
sr = osr.SpatialReference(osr.SRS_WKT_WGS84)

# 获取驱动程序对象
shp_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(shp_fn)
# 创建矢量点图层
shp_lyr = shp_ds.CreateLayer('albatross_dd', sr, ogr.wkbPoint)
# 添加属性字段：tag_id
shp_lyr.CreateField(ogr.FieldDefn('tag_id', ogr.OFTString))
# 添加属性字段：timestamp
shp_lyr.CreateField(ogr.FieldDefn('timestamp', ogr.OFTString))
# 创建空白特征，方便后面存储
shp_row = ogr.Feature(shp_lyr.GetLayerDefn())

csv_ds = ogr.Open(csv_fn)
csv_lyr = csv_ds.GetLayer()
# 主要实现将逐个CSV中的点存储到shp中
for csv_row in csv_lyr:
    x = csv_row.GetFieldAsDouble('location-long')
    y = csv_row.GetFieldAsDouble('location-lat')
    # 创建几何点
    shp_pt = ogr.Geometry(ogr.wkbPoint)
    # 添加点
    shp_pt.AddPoint(x, y)
    tag_id = csv_row.GetField('individual-local-identifier')
    timestamp = csv_row.GetField('timestamp')
    # 添加点以及对应的属性tag_id和timestamp
    shp_row.SetGeometry(shp_pt)
    shp_row.SetField('tag_id', tag_id)
    shp_row.SetField('timestamp', timestamp)
    # 生成特征
    shp_lyr.CreateFeature(shp_row)

del csv_ds, shp_ds
