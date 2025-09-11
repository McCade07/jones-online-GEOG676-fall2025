import arcpy
arcpy.env.workspace = r"C:/COLLEGE/GEOG_676/LABS/Lab4/Workspace"
arcpy.CreateFileGDB_management(arcpy.env.workspace, "Lab4.gdb")
folder_path = r"C:/COLLEGE/GEOG_676/LABS/Lab4/Workspace/"
gdb_path = folder_path + "Lab4.gdb"

csv_path = folder_path + "garages.csv"
garage_layer_name = "Garage_Points"
garages = arcpy.MakeXYEventLayer_management(csv_path, "X", "Y", garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + "\\" + garage_layer_name

#open campus gdb, copy building feature to my gdb
campus = r"C:/COLLEGE/GEOG_676/LABS/Lab4/Campus.gdb"
buildings_campus = campus + "/Structures"
buildings = gdb_path + "\\" + "Buildings"

arcpy.Copy_management(buildings_campus, buildings)

#re-projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + "/Garage_Points_reprojected", spatial_ref)

#Buffer the garages
buffer_distance = input("Enter the desired buffer distance in meters: ")
garageBuffered = arcpy.Buffer_analysis(gdb_path + "/Garage_Points_reprojected", gdb_path + "/Garage_Points_buffered", buffer_distance)

#Intersect our buffer with our buildings
arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + "/Garage_Building_intersection", "ALL")

#Create intersect csv file
arcpy.TableToTable_conversion(gdb_path + "/Garage_Building_intersection.dbf", r"C:/COLLEGE/GEOG_676/LABS/Lab4", "lab4intersection.csv")