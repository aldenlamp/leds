
# print(sd.query_devices())

size = 100
pin = board.D12
# print(pin)

led = neopixel.NeoPixel(pin, size, auto_write=False)

# colors (R, B, G)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)
# purple = (150, 50, 0)

colors = [red, blue, green]

grad = gd.Gradient(colors=colors)

led[0] = red
led.show()