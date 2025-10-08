# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Graduated Color Map Tool"
        self.description = "Create a graduated color map based on a chosen attribute of a layer."

    def getParameterInfo(self):
        """Define the tool parameters."""

        #Get ArcGIS Project Name
        param0 = arcpy.Parameter(
            displayName="ArcGIS Project Name",
            name="projectname",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        #Get the layer that is to be classified
        param1 = arcpy.Parameter(
            displayName="Layer to be Classified",
            name="layertoclassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )

        #Output Folder
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="outputfolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        params = [param0, param1, param2, param3]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""

        #Define the progressor variables
        readTime = 3    #the time for users to read the progress
        start = 0       #beginning position of the progressor
        max = 100       #end position of the progressor
        step = 33       #interval at which the progressor moves

        #Set up progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime) #pause the execution for three seconds
        arcpy.AddMessage("Validating Project File...")

        #Project File
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        #Gets the first instance of a map from the project file
        campus = project.listMaps('Map')[0]

        #Increment progressor
        arcpy.SetProgressorPosition(start + step) 
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        #Loop through the layers of the map
        for layer in campus.listLayers():
            if layer.isFeatureLayer:
                symbology = layer.symbology
                
                if hasattr(symbology, 'renderer'):

                    if layer.name == parameters[1].valueAsText:

                        #Increment progressor
                        arcpy.SetProgressorPosition(start + step*2)
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        #Update the copy's renderer to "Graduated Colors Renderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        #tell arcpy which field we want to base our map off of
                        symbology.renderer.classificationField = "Shape_Area"

                        #Set how many classes we will have for the map
                        symbology.renderer.breakCount = 5

                        #set color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 classes)')[0]

                        #Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                    
                    else:
                        print("No feature layers found")

        #Increment Progressor
        arcpy.SetProgressorPosition(start + step*3)
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
