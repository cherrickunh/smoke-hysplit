# Convert HYSPLIT trajectories to GDB Feature Classes

Author: <br>
<ul style="list-style-type: none;">
		Chrstina Herrick, christina.herrick@unh.edu<br>
		Earth Systems Research Center, EOS<br>
		University of New Hampshire<br>
</ul>

HYPSLIT: https://www.ready.noaa.gov/HYSPLIT.php

<hr>

> [!NOTE]
> This script as written requires ESRI's `arcpy` python module, which is part of the ArcGIS Desktop/ ArcGIS Pro software suite. The script can be modified to run without it, but will result in shapefiiles instead of geodatabase feature classes. This may present a problem with column names and file sizes. [Shapefiles vs Geodatabase FCs](https://blogs.library.duke.edu/data/2015/09/14/shapefiles-vs-geodatabases/)

## How to use this script

<ul>
<li> This is written to work with multiple sites in Amazonia. Data should be organized in a standalone directory called `data`, and there should be a subdirectory for every site.  HYSPLIT trajectories are stored within site subdirectories. Nested subdirectories probably won't work here.</li>

![image](https://github.com/cherrickunh/smoke-hysplit/blob/9bddf7184dbe562e024d57756bde646c9d43daea/readme/dir-struc.JPG) <p>

<li>Trajectory files should end in 8 digits: YYYYMMDD</li>
<li>Each site will result in 5 output feature classes: </li>
<ul>
	<li>All trajectories for a site</li>
	<li>Trajectories during the wet season (Nov-Jun)</li>
	<li>Trajectories during the dry season (Jul-Oct)</li>
	<li>Trajectories during drought years (2006, 2010, and 2018) </li>
	<li>Trajectories during non drought years (from 2001-2020)</li>
</ul>
<li>Users should double-check these parameters</li>
https://github.com/cherrickunh/smoke-hysplit/blob/d2a84201f6da641128a0aed162ab82394fb5b54e/make_shps.py#L16-L21
</ul>
