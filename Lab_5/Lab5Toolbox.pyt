# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GarageBuildingIntersection]


class GarageBuildingIntersection:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Garage Intersect Tool"
        self.description = "Make sure to include .gdb in the GDB Name parameter"

    def getParameterInfo(self):
        """Define the tool parameters."""
        param0 = arcpy.Parameter(
            displayName="Location to Create Geodatabase", name="GDBFolder", datatype="DEFolder", parameterType="Required", direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GDB Name (Make sure to include .gdb at the end)", name="GDBName", datatype="GPString", parameterType="Required", direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File", name="GarageCSVFile", parameterType="Required", datatype="DEFile", direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name (No spaces)", name="GarageLayerName", datatype="GPString", parameterType="Required", direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB", name="CampusGDB", datatype="DEType", parameterType="Required", direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance", name="BufferDistance", datatype="GPDouble", parameterType="Required", direction="Input"
        )
        param6 = arcpy.Parameter(
            displayName="Folder for Intersect Output Table", name="OutputTableFolder", datatype="DEFolder", parameterType="Required", direction="Input"
        )
        params = [param0, param1, param2, param3, param4, param5, param6]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        folder_path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText
        gdb_path = folder_path + '\\' + gdb_name
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        csv_path = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText
        garages = arcpy.MakeXYEventLayer_management(csv_path, "X", "Y", garage_layer_name)

        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = gdb_path + '\\' + garage_layer_name

        #open campus gdb, copy building feature to my gdb
        campus = parameters[4].valueAsText
        buildings_campus = campus + "\Structures"
        buildings = gdb_path + "\Buildings"

        arcpy.Copy_management(buildings_campus, buildings)

        #re-projection
        spatial_ref = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garage_points, gdb_path + "\Garage_Points_reprojected", spatial_ref)

        buffer_distance = int(parameters[5].value)
        garage_buffered = arcpy.Buffer_analysis(gdb_path + "\Garage_Points_Reprojected", gdb_path + "\Garage_Points_buffered", buffer_distance)

        #Intersect our buffer with our buildings
        arcpy.Intersect_analysis([garage_buffered, buildings], gdb_path + "\Garage_Building_intersection", "ALL")

        
        #Create intersect csv file
        arcpy.ExportTable_conversion(gdb_path + "\\" + "Garage_Building_intersection.dbf", parameters[6].valueAsText + "\Intersection.csv")

        return None
