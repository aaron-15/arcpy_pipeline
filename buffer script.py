#This script reads the positions of rhino sightings from a CSV file and writes them as polylines to a new shapefile

#import modules and set up workspace
import arcpy
workspace = "D:/ArcPy/arcpy_scripts"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

#create a 25 mile buffer for each of the states
states = workspace+"/projected_states/projected_States.shp"
statesBuffer = workspace+"/buffer_output"
distanceField = "Distance"
sideType = "FULL"
endType = "ROUND"
dissolveType = "NONE"
arcpy.Buffer_analysis(states, statesBuffer, "25 Miles", sideType, endType, dissolveType)

