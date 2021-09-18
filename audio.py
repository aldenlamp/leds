import time
import gradient as gd
import sys
import numpy as np
from scipy.fftpack import fft
import sounddevice as sd


class Audio:
    """ 
    Attributes:

    """

    def __init__(self, bins=50, analysis_window=(.004, 0.5), channels=[0], 
                 device=2, update_interval=30,  gain=20, sample_rate=None):
        
        self.bins = 50
        self.analysis_window = analysis_window
        self.channels = channels
        self.device = device
        self.update_interval = update_interval

        if sample_rate is None:    
            device_info = sd.query_devices(self.device, 'input')
            sample_rate = device_info['default_samplerate']

        self.sample_rate = sample_rate

        self.block_size = int(sample_rate * (interval /1000))


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""

    a = np.array(indata[:, 0])
    
    window = np.hanning(frames)

    d = np.abs(np.fft.rfft(a))
    d *= 20 / len(d)

    group_size = int(len(d) / 100)

    groups = [np.sum(d[i*group_size:((i + 1) * group_size) if i != len(d)/group_size else int(len(d)/group_size)]) for i in range(int(len(d)/group_size))]
    
    current_data = groups

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
            device=device, channels=max(channels),
            samplerate=sample_rate, callback=audio_callback, blocksize=)

        # with stream:
        stream.start()
        while True:
            # update_lights()
            time.sleep(0.001)


    except Exception as e:
        print(e)
        # parser.exit(type(e).__name__ + ': ' + str(e))