import soundfile as sf
import random
import numpy as np
import matplotlib.pyplot as plt

input_file = "sample_input.wav"
output_file = "algorithm_test.wav"

data, samplerate = sf.read(input_file)

def impulse_response(i):
    L = 1
    W = 200
    w_0 = 1300
    ir = np.sin(i * np.pi / L) * W/np.pi * np.cos(w_0 * (i * L/2)) * np.sin(W * (i - L/2) * 0.5) / (0.5 * W * (i - L/2))
    if i < 0 or i > L:
        return 0
    else:
        return ir/(1000 * 200);

class ring_buffer:
    def __init__(self, capacity: int):
        self.index = 0
        self.capacity = capacity
        self.head = [0.0] * capacity

    def __repr__(self):
        return f"ring_buffer(index={self.index}, capacity={self.capacity})"

def create_ring_buffer(capacity: int) -> ring_buffer:
    return ring_buffer(capacity)

def FIR_bandpass_filter(sample, buffer):
    buffer.head[buffer.index] = sample
    buffer.index += 1
    if buffer.index == buffer.capacity:
        buffer.index = 0
    filtered_sample = 0
    sum_index = buffer.index

    for i in range(buffer.capacity):
        if sum_index > 0:
            sum_index -= 1
        else:
            sum_index = buffer.capacity - 1
        filtered_sample += impulse_response(i) * buffer.head[sum_index]

    return filtered_sample

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
    buf = ring_buffer(5);
    
    for channel in samples.T:
        modified_channel = []
        for sample in channel:
            modified_channel.append(FIR_bandpass_filter(sample, buf))
            
        modified_samples.append(modified_channel)
    
    return np.array(modified_samples).T

modified_data = processor(data)

print("Success.\n")

sf.write(output_file, modified_data, samplerate)

N = len(data)
N_mod = len(modified_data)
fft_data = np.fft.fft(data)
fft_data_mod = np.fft.fft(modified_data)

magnitude = np.abs(fft_data)
magnitude_mod = np.abs(fft_data_mod)

freqs = np.fft.fftshift(np.fft.fftfreq(N, 1/samplerate))

plt.plot(freqs, magnitude, label = "Original")
plt.plot(freqs, magnitude_mod, label = "Processed")
plt.title("Fourier Transforms")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.legend()
plt.show()
