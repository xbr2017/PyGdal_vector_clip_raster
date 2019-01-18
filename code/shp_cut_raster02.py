# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2019/1/2 18:06'

import operator
from osgeo import gdal, gdal_array, osr
import shapefile

try:
    import Image
    import ImageDraw
except:
    from PIL import Image, ImageDraw

# 用于裁剪的栅格数据
raster = r'D:\FalseColor.tif'
# 用于裁剪的多边形shp文件
shp = r'D:\hancock'
# 裁剪后的栅格数据
output = r'D:\clip'


def image2Array(i):
    """
    将一个Python图像库的数组转换为一个gdal_array图片
    """
    a = gdal_array.numpy.fromstring(i.tobytes(), 'b')
    a.shape = i.im.size[1], i.im.size[0]
    return a


def world2Pixel(geoMatrix, x, y):
    """
    使用GDAL库的geomatrix对象((gdal.GetGeoTransform()))计算地理坐标的像素位置
    """
    ulx = geoMatrix[0]
    uly = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int((x - ulx) / xDist)
    line = int((uly - y) / abs(yDist))
    return (pixel, line)

# 将数据源作为gdal_array载入
srcArray = gdal_array.LoadFile(raster)
# 同时载入gdal库的图片从而获取geotransform
srcImage = gdal.Open(raster)
geoTrans = srcImage.GetGeoTransform()
# 使用PyShp库打开shp文件
r = shapefile.Reader("{}.shp".format(shp))
# 将图层扩展转换为图片像素坐标
minX, minY, maxX, maxY = r.bbox
ulX, ulY = world2Pixel(geoTrans, minX, maxY)
lrX, lrY = world2Pixel(geoTrans, maxX, minY)
# 计算新图片的尺寸
pxWidth = int(lrX - ulX)
pxHeight = int(lrY - ulY)
clip = srcArray[:, ulY:lrY, ulX:lrX]
# 为图片创建一个新的geomatrix对象以便附加地理参照数据
geoTrans = list(geoTrans)
geoTrans[0] = minX
geoTrans[3] = maxY
# 在一个空白的8字节黑白掩膜图片上把点映射为像元绘制市县
# 边界线
pixels = []
for p in r.shape(0).points:
    pixels.append(world2Pixel(geoTrans, p[0], p[1]))
rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
# 使用PIL创建一个空白图片用于绘制多边形
rasterize = ImageDraw.Draw(rasterPoly)
rasterize.polygon(pixels, 0)
# 使用PIL图片转换为Numpy掩膜数组
mask = image2Array(rasterPoly)
# 根据掩膜图层对图像进行裁剪
clip = gdal_array.numpy.choose(mask, (clip, 0)).astype(gdal_array.numpy.uint8)
print clip.max()
# 将NDVI保存为tiff文件
gdal_array.SaveArray(clip, "{}.tif".format(output),
                     format="GTiff", prototype=raster)
