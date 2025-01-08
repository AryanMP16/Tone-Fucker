import soundfile as sf
import random
import numpy as np
import matplotlib.pyplot as plt

input_file = "sample_input.wav"
output_file = "algorithm_test.wav"

data, samplerate = sf.read(input_file)

def impulse_response(i):
    L = 3
    W = 200 * 2 * np.pi
    w_0 = 1300 * 2 * np.pi
    ir = np.sin(i * np.pi / L) * W/np.pi * np.cos(w_0 * (i - L/2)) * np.sinc(W * (i - L/2) * 0.5)
    if i < 0 or i > L:
        return 0
    else:
        return ir/60000;

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
    buf = ring_buffer(3);
    
    for channel in samples.T:
        modified_channel = []
        for sample in channel:
            modified_channel.append(FIR_bandpass_filter(sample, buf))
            
        modified_samples.append(modified_channel)
    
    return np.array(modified_samples).T

modified_data = processor(data)

print("Success.\n")

sf.write(output_file, modified_data, samplerate)

N_mod = len(modified_data)
fft_data = np.fft.fft(data)
fft_data_mod = np.fft.fft(modified_data)

N = len(data)
h_FIR = []
for i in range(N):
    h_FIR.append(impulse_response(i * 1/samplerate))
fft_h_FIR = np.fft.fft(h_FIR)

freqs = np.fft.fftfreq(N, 1/samplerate)

plt.plot(freqs, fft_data[:, 1], label = "Original")
plt.plot(freqs, fft_data_mod[:, 1], label = "Processed")
#plt.plot(freqs, np.fft.fft(h_FIR), label = "h_FIR")
plt.title("Fourier Transforms")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.legend()
plt.show()
