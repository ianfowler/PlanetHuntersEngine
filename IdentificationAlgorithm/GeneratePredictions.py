import numpy as np
import pandas as pd
from joblib import dump, load
import csv


def generate_predictions(model_directory,transit_directory):
    model = load(model_directory)
    transitsStr = list(csv.reader(open(transit_directory)))[1:]
    transits = np.array(transitsStr).astype(np.float)
    predictions = model.predict(transits)
    return predictions

def save_predictions(model_directory,transit_directory,new_file_directory):
    predictions = generate_predictions(model_directory,transit_directory)
    df = pd.DataFrame({"predictions":predictions})
    df.to_csv(new_file_directory)
