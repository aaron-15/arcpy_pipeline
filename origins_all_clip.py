import arcpy, os
import pandas as pd
arcpy.env.overwriteOutput = True

#Script to get the origin schools for each state
us_states = r'D:\ArcPy\arcpy_scripts\projected_states\projected_States.shp' #The states polygons used to clip schools

#Creating variable to read statename and index
state_name = pd.read_csv('D:/ArcPy/arcpy_scripts/projected_states/state_name.csv')
state_name.drop('Unnamed: 0', axis=1, inplace=True)

years = ['98', '99', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']

for year in years:	#looping over the required years
    string = '/year_'+str(year)
    os.mkdir('D:/Arcpy/arcpy_scripts/origins/'+string) #Creating new directory for a new year
    outws = r'D:/Arcpy/arcpy_scripts/origins'+str(string) #The output directory of the clipped origin file
    school_points = r'D:/Arcpy/arcpy_scripts/schools/schools'+str(year)+'.shp'  # The school points to be clipped
    states = arcpy.SearchCursor(us_states)
    count = 0     # Start a counter to name output points
    for state in states: # Loop through individual features of "us_states"
        name = state_name.loc[count, 'STATE_NAME']	# reading the state file name
        ori_schools = os.path.join(outws, 'origin_'+str(year)+'_'+str(name))  # Assemble the output point name and path
        arcpy.Clip_analysis(school_points, state.Shape, ori_schools) #Clipping the data
        count = count + 1

# Clean up...Not necessary using "with" statement used in arcpy.da module 

del state
del states
