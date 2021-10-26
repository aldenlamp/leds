import board
import neopixel
import audio
import time
import gradient as gd

size = 100
pin = board.D12


led = neopixel.NeoPixel(pin, size, auto_write=False)

# colors (R, B, G)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)
blue_green = (0, 50, 50)
purple = (150 ,50, 0)

colors = [red, purple]

grad = gd.Gradient(colors=colors)



# led[0] = red
# led.show()

 
def call_back(bins, rms):
    # bins = bins * (10 ** 3) / 3 * 2
    for i in range(int(size / 2)):
        color = grad.get_color_at(bins[i], brightness=3, dim=True)
        led[int(size / 2) - i] = color
        led[int(size / 2) + i] = color
    led.show()
    if rms > 0.65:
        grad.step(0.1)
    # print(bins)


song = audio.Audio(call_func=call_back, bins = int(size/2))
song.start_stream()
    # while True:
    #     time.sleep(0.0001)

# print("finish")