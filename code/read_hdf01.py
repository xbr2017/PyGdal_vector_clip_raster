# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2019/1/16 17:52'

import gdal, osr


def array2raster(newRasterfn,rasterOrigin, xsize, ysize, array):
    """
     newRasterfn: 输出tif路径
     rasterOrigin: 原始栅格数据路径
     xsize: x方向像元大小
     ysize: y方向像元大小
     array: 计算后的栅格数据
    """
    cols = array.shape[1]  #  矩阵列数
    rows = array.shape[0]  #  矩阵行数
    originX = rasterOrigin[0]  #  起始像元经度
    originY = rasterOrigin[1]  #  起始像元纬度
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    #  括号中两个0表示起始像元的行列号从(0,0)开始
    outRaster.SetGeoTransform((originX, xsize, 0, originY, 0, ysize))
    #  获取数据集第一个波段，是从1开始，不是从0开始
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    #  代码4326表示WGS84坐标
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


ds = gdal.Open('D:/osgeopy-data/Modis/MYD13Q1.A2014313.h20v11.005.2014330092746.hdf')

subdatasets = ds.GetSubDatasets()
print('Number of subdatasets: {}'.format(len(subdatasets)))
for sd in subdatasets:
    print('Name: {0}\nDescription:{1}\n'.format(*sd))

ndvi_ds = gdal.Open(subdatasets[0][0]).ReadAsArray()
dst_filename = "D:/nc/result.tif"
xsize = 0.0025
ysize = 0.0025

array2raster(dst_filename, [90,75], xsize,ysize, ndvi_ds)



