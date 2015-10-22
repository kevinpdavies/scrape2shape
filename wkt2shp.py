#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Create shapefiles of indigenous language regions based on web page WKT
Copyright 2015 Dr. Kevin Davies <kpdavies@uni.sydney.edu.au>

"""
import glob
import iso19139gen.iso19139gen as iso19139gen
from os.path import basename, splitext
from osgeo import ogr, osr
import os

def get_wkt(f):
    
    with open(f) as h:
        for line in h:
            if "wkt" in line:
                first = line.split('"wkt":"')[1]
                wkt = first.split('","projection"')[0]
                return wkt

def line2poly(wkt):
    
    coords = wkt.strip('LINESTRING ').strip('(').strip(')')
    wkt = 'POLYGON((' + coords + ", " + coords.split(',')[0] + "))"

    return wkt
    
def createshp(shp_f):
    
    # Remove the file if it exists
    if os.path.isfile(shp_f):
        print("Removing {:}".format(shp_f))
        os.remove(shp_f)
    
    print("Creating {:}...".format(shp_f))
    
    # Create the ouput shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = driver.CreateDataSource(shp_f)
    
    # Create the projection file
    sr = osr.SpatialReference()
    sr.SetWellKnownGeogCS("EPSG:4326") 
    sr.MorphToESRI()
    with open(shp_f.replace(".shp", ".prj"), 'w') as sr_f:
        sr_f.write(sr.ExportToWkt())

    return ds
    
def createlayer(ds):
    
    layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('name', ogr.OFTString))

    return layer
    
def createfeature(layer, wkt, i, name):
    
    poly = ogr.CreateGeometryFromWkt(wkt)
    defn = layer.GetLayerDefn()
    feat = ogr.Feature(defn)
    feat.SetField('id', i)
    feat.SetField('name', name)
    feat.SetGeometry(poly)
    layer.CreateFeature(feat)
    return
    
def plot(shp_f = '../data/indiglang.shp'):
    
    # Print out a map if needbe
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    
    map = Basemap(llcrnrlon=105,llcrnrlat=-45,urcrnrlon=155,urcrnrlat=-8,
                resolution='i', projection='tmerc', lat_0 = -28, lon_0 = 130)
    
    #map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='#ddaa66',lake_color='aqua')
    #map.drawcoastlines()
    
    map.readshapefile(shp_f.replace(".shp", ""), 'test')
    
    plt.show()

if __name__ == "__main__":
    
    # Metadata base title
    title = 'Indigenous Language Region'
    
    # Create global shapefile
    gshp_f = '../data/indiglang.shp'
    gds = createshp(gshp_f)
    glayer = createlayer(gds)
    
    # Get a list of files to process
    files = glob.glob('../data/www/*.txt')
    for i, f in enumerate(files):
    
        print("Processing {:}".format(f))
        
        # Get wkt from the www file. The tassie one is a LINESTRING so fix.
        wkt = get_wkt(f)
        if 'LINESTRING' in wkt:
            wkt = line2poly(wkt)

        # Create feature in global shapefile
        name = splitext(basename(f))[0]
        name = name[:-2] if name.endswith('-0') else name # Get rid of '-0'
        createfeature(glayer, wkt, i, name.title())
    
        # Create feature in a local shapefile and close
        lshp_f = gshp_f.replace(".shp", "_{:}.shp".format(name))
        lds = createshp(lshp_f)
        llayer = createlayer(lds)
        createfeature(llayer, wkt, i, name.title())
        lds = llayer = None
        
        # Create metadata
        ltitle = title + " - " + name.title()
        xml_f = lshp_f + ".xml"
        iso19139gen.go("IndigLangTemplate.xml", lshp_f, xml_f, title=ltitle)
    
    # Close the global shapefile
    gds = glayer = None
    
    # Create global metadata
    xml_f = gshp_f + ".xml"
    iso19139gen.go("IndigLangTemplate.xml", gshp_f, xml_f, title=title)
    
    print("Finished")