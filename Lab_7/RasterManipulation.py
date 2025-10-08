import arcpy

#Composite raster image
source = r"D:\COLLEGE\GEOG_676\LABS\Lab7"
band1 = arcpy.sa.Raster(source + r"\band1.TIF")
band2 = arcpy.sa.Raster(source + r"\band2.TIF")
band3 = arcpy.sa.Raster(source + r"\band3.TIF")
band4 = arcpy.sa.Raster(source + r"\band4.TIF")
combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\combinedimg.TIF")

#Hillshade
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
arcpy.ddd.HillShade(source + r"\dem.tif", source + r"\outputHillshade.tif", azimuth, altitude, shadows, z_factor)

#Slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(source + r"\dem.tif", source + r"\outputSlope.tif", output_measurement, z_factor)

print("Success!")