#----------------------- import libraries

import os
import re
import glob
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from time import strftime

import arcpy
from arcpy import env

import warnings
warnings.filterwarnings('ignore')

# -------------------- user input
inspace = os.path.join(os.getcwd(), "data") # <-- directory that holds subdirectories of sites
outspace = os.path.join(os.getcwd(), "out") # <-- where intermediate shapefiles and geodatabase live

skipSites = [] # <-- string list of subdirectory names that should be skipped
overwrite = False # <-- should existing files be overwritten? yes= True, no= False

# -------------------- rest of the script
env.workspace = outspace
env.overwriteOutput = True

def writeOverwrite(input_path):
    if os.path.exists(input_path):
        return overwrite
    else:
        return True

if not os.path.exists(os.path.join(outspace, "Hysplit_sites.gdb")):
    arcpy.management.CreateFileGDB(outspace, "Hysplit_sites")

for d in os.listdir(inspace):
    if os.path.isdir(os.path.join(inspace, d)) and d not in skipSites:

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
            f_yr = int(f_id[-8:-4])
            f_mn = int(f_id[-4:-2])
            f_dy = int(f_id[-2:])

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

        files_to_gdb = []

        if writeOverwrite(os.path.join(outspace, site+"_all.shp")):
            print("Writing 'all' geometries... (%s)" % (strftime('%X')))
            all['geom'] = all.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
            print("Writing 'all' geopandas df... (%s)" % strftime('%X'))
            shp_all = gpd.GeoDataFrame(all, geometry='geom', crs='EPSG:4326')
            print("Writing 'all' to local files...  (%s)" % strftime('%X'))
            shp_all.to_file(os.path.join(outspace, site+"_all.shp"), driver='ESRI Shapefile', index=False)
            files_to_gdb.append(site+"_all.shp")

        if writeOverwrite(os.path.join(outspace, site+"_wet.shp")):
            print("Writing 'wet' geometries... (%s)" % (strftime('%X')))
            all_wet['geom'] = all_wet.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
            print("Writing 'wet' geopandas df... (%s)" % strftime('%X'))
            shp_wet = gpd.GeoDataFrame(all_wet, geometry='geom', crs='EPSG:4326')
            print("Writing 'wet' to local files...  (%s)" % strftime('%X'))
            shp_wet.to_file(os.path.join(outspace, site+"_wet.shp"), driver='ESRI Shapefile', index=False)
            files_to_gdb.append(site+"_wet.shp")

        if writeOverwrite(os.path.join(outspace, site+"_dry.shp")):
            print("Writing 'dry' geometries... (%s)" % (strftime('%X')))
            all_dry['geom'] = all_dry.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
            print("Writing 'dry' geopandas df... (%s)" % strftime('%X'))
            shp_dry = gpd.GeoDataFrame(all_dry, geometry='geom', crs='EPSG:4326')
            print("Writing 'dry' to local files...  (%s)" % strftime('%X'))
            shp_dry.to_file(os.path.join(outspace, site+"_dry.shp"), driver='ESRI Shapefile', index=False)
            files_to_gdb.append(site+"_dry.shp")

        if writeOverwrite(os.path.join(outspace, site+"_drought.shp")):
            print("Writing 'drought' geometries... (%s)" % (strftime('%X')))
            all_drought['geom'] = all_drought.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
            print("Writing 'drought' geopandas df... (%s)" % strftime('%X'))
            shp_drought = gpd.GeoDataFrame(all_drought, geometry='geom', crs='EPSG:4326')
            print("Writing 'drought' to local files...  (%s)" % strftime('%X'))
            shp_drought.to_file(os.path.join(outspace, site+"_drought.shp"), driver='ESRI Shapefile', index=False)
            files_to_gdb.append(site+"_drought.shp")

        if writeOverwrite(os.path.join(outspace, site+"_nondrought.shp")):
            print("Writing 'nondrought' geometries... (%s)" % (strftime('%X')))
            all_non_drought['geom'] = all_non_drought.apply(lambda rec: Point((float(rec.x), float(rec.y))), axis=1)
            print("Writing 'nondrought' geopandas df... (%s)" % strftime('%X'))
            shp_non_drought = gpd.GeoDataFrame(all_non_drought, geometry='geom', crs='EPSG:4326')
            print("Writing 'nondrought' to local files...  (%s)" % strftime('%X'))
            shp_non_drought.to_file(os.path.join(outspace, site+"_nondrought.shp"), driver='ESRI Shapefile', index=False)
            files_to_gdb.append(site+"_nondrought.shp")

        print("Writing to gdb...  (%s)" % strftime('%X'))
        arcpy.conversion.FeatureClassToGeodatabase([site+"_all.shp", site+"_wet.shp", site+"_dry.shp", site+"_drought.shp", site+"_nondrought.shp"], 
                                                'Hysplit_sites.gdb')
        
        csv_files = glob.glob(site_dir, "*.csv")
        for c in csv_files:
            os.remove(c)

        print("Done!\n")
