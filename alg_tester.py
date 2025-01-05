import soundfile as sf
import random
import numpy as np
import matplotlib.pyplot as plt

input_file = "sample_input.wav"
output_file = "algorithm_test.wav"

data, samplerate = sf.read(input_file)

def algorithm(samples, gain, thresh):
    # Create an empty list to store modified samples
    modified_samples = []

    for channel in samples.T:  # Iterate over each channel (transpose the array)
        modified_channel = []
        for sample in channel:
            ############################################################
            ##########################actual alg########################
            ############################################################
            noise = random.uniform(-thresh * 0.1, thresh * 0.1)
            fuzzed_sample = np.tanh(gain * sample) + noise
            
            if fuzzed_sample > 1:
                modified_channel.append(1)
            elif fuzzed_sample < -1:
                modified_channel.append(-1)
            else:
                modified_channel.append(fuzzed_sample)
            ############################################################
            ############################################################
            ############################################################
        modified_samples.append(modified_channel)
    
    return np.array(modified_samples).T

modified_data = algorithm(data, 20.0, 0.1)
# time  = np.linspace(0, 1, samplerate)

fft_modified_data = np.fft.fft(modified_data[:samplerate, 0])
fft_data = np.fft.fft(data[:samplerate, 0])
frequencies = np.fft.fftfreq(samplerate, 1 / samplerate)

print("Success.\n")

plt.plot(frequencies[:samplerate], fft_modified_data)
plt.plot(frequencies[:samplerate], fft_modified_data)
plt.show()

sf.write(output_file, modified_data, samplerate)