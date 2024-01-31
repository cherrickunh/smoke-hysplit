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
> This script as written requires ESRI's `arcpy` python module, which is part of the ArcGIS Desktop/ ArcGIS Pro software suite. The script can be modified to run without it, but will result in shapefiiles instead of geodatabase feature classes.

## How to use this script

This is written to work with multiple sites in Amazonia. Data should be organized in a standalone directory, and there should be a subdirectory for every site.  HYSPLIT trajectories are stored within site subdirectories. Nested subdirectories probably won't work.

![image](https://github.com/cherrickunh/smoke-hysplit/assets/12398236/024b7fce-8316-48c5-9128-f6633beeaa16) <p>

