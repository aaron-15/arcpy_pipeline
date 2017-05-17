import arcpy, os
import pandas as pd
arcpy.env.overwriteOutput = True

#Script to get the destination schools for each state
os.mkdir('D:/Arcpy/arcpy_scripts/destination')
poly_25buffer = r'D:\Arcpy\arcpy_scripts\25milesbuffer\25milebuffer.shp'    # The buffer polygons used to clip features

state_name = pd.read_csv('D:/ArcPy/arcpy_scripts/projected_states/state_name.csv')
state_name.drop('Unnamed: 0', axis=1, inplace=True)
state_name.head()

# years = ['98', '99', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']
years = ['98', '99']

for year in years:
    string = '/year_'+str(year)
    os.mkdir('D:/Arcpy/arcpy_scripts/destination/'+string)
    outws = r'D:/Arcpy/arcpy_scripts/destination'+str(string)
    school_points = r'D:/Arcpy/arcpy_scripts/schools/schools'+str(year)+'.shp'  # The school points to be clipped
    states = arcpy.SearchCursor(poly_25buffer)
    count = 0     # Start a counter to name output points
    for state in states: # Loop through individual features of poly_25_buffer"
        name = state_name.loc[count, 'STATE_NAME']
        des_schools = os.path.join(outws, 'destination_'+str(year)+'_'+str(state.STATE_NAME))  # Assemble the output point name and path
        arcpy.Clip_analysis(school_points, state.Shape, des_schools)
        count = count + 1



# Clean up...Not necessary using "with" statement used in arcpy.da module 
del row
del rows

