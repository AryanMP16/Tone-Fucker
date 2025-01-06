import soundfile as sf
import random
import numpy as np
import matplotlib.pyplot as plt

input_file = "sample_input.wav"
output_file = "algorithm_test.wav"

data, samplerate = sf.read(input_file)

def algorithm(sample, gain, thresh):
    noise = random.uniform(-thresh * 0.1, thresh * 0.1)
    fuzzed_sample = np.tanh(gain * sample) + noise
    
    if fuzzed_sample > 1:
        return 1.0
    elif fuzzed_sample < -1:
        return -1.0
    else:
        return fuzzed_sample
    
def processor(samples):
    modified_samples = []
    
    for channel in samples.T:
        modified_channel = []
        for sample in channel:
            modified_channel.append(algorithm(sample, 20.0, 0.1))
            
        modified_samples.append(modified_channel)
    
    return np.array(modified_samples).T

modified_data = processor(data)

print("Success.\n")

sf.write(output_file, modified_data, samplerate)
