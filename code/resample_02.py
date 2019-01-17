# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/10/23 15:50'

import os
from osgeo import gdal

os.chdir(r'D:\osgeopy-data\Landsat\Washington')

in_ds = gdal.Open('nat_color.tif')
out_rows = int(in_ds.RasterYSize / 50)
out_columns = int(in_ds.RasterXSize / 50)
num_bands = in_ds.RasterCount

gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('nat_color_resampled.tif',
        out_columns, out_rows, num_bands)

out_ds.SetProjection(in_ds.GetProjection())
geotransform = list(in_ds.GetGeoTransform())
geotransform[1] *= 50
geotransform[5] *= 50
out_ds.SetGeoTransform(geotransform)

data = in_ds.ReadRaster(
    buf_xsize=out_columns, buf_ysize=out_rows)
out_ds.WriteRaster(0, 0, out_columns, out_rows, data)
out_ds.FlushCache()
for i in range(num_bands):
    out_ds.GetRasterBand(i + 1).ComputeStatistics(False)

out_ds.BuildOverviews('average', [2, 4, 8, 16])
del out_ds
