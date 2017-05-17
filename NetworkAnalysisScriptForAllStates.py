#Import system modules
import arcpy
from arcpy import env
import glob

#Needed wildcards and paths
origins = 'D:/ArcPy/arcpy_scripts/jenniferJennings/tempOrigins/*.shp'
destinations = 'D:/ArcPy/arcpy_scripts/jenniferJennings/tempDestinations/*.shp'
layer_name = 'OD Cost Matrix'
output_csv = 'D:/ArcPy/arcpy_scripts/jenniferJennings/'

#Collecting files from directory
fListOrigins = glob.glob(origins)
fListDestinations = glob.glob(destinations)

#Solving OD Matrix for each state in a given year.
for index in range(len(fListOrigins)):
    
    #Creating OD Matrix
    print "Creating OD matrix for file %s"%index
    result_object  = arcpy.MakeODCostMatrixLayer_na(in_network_dataset="D:/ESRI_Data_2013/streetmap_na/data/streets",\
                               out_network_analysis_layer="OD Cost Matrix", \
                               impedance_attribute="Length", default_cutoff="25", \
                               default_number_destinations_to_find="", accumulate_attribute_name="Length", \
                               UTurn_policy="ALLOW_UTURNS",\
                               restriction_attribute_name="'Driving a Passenger Car';'Avoid Service Roads';'Avoid Pedestrian Zones';\
                               'Avoid Walkways';'Avoid Roads for Authorities';'Avoid Private Roads';'Avoid Unpaved Roads';\
                               'Through Traffic Prohibited';'Avoid Express Lanes';'Avoid Carpool Roads'", 
                               hierarchy="USE_HIERARCHY", hierarchy_settings="", \
                               output_path_shape="NO_LINES", time_of_day="")
    
    layer_object = result_object.getOutput(0)
    sublayer_names = arcpy.na.GetNAClassNames(layer_object)
    origins_layer_name = sublayer_names["Origins"]
    destinations_layer_name = sublayer_names["Destinations"]
    linesLayerName = sublayer_names['ODLines']
    
    #Adding Origin and Destination to the OD Matrix
    print "Adding Origin for file %s"%fListOrigins[index]
    arcpy.na.AddLocations(layer_object,  origins_layer_name, fListOrigins[index], 
                          "Name leaid #;TargetDestinationCount # #", "1000 Meters")
    field_mappings = arcpy.na.NAClassFieldMappings(layer_object,  origins_layer_name)
    
    print "Adding Destinations for file %s"%fListDestinations[index]
    arcpy.AddLocations_na(layer_object, destinations_layer_name, fListDestinations[index],
                      field_mappings="Name leaid #", search_tolerance="1000 Meters")
    
    #Solving OD Matrix to obtain Distance metric
    print "Starting Network Analysis for file %s"%index
    arcpy.na.Solve(layer_object)
    print "Completed Network Analysis for file %s"%index
    
    #Saving distance metric to csv
    output_csv = 'D:/ArcPy/arcpy_scripts/jenniferJennings/outputCSV/'+str(fListOrigins[index][62:67])+'.csv'
    fields = ["Name", "Total_Length"]
    headers = ['Origin', 'Destination', 'Length']
    for lyr in arcpy.mapping.ListLayers(layer_object):
        if lyr.name == linesLayerName:
            with open(output_csv, 'w') as f:
                f.write(','.join(headers)+'\n') # csv headers
                with arcpy.da.SearchCursor(lyr, fields) as cursor:
                    print "Successfully created lines searchCursor.\nExporting to " + output_csv
                    for i, row in enumerate(cursor):
                        string = row[0].split('-')
                        string.append(row[1])
                        f.write(','.join([str(r) for r in string])+'\n')
    print "Saved file %s"%(output_csv)