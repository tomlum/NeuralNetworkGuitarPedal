# INSTALL > pipenv install
# RUN     > pipenv run python run.py NAME_OF_SAVE_FILE
import argparse
import numpy as np
from keras.models import load_model
from keras.backend import clear_session
import soundfile as sf

from_file = "input.wav"
to_file = "target.wav"

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
model.make_predict_function()


in_data, sample_rate = sf.read(from_file, dtype='float32')

result_data = []

end = in_data.shape[0] - buffer_size

chunks = list(in_data[i:i+buffer_size] for i in range(0, end, buffer_size))
current_data = np.array(chunks)
result_chunks = model.predict(current_data)

for i in range(0, len(result_chunks)):
    result_data.extend(result_chunks[i])

sf.write(to_file, result_data, sample_rate)

print('~' * 80)
print("~~~DEEP WAVE BEND ACTIVE~~~")
print('---press Return to quit---')
print('~' * 80)
input()
