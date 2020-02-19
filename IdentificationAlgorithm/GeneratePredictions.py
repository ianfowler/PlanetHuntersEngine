import numpy as np
from joblib import dump, load
import csv


def generate_predictions(model_directory,transit_directory):
    model = load(model_directory)
    transitsStr = list(csv.reader(open(transit_directory)))[1:]
    transits = np.array(transitsStr).astype(np.float)
    predictions = model.predict(transits)
    return predictions


print(generate_predictions('../../knn.joblib', '../../trial_1/bin_22/transits.csv'))


