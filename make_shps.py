import os
import re
# from datetime import datetime
import geopandas as gpd


inspace = os.path.join(os.getcwd(), "data")

known_issues = ["BR_17","Rurop"]

yrs = range(2000,2021,1)
yrs= ["{:04d}".format(x) for x in yrs]

'''     ALL POINTS      '''

for d in os.listdir(inspace):
    site = d
    site_dir = os.path.join(inspace,d)

    if site not in known_issues:
        for f in os.listdir(site_dir):
            f_name = re.match("^(\D*)(\d{8})$", f)

            site_name = f_name.group(1)
            site_date = f_name.group(2)
