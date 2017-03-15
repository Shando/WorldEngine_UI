try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    try:
        import gdal
    except ImportError:
        print("Unable to load GDAL support, no heightmap export possible.")

import tempfile
import numpy
import os
import sys


'''
Whenever a GDAL short-format (http://www.gdal.org/formats_list.html) is given
and a unique mapping to a file suffix exists, it is looked up in gdal_mapper.

Trivial ones (i.e. a call to lower() does the job) are not handled:
   BAG, BMP, BT, ECW, ERS, FITS, GIF, GTA, PNG, RIK, VRT, XPM

All other formats (>100) currently end up with their respective GDAL short-format
converted to lower-case and might need to be renamed by the user.
'''
gdal_mapper = {  # TODO: Find a way to make GDAL provide this mapping.
    "aig": "adf",
    "bsb": "kap",
    "doq1": "doq",
    "doq2": "doq",
    "esat": "n1",
    "grib": "grb",
    "gtiff": "tif",
    "hfa": "img",
    "jdem": "mem",
    "jpeg": "jpg",
    "msgn": "nat",
    "terragen": "ter",
    "usgsdem": "dem",
}


def export(world, export_filetype='GTiff', export_datatype='float32', export_dimensions='None',
           export_normalise='None', export_subset='None', resample_alg='CubicSpline', path='seed_output'):
    try:
        gdal
    except NameError:
        print ("Cannot export: please install pygdal.")
        sys.exit(1)

    gdal.AllRegister()

#    for i in range(1, gdal.GetDriverCount()):
#        drv = gdal.GetDriver(i)
#        sTmp = drv.GetDescription()
#        print (sTmp)
    
    final_driver = gdal.GetDriverByName(str(export_filetype))
    
    # metadata = final_driver.GetMetadata()
    
    # if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
    #     print ('Driver %s supports Create() method.' % final_driver)
    
    # if metadata.has_key(gdal.DCAP_CREATECOPY) and metadata[gdal.DCAP_CREATECOPY] == 'YES':
    #     print ('Driver %s supports CreateCopy() method.' % final_driver)

    if final_driver is None:
        print ("%s driver not registered." % export_filetype)
        sys.exit(1)

    # try to find the proper file-suffix
    export_file = str(export_filetype)
    export_file = export_file.lower()

    if export_file in gdal_mapper:
        export_file = gdal_mapper[export_file]

    # Note: GDAL will throw informative errors on its own whenever file type and data type cannot be matched.
    # translate export_datatype; http://www.gdal.org/gdal_8h.html#a22e22ce0a55036a96f652765793fb7a4
    export_data = str(export_datatype)
    export_data = export_data.lower()

    if export_data in ['gdt_byte', 'uint8', 'int8', 'byte', 'char']:  # GDAL does not support int8
        bpp = 8
        numpy_type = numpy.uint8
        gdal_type = gdal.GDT_Byte
    elif export_data in ['gdt_uint16', 'uint16']:
        bpp = 16
        numpy_type = numpy.uint16
        gdal_type = gdal.GDT_UInt16
    elif export_data in ['gdt_uint32', 'uint32']:
        bpp = 32
        numpy_type = numpy.uint32
        gdal_type = gdal.GDT_UInt32
    elif export_data in ['gdt_int16', 'int16']:
        bpp = 64
        numpy_type = numpy.int16
        gdal_type = gdal.GDT_Int16
    elif export_data in ['gdt_int32', 'int32', 'int']:  # fallback for 'int'
        bpp = 32
        numpy_type = numpy.int32
        gdal_type = gdal.GDT_Int32
    elif export_data in ['gdt_float32', 'float32', 'float']:  # fallback for 'float'
        bpp = 32
        numpy_type = numpy.float32
        gdal_type = gdal.GDT_Float32
    elif export_data in ['gdt_float64', 'float64']:
        bpp = 64
        numpy_type = numpy.float64
        gdal_type = gdal.GDT_Float64
    else:
        raise TypeError("Type of data not recognized or not supported by GDAL: %s" % export_datatype)

    # massage data to scale between the absolute min and max
    elevation = numpy.copy(world.layers['elevation'].data)

    # round data (integer-types only)
    if numpy_type != numpy.float32 and numpy_type != numpy.float64:
        elevation = elevation.round()

    # switch to final data type; no rounding performed
    elevation = elevation.astype(numpy_type)

    # take elevation data and push it into an intermediate ENVI format,
    # some formats don't support being written by Create()
    inter_driver = gdal.GetDriverByName("ENVI")
    fh_inter_file, inter_file = tempfile.mkstemp()  # returns: (file-handle, absolute path)
    intermediate_ds = inter_driver.Create(inter_file, world.width, world.height, 1, gdal_type)

    band = intermediate_ds.GetRasterBand(1)
    band.WriteArray(elevation)
    band = None  # dereference band

    intermediate_ds = None  # save/flush and close

    # take the intermediate ENVI format and convert to final format
    intermediate_ds = gdal.Open(inter_file)

    # For more information about gdal_translate
    #  https://svn.osgeo.org/gdal/trunk/autotest/utilities/test_gdal_translate_lib.py
    #  https://github.com/dezhin/pygdal/blob/master/2.1.2/osgeo/gdal.py
    # re-size, normalize and blend if necessary
    width = height = None

    if export_dimensions is not None:
        width, height = export_dimensions

    # normalize data-set to the min/max allowed by data-type, typical for 8bpp
    scale_param = None

    if export_normalise is not None:
        min_norm, max_norm = export_normalise
        scale_param = [[elevation.min(), elevation.max(), min_norm, max_norm]]

    export_resample = gdal.GRA_CubicSpline

    # apply changes to the dataset
    if export_dimensions or export_normalise:
        if resample_alg == 'CubicSpline':
            pass
        elif resample_alg == 'NearestNeighbour':
            export_resample = gdal.GRA_NearestNeighbour
        elif resample_alg == 'Bilinear':
            export_resample = gdal.GRA_Bilinear
        elif resample_alg == 'Cubic':
            export_resample = gdal.GRA_Cubic
        elif resample_alg == 'Lanczos':
            export_resample = gdal.GRA_Lanczos
        elif resample_alg == 'Average':
            export_resample = gdal.GRA_Average
        else:
            export_resample = gdal.GRA_Mode

        intermediate_ds = gdal.Translate('', intermediate_ds, format='MEM', width=width, height=height,
                                         scaleParams=scale_param, resampleAlg=export_resample)

    # only use a specific subset of dataset
    if export_subset is not None:
        intermediate_ds = gdal.Translate('', intermediate_ds, format='MEM', srcWin=export_subset)

    final_driver.CreateCopy('%s-%d.%s' % (path, bpp, export_file), intermediate_ds)

    intermediate_ds = None  # dereference

    os.close(fh_inter_file)
    os.remove(inter_file)
