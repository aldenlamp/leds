# leds

https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring

Follow this guide to get it to work

Also there is a way to do FFTs multicore rather than single core, figure that out!

https://realpython.com/python-scipy-fft/

- replace `scipy.fftpack` with `scipy.fft` as this enables multiple cores to be used on the Raspberry Pi for overall speed improvements

- get sister to send me the actual python files that are being used on the raspberry pi, as these ones are not the current ones

# DIY Guide  

## Bill of Materials

- [5V/12A PSU](https://www.amazon.com/gp/product/B074YHN8D1/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&th=1) [~$17]
- [3.5mm Audio Stereo Y Splitter](https://www.amazon.com/gp/product/B00LM0ZGK6/ref=ppx_yo_dt_b_asin_title_o04_s01?ie=UTF8&psc=1) [~$8]
- [USB stereo adapter](https://www.amazon.com/gp/product/B00IRVQ0F8/ref=ppx_yo_dt_b_asin_title_o04_s01?ie=UTF8&psc=1) [~$10]
- 74AHCT125 Quad Level-Shifter
    - [Adafruit](https://www.adafruit.com/product/1787) [$1.50 + shipping]
    - [Amazon](https://www.amazon.com/gp/product/B00XW2L39K/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1) [~$5]

---

So this comes out to be approximately $40 worth of items, considering you already have a breadboard and some cables to connect from the GPIO of the Raspberry Pi. 

And of course a Raspberry Pi, **do not buy at more then MSRP!**

This has been tested on a 3B+, although anything onwards from the first generation should work just fine.



