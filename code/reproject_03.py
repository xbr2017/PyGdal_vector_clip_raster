# _*_ coding: utf-8 _*_
__author__ = 'xbr'
__date__ = '2018/11/26 22:45'


from osgeo import gdal
from osgeo import osr

# root_ds = gdal.Open('/Users/tanzhenyu/Resources/DataWare/MODIS/MOD09A1.A2017361.h28v06.006.2018005034659.hdf')
# # 返回结果是一个list，list中的每个元素是一个tuple，每个tuple中包含了对数据集的路径，元数据等的描述信息
# # tuple中的第一个元素描述的是数据子集的全路径
# ds_list = root_ds.GetSubDatasets()
#
# # 取出第1个数据子集（MODIS反射率产品的第一个波段）进行转换
# # 第一个参数是输出数据，第二个参数是输入数据，后面可以跟多个可选项
# gdal.Warp('reprojection.tif', ds_list[0][0], dstSRS='EPSG:32649')
#
# # 关闭数据集
# root_ds = None


def reproject(src_file, dst_file, p_width, p_height, epsg_to):
    """
    :param src_file: 输入文件
    :param dst_file: 输出文件
    :param p_width: 输出图像像素宽度
    :param p_height: 输出图像像素高度
    :param epsg_to: 输出图像EPSG坐标代码
    :return:
    """
    # 首先，读取输入数据，然后获得输入数据的投影，放射变换参数，以及图像宽高等信息
    src_ds = gdal.Open(src_file)
    src_srs = osr.SpatialReference()
    src_srs.ImportFromWkt(src_ds.GetProjection())

    srs_trans = src_ds.GetGeoTransform()
    x_size = src_ds.RasterXSize
    y_size = src_ds.RasterYSize
    d_type = src_ds.GetRasterBand(1).DataType

    # 获得输出数据的投影，建立两个投影直接的转换关系
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(epsg_to)
    tx = osr.CoordinateTransformation(src_srs, dst_srs)

    # 计算输出图像四个角点的坐标
    (ulx, uly, _) = tx.TransformPoint(srs_trans[0], srs_trans[3])
    (urx, ury, _) = tx.TransformPoint(srs_trans[0] + srs_trans[1] * x_size, srs_trans[3])
    (llx, lly, _) = tx.TransformPoint(srs_trans[0], srs_trans[3] + srs_trans[5] * y_size)
    (lrx, lry, _) = tx.TransformPoint(srs_trans[0] + srs_trans[1] * x_size + srs_trans[2] * y_size,
                                      srs_trans[3] + srs_trans[4] * x_size + srs_trans[5] * y_size)

    min_x = min(ulx, urx, llx, lrx)
    max_x = max(ulx, urx, llx, lrx)
    min_y = min(uly, ury, lly, lry)
    max_y = max(uly, ury, lly, lry)

    # 创建输出图像，需要计算输出图像的尺寸（重投影以后图像的尺寸会发生变化）
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(dst_file,
                           int((max_x - min_x) / p_width),
                           int((max_y - min_y) / p_height),
                           1, d_type)
    dst_trans = (min_x, p_width, srs_trans[2],
                 max_y, srs_trans[4], -p_height)

    # 设置GeoTransform和Projection信息
    dst_ds.SetGeoTransform(dst_trans)
    dst_ds.SetProjection(dst_srs.ExportToWkt())
    # 进行投影转换
    gdal.ReprojectImage(src_ds, dst_ds,
                        src_srs.ExportToWkt(), dst_srs.ExportToWkt(),
                        gdal.GRA_Bilinear)
    dst_ds.GetRasterBand(1).SetNoDataValue(0)  # 设置NoData值
    dst_ds.FlushCache()

    del src_ds
    del dst_ds


if __name__ == '__main__':
    # 需要修改的地方
    src_file = 'HDF4_EOS:EOS_GRID:"MOD09A1.A2017361.h28v06.006.2018005034659.hdf":MOD_Grid_500m_Surface_Reflectance:sur_refl_b01'
    dst_file = 'reprojection.tif'
    reproject(src_file, dst_file, 0.002983, 0.002983, 4326)
