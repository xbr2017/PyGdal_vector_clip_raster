# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/11/26 22:40'


from osgeo import gdal

in_ds = gdal.Open('D:/MOD09A1.A2017361.h28v06.006.2018005034659.hdf')
# 返回结果是一个list，list中的每个元素是一个tuple，每个tuple中包含了对数据集的路径，元数据等的描述信息
# tuple中的第一个元素描述的是数据子集的全路径
datasets = in_ds.GetSubDatasets()

# 取出第1个数据子集（MODIS反射率产品的第一个波段）进行转换
# 第一个参数是输出数据，第二个参数是输入数据，后面可以跟多个可选项
gdal.Warp('D:/reprojection01.tif', datasets[0][0], dstSRS='EPSG:32649')  # UTM投影
gdal.Warp('D:/reprojection02.tif', datasets[0][0], dstSRS='EPSG:4326')   # 等经纬度投影

# 关闭数据集
root_ds = None
