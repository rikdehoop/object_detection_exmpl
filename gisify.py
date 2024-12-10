from osgeo import osr, ogr, gdal
import os
from shapely.geometry import mapping, Polygon
from shapely.ops import unary_union
import fiona
import geopandas as gpd
path_to_main_folder = input('path to the main folder where a folder images and a folder labels are stored: ')
path_to_store_geodata = input('path to store georeference data: ')
input('name the folder for labels "labels" and the folder for images "images", Let"s continue:  CLICK ENTER')

cnt = 0
polylist = []
confv = []

def pixel_to_world(geo_matrix, x, y):
    ul_x = geo_matrix[0]
    ul_y = geo_matrix[3]
    x_dist = geo_matrix[1]
    y_dist = geo_matrix[5]
    _x = x * x_dist + ul_x
    _y = y * y_dist + ul_y
    return _x, _y


SCREEN_DIMENSIONS = (1280, 1280)
def xywh2xyxy_(x,y,w,h):
        x1, y1 = x-w/2, y-h/2
        x2, y2 = x+w/2, y+h/2
        return x1, y1, x2, y2

def xyxy2pixel_(coords):
    return tuple(round(coord * dimension) for coord, dimension in zip(coords, SCREEN_DIMENSIONS))
TEST_ANNO = path_to_main_folder
for i in os.listdir(TEST_ANNO):
    file_name, file_extension = os.path.splitext(i)
    with open((rf"{TEST_ANNO}//labels//"+file_name+".txt"), "r") as test_txt:
        for line in test_txt:
            test_txt = line.split(" ")
            
            if int(test_txt[0])==0:

                xyxy = xywh2xyxy_(float(test_txt[1]),float(test_txt[2]),float(test_txt[3]),float(test_txt[4]))
                XminYmin = (xyxy[0],xyxy[1])
                XmaxYmax= (xyxy[2],xyxy[3])

                XminYmax = (xyxy[0],xyxy[3])
                XmaxYmin = (xyxy[2],xyxy[1])


    # convert xyxy coords to pixel values:
                # xmin=(xyxy2pixel_(XminYmin)[0])
                # ymin=(xyxy2pixel_(XminYmin)[1])
                # xmax=(xyxy2pixel_(XmaxYmax)[0])
                # ymax=(xyxy2pixel_(XmaxYmax)[1])
                


                ds = gdal.Open(rf"{TEST_ANNO}//images//" + file_name + ".tif")

                world_Xmin, world_Ymin = pixel_to_world(ds.GetGeoTransform(), xyxy[0], xyxy[1])
                world_Xmax, world_Ymax = pixel_to_world(ds.GetGeoTransform(), xyxy[2], xyxy[3])
                world_Xmin, world_Ymax = pixel_to_world(ds.GetGeoTransform(), xyxy[0], xyxy[3])
                world_Xmax, world_Ymin = pixel_to_world(ds.GetGeoTransform(), xyxy[2], xyxy[1])

                coord1 = (world_Xmax, world_Ymax)
                coord2 = (world_Xmax, world_Ymin)
                coord3 = (world_Xmin, world_Ymin)
                coord4 = (world_Xmin, world_Ymax)

                poly = Polygon([coord1, coord2, coord3, coord4])
                polylist.append(poly)
                confv.append(float(test_txt[5]))
                print(len(polylist)," ",len(confv))
                # Define a polygon feature geometry with one attribute
    
    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int',
                       'confv':'float'},
    }

    # Write a new Shapefile
    
    with fiona.open(f'{path_to_store_geodata}//square_bbxs_turb2_conf.shp', 'w', 'ESRI Shapefile', schema) as c:
        ## If there are multiple geometries, put the "for" loop here
        for i, cnf in zip(polylist, confv):
            cnt+=1
            c.write({
                'geometry': mapping(i),
                'properties': {'id': cnt,
                               'confv': cnf},
            })

    
    # GeoDataFrame creation
    poly = gpd.read_file(f"{path_to_store_geodata}//square_bbxs_poly.shp")
    points = poly.copy()
    points.geometry = points['geometry'].centroid
    # same crs
    points.crs=poly.crs
    # save the shapefile
    points.to_file(f'{path_to_store_geodata}//bbxs_centroid_pnt.shp')


    