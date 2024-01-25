import os, re
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from time import strftime

import arcpy
from arcpy import env

import warnings
warnings.filterwarnings('ignore')

inspace = os.path.join(os.getcwd(), "data")
outspace = os.path.join(os.getcwd(), "out")

env.workspace = outspace
env.overwriteOutput = True

# if not os.path.exists(os.path.join(outspace, "Hysplit_sites.gdb")):
#     arcpy.management.CreateFileGDB(outspace, "Hysplit_sites")
# gdb_out = os.path.join(outspace, "Hysplit_sites.gdb")

for d in os.listdir(inspace):
    if os.path.isdir(os.path.join(inspace, d)):
        site = d
        site_dir = os.path.join(inspace, d)

        print('site: %s --> %s' % (site, strftime('%X')))

        all = pd.DataFrame(columns=['year','month', 'day','hour','y','x','z','P','id'])
        all_wet = pd.DataFrame(columns=['year','month', 'day','hour','y','x','z','P','id'])
        all_dry = pd.DataFrame(columns=['year','month', 'day','hour','y','x','z','P','id'])
        all_drought = pd.DataFrame(columns=['year','month', 'day','hour','y','x','z','P','id'])
        all_non_drought = pd.DataFrame(columns=['year','month', 'day','hour','y','x','z','P','id'])

        for f in os.listdir(site_dir):
            colnames = ['id1', 'id2', 'year','month', 'day','hour','min','sec','diff','y','x','z','P']
            
            f_csv = os.path.join(site_dir, f+'.csv')
            f_id = re.sub('\D', '', f)
            f_yr = int(f_id[:4])
            f_mn = int(f_id[4:6])
            f_dy = int(f_id[6:])

            with open(os.path.join(site_dir, f), 'r') as rl, open(f_csv, 'w') as wl:
                lines = rl.readlines()
                wl.writelines(lines[5:])
            
            df = pd.read_csv(f_csv, header=None, delim_whitespace=True, names=colnames)
            df = df.drop(columns=['id1','id2','diff','min','sec'])
            df['id'] = f_id

            all = pd.concat([all, df])
            if f_mn in [11,12,1,2,3,4,5,6]:
                all_wet = pd.concat([all_wet, df])
            elif f_mn in [7,8,9,10]:
                all_dry = pd.concat([all_dry, df])
            
            if f_yr in [2006,2010,2018]:
                all_drought = pd.concat([all_drought, df])
            else:
                all_non_drought = pd.concat([all_non_drought, df])

        print("Writing geometries... (%s)" % (strftime('%X')))
        all['geom'] = all.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
        all_wet['geom'] = all_wet.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
        all_dry['geom'] = all_dry.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
        all_drought['geom'] = all_drought.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
        all_non_drought['geom'] = all_non_drought.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)

        print("Writing geopandas df... (%s)" % strftime('%X'))
        shp_all = gpd.GeoDataFrame(all, geometry='geom')
        shp_wet = gpd.GeoDataFrame(all_wet, geometry='geom')
        shp_dry = gpd.GeoDataFrame(all_dry, geometry='geom')
        shp_drought = gpd.GeoDataFrame(all_drought, geometry='geom')
        shp_non_drought = gpd.GeoDataFrame(all_non_drought, geometry='geom')

        print("Writing to local files...  (%s)" % strftime('%X'))
        shp_all.to_file(os.path.join(outspace, site+"_all.shp"), driver='ESRI Shapefile', index=False)
        shp_wet.to_file(os.path.join(outspace, site+"_wet.shp"), driver='ESRI Shapefile', index=False)
        shp_dry.to_file(os.path.join(outspace, site+"_dry.shp"), driver='ESRI Shapefile', index=False)
        shp_drought.to_file(os.path.join(outspace, site+"_drought.shp"), driver='ESRI Shapefile', index=False)
        shp_non_drought.to_file(os.path.join(outspace, site+"_nondrought.shp"), driver='ESRI Shapefile', index=False)

        print("Writing to gdb...  (%s)" % strftime('%X'))
        arcpy.conversion.FeatureClassToGeodatabase([site+"_all.shp", site+"_wet.shp", site+"_dry.shp", site+"_drought.shp", site+"_nondrought.shp"], 
                                                   'Hysplit_sites.gdb')

        print("Done!\n")