import board
import neopixel
import audio
import time
import gradient as gd

use_board_in = input("use board? [y/n]:")

single_strip = not (use_board_in == "y" or use_board_in == "Y")

# size = 100
width = 100 if single_strip else 30
height = 16
pin = board.D12


led = neopixel.NeoPixel(pin, width * height, auto_write=False)

# colors (R, B, G)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)
blue_green = (0, 50, 50)
purple = (150 ,50, 0)

colors = [red, purple]
test_color = red

grad = gd.Gradient(colors=colors)



# led[0] = red
# led.show()

 
def call_back(bins, rms):
    if single_strip:
        single_strip_callback(bins, rms)

    else:
        board_callback(bins, rms)

    # bins = bins * (10 ** 3) / 3 * 2

    # print(bins)

def board_callback(bins, rms):
    for i in range(int(width/2)):
        a = int(width/2)
        b = int(width/2) - i - 1
        for j in range(bins[i] * height):
            led[position_at(a, j)] = test_color
            led[position_at(b, j)] = test_color
    led.show()


def single_strip_callback(bins, rms):
    for i in range(int(width / 2)):
        color = grad.get_color_at(bins[i], brightness=3, dim=True)
        led[int(width / 2) - i] = color
        led[int(width / 2) + i] = color
    led.show()
    if rms > 0.65:
        grad.step(0.1)


def position_at(x, y):
        if y % 2 != 0:
            return (width * height - 1) - width * y - (width - x - 1)
        else:
            return (width * height - 1) - width * y - x


song = audio.Audio(call_func=call_back, bins = int(width/2))
song.start_stream()
    # while True:
    #     time.sleep(0.0001)

# print("finish")