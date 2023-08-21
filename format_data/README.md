Scripts to process datasets to match resolution of AVHRR reflectance dataset.

|            Variable               |	Spatial resolution (degrees) |	Type of regridding	| Native temporal resolution       |	    Script for temporal averaging	   |         Script for spatial regrid        |
|-----------------------------------|------------------------------|----------------------|----------------------------------|---------------------------------------|------------------------------------------|
|Filtered Remote Sensing Reflectance|	          	0.1 	           |        N/A	          |            Monthly 	             |                N/A                    | Mask_Rrs_data_by_sea_ice_fraction.ipynb* | 
|         Sea ice extent 	          |           	0.05             |       	BL	          |            Daily 	               |          timeavg_function.py          |            regrid_function.py            |
|     Sea surface temperature 	    |           	0.05             |      	BL	          |            Daily                 |        	timeavg_function.py          |           	regrid_function.py            |
|        Sea level anomaly 	        |            	0.25 	           |        NN	          |            Monthly 	             |                  N/A	                 |          spatial_only_regrid.py          |
|      Wind speed and stress 	      |           	0.25 	           |        NN            |          	6 hourly 	             |timeavg_function.py/timestd_function.py|            regrid_function.py            |
|               PAR                 |           	0.85             |       	NN	          |Monthly mean of daily accumulation| 	                N/A	                 |       spatial_only_regrid_YEARLY.py      |
|         Mix layer depth 	        |             0.85 	           |        NN	          |            Monthly 	             |                  N/A	                 |          spatial_only_regrid.py          |
![image](https://github.com/E-Duncan/coccolithophore_analysis/assets/57486822/96bd6fac-d153-4230-8f7b-ebf504e1bedf)

*Note Mask_Rrs_data_by_sea_ice_fraction.ipynb is used to remove areas from reflectance data filled with sea ice due to interference with signal in polar provinces.
Data is then sectioned into Longhurst province dataframes for analysis using make_dataframe_function.py in make_province_loop.py.
