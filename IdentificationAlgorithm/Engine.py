import os
import csv
from TransitGenerator import row_to_lightcurve
from ParameterStepper import gen_param_csv
from GeneratePredictions import save_predictions


# Go through files and generate transits

FOLDER_NAME = "trial_1"
SAMPLE_LENGTH = 3197
TRANSIT_TIME_MINUTES = 30

# From the star temperature array, step through the stellar parameters we will feed into the fake transits. 
gen_param_csv(folder_name=FOLDER_NAME, length=SAMPLE_LENGTH, transit_time_minutes=TRANSIT_TIME_MINUTES)

HEAD = ["FLUX.{}".format(i) for i in range(1,SAMPLE_LENGTH+1)]

for subdir, dirs, files in os.walk("./{}/".format(FOLDER_NAME)):
    for d in dirs:
        with open('{}{}/parameters.csv'.format(subdir,d)) as csvfile:
            arr = list(csv.reader(csvfile))
            
            lc_arr = [HEAD]
            
            header = arr[0]
            
            for i in range(1,len(arr)):
                p = [float(a) for a in arr[i]] # Get params in float form
                lc = row_to_lightcurve(header, p) # Generate lightcurve
                lc_arr.append(lc)
                
            with open("{}{}/transits.csv".format(subdir,d),"w+") as my_csv:
                csvWriter = csv.writer(my_csv,delimiter=',')
                csvWriter.writerows(lc_arr)
                
            save_predictions('../../knn.joblib', '{}{}/transits.csv'.format(subdir,d), '{}{}/predictions.csv'.format(subdir,d))
        
        print("finished " + d)

