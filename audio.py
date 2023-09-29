import time
import gradient as gd
import sys
import math
import numpy as np
# from scipy.fftpack import fft
from scipy.fft import fft
import sounddevice as sd

# import board
# import neopixel
# size = 100
# pin = board.D12

# led = neopixel.NeoPixel(pin, size, auto_write=False)
# # colors (R, B, G)
# red = (255, 0, 0)
# blue = (0, 255, 0)
# green = (0, 0, 255)
# # purple = (150, 50, 0)

# colors = [red, blue, green]

# grad = gd.Gradient(colors=colors)



class Audio:
    """ 
    Attributes:
        bins: The number of bins to group the sound data into
        analysis_window: The proportions of the frequency range to analyze
        channels: The channels to input from (currently one channel allowed) ????
        device: The sound input device
        update_interval: How frequently to update the callback (in millis)
        sample_rate: Audio sample rate (defaults based on device default)
        block_size: The number of frames in each interval
        last_bins: This stores the lsat rows of bins for bluring
        call_func: the function to call from main with bins
        GAIN: The gain for the audio samples
        HORIZONTAL_BLUR_FRAME: The criteria for each pixel in the 
            horizontal blur
        BACK_BLUR_FRAME: The criteria for each pixel when bluring with the
            previous samples
    """

    HORIZONTAL_BLUR_FRAME = np.array([0.1, 0.2, 0.4, 0.2, 0.1])
    
    # HORIZONTAL_BLUR_FRAME = np.array([0.1, 0.1, 0.1, 0.1, 0.1])
    # HORIZONTAL_BLUR_FRAME = np.array([0.5, 0.1, 0.1, .15, 0.2, 0.15, 0.1, 0.1, 0.5])
    # HORIZONTAL_BLUR_FRAME = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, .1, 0.1, 0.1, 0.1, 0.1, 0.1])
    
    # HORIZONTAL_BLUR_FRAME = np.array([0.1, 0.15, .15, 0.2, 0.15, 0.15, 0.1])

    # BACK_BLUR_FRAME = np.array([0.3, 0.2, 0.15, 0.15, 0.1, 0.05, 0.05])
    
    BACK_BLUR_FRAME = np.array([0.4, 0.2, 0.15, 0.1, 0.1, 0.05])
    # BACK_BLUR_FRAME = np.array([0.5, 0.3, 0.15, 0.1, 0.1, 0.05])
    # BACK_BLUR_FRAME = np.array([0.6, 0.3, 0.15, 0.15])
    GAIN = 2.5
    DROP_OFF = 5

    def __init__(self, call_func, bins=50, analysis_window=(.004, 0.4), channels=1, 
                 device=2, update_interval=30,  gain=20, sample_rate=None):
        
        self.call_func = call_func

        self.bins = bins
        self.analysis_window = analysis_window
        self.channels = channels
        self.device = device
        self.update_interval = update_interval

        if sample_rate is None:    
            device_info = sd.query_devices(self.device, 'input')
            sample_rate = device_info['default_samplerate']

        self.sample_rate = int(sample_rate)

        self.block_size = int(sample_rate * (self.update_interval /1000)) 
        self.last_bins = []


    def blur_sideways(self, bins):
        blur_size = int(len(self.HORIZONTAL_BLUR_FRAME) / 2)
        blurred = []

        for i in range(len(bins)):

            start = max(i - blur_size, 0)
            last = min(i + blur_size, len(bins))

            new_value = 0
            blur_sum = 0
            for j in range(start, last):
                blur_index = (blur_size - i) + j
                new_value += self.HORIZONTAL_BLUR_FRAME[blur_index] * bins[i]
                blur_sum += self.HORIZONTAL_BLUR_FRAME[blur_index]
            blurred.append(new_value / blur_sum)

        for i in range(len(bins)):
            bins[i] = blurred[i]

    def blur_backward(self, bins):
        blur_size = len(self.BACK_BLUR_FRAME)
        blurred = []
        for i in range(len(bins)):
            blur_sum = 0
            value = 0
            for j in range(len(self.last_bins)):
                if j == 0:
                    value += self.BACK_BLUR_FRAME[j] * bins[i]
                elif j == 1:
                    greater = max(self.last_bins[j - 1][i], bins[i])
                    value += self.BACK_BLUR_FRAME[j] * greater
                else:
                    value += self.BACK_BLUR_FRAME[j] * self.last_bins[j - 1][i]
                blur_sum += self.BACK_BLUR_FRAME[j]
            
            if blur_sum == 0:
                blurred = bins
                break
            blurred.append(value / blur_sum)
        
    
        for i in range(len(bins)):
            bins[i] = blurred[i]
        
        self.last_bins.insert(0, blurred)
        if len(self.last_bins) >= blur_size - 1:
            self.last_bins = self.last_bins[:-1]


    def get_bins(self, sample):

        analysis_start = int(self.analysis_window[0] * len(sample))
        analysis_end = int(self.analysis_window[1] * len(sample))

        start = math.log(analysis_start, 2)
        end = math.log(analysis_end, 2)
        div_size = (end - start) / self.bins

        bins = []
        bin_count = [0 for i in range(self.bins + 1)]

        value = 0
        curr_bin = 0
        for i in range(analysis_start, analysis_end):
            window = (math.log(i, 2) - start) / div_size
            bin_count[curr_bin] += 1
            if window >= curr_bin:
                curr_bin += 1
                bins.append(value * value)
                value = 0
            
            value += sample[i]
        for i in range(len(bins)):
            bins[i] /= (bin_count[i] ** (1/self.DROP_OFF))
        # print(bin_count)
        return np.array(bins)
        

    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""

        a = np.array(indata[:, 0])
        window = np.hanning(frames)

        d = np.abs(np.fft.rfft(a))
        d *= (self.GAIN / len(d))

        bins = self.get_bins(d)
        # print("Num Bins: {}".format(len(bins)))
        self.blur_sideways(bins)
        self.blur_backward(bins)

        rms = np.sqrt(np.mean(a**2))

        self.call_func(bins, rms)

        # for i in range(len(bins)):
        #     led[i] = grad.get_color_at(bins[i])
        # led.show()


        # group_size = int(len(d) / 100)

        # groups = [np.sum(d[i*group_size:((i + 1) * group_size) if i != len(d)/group_size else int(len(d)/group_size)]) for i in range(int(len(d)/group_size))]
        
        # current_data = groups

        # if current_data != last_data:
        #     # print([grad.get_color_at(current_data[i]) for i in range(size)])
        # for i in range(size):
        #     # print(grad.get_color_at(current_data[i]))
        #     led[i] = grad.get_color_at(current_data[i])
        # led.show()
        # last_data = current_data

    def start_stream(self): 
        try:
            stream = sd.InputStream(
                device=self.device, channels=1, 
                samplerate=self.sample_rate, callback=self.audio_callback, 
                blocksize=self.block_size)

            # with stream:
            stream.start()
            while True:
                # update_lights()
                time.sleep(0.001)


        except Exception as e:
            print(e)


# if __name__ == "__main__":
    # asdf = Audio()
    # asdf.start_stream()
