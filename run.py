# INSTALL > pipenv install
# RUN     > pipenv run python run.py NAME_OF_SAVE_FILE
import argparse
import numpy as np
import sounddevice as sd
from keras.models import load_model
from keras.backend import clear_session

# Setup CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('save_file',
                    help="save file to use")
args = parser.parse_args()

# Arguments
buffer_size = 512

clear_session()
# Load the model
model = load_model(args.save_file)
model._make_predict_function()

live_array = np.zeros(buffer_size).reshape(1, buffer_size)

def predict(in_data, out_data, frames, t, status):
    global model, live_array

    current_data = np.array([in_data.reshape(buffer_size)])
    result_data = model.predict(current_data)
    result_data = result_data.flatten()
    result_data = result_data.reshape(buffer_size, 1)
    maxx = np.amax(result_data)
    if(maxx > 0.022):
        out_data[:] = result_data
    else:
        out_data[:] = np.zeros(buffer_size).reshape(buffer_size, 1)

with sd.Stream(device=(None, None),
               samplerate=44100, blocksize=buffer_size,
               dtype=None, latency=None,
               channels=1, callback=predict):
    print('~' * 80)
    print("~~~DEEP WAVE BEND ACTIVE~~~")
    print('---press Return to quit---')
    print('~' * 80)
    input()
