# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/12/10 11:41'

import os, sys, gdal
from gdalconst import *
import glob


def get_extent(fn):
    ds = gdal.Open(fn)
    rows = ds.RasterYSize
    cols = ds.RasterXSize
    # 获取图像角点坐标
    gt = ds.GetGeoTransform()
    minx = gt[0]
    maxy = gt[3]
    maxx = gt[0] + gt[1] * rows
    miny = gt[3] + gt[5] * cols
    return (minx, maxy, maxx, miny)


os.chdir('D:\MODIS-data')
in_files = glob.glob('*.tif')
# 通过两两比较大小,将最终符合条件的四个角点坐标保存，
# 即为拼接图像的四个角点坐标
minX, maxY, maxX, minY = get_extent(in_files[0])
for fn in in_files[1:]:
    minx, maxy, maxx, miny = get_extent(fn)
    minX = min(minX, minx)
    maxY = max(maxY, maxy)
    maxX = max(maxX, maxx)
    minY = min(minY, miny)

# 获取输出图像的行列数
in_ds = gdal.Open(in_files[0])
gt = in_ds.GetGeoTransform()
rows = int(maxX - minX) / abs(gt[5])
cols = int(maxY - maxy) / gt[1]

# 创建输出图像
driver = gdal.GetDriverByName('gtiff')
out_ds = driver.Create('mosaic.tif', cols, rows)
out_ds.SetProjection(in_ds.GetProjection())
out_band = out_ds.GetRasterBand(1)

gt = list(in_ds.GetGeoTransform())
gt[0], gt[3] = minX, maxY
out_ds.SetGeoTransform(gt)

for fn in in_files:
    in_ds = gdal.Open(fn)
    trans = gdal.Transformer(in_ds, out_ds, [])
    success, xyz = trans.TransformPoint(False, 0, 0)
    x, y, z = map(int, xyz)
    data = in_ds.GetRasterBand(1).ReadAsArray()
    out_band.WriteArray(data, x, y)

del in_ds, out_band, out_ds