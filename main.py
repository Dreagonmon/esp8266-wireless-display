import app
import config

# ========
# setup network
import network
wifi_sta = network.WLAN(network.STA_IF)
wifi_ap = network.WLAN(network.AP_IF)
# set wifi config
wifi_sta.active(True)
wifi_sta.connect(config.wifi_ssid, config.wifi_password)
# set ap
wifi_ap.active(True)
wifi_ap.config(essid='MicroDragon')
wifi_ap.config(password='12345678')
wifi_ap.config(authmode=network.AUTH_WPA_WPA2_PSK)
import webrepl
webrepl.stop()
def ip():
    print(wifi_sta.ifconfig()[0])

# ========
# setup screen
from st7565 import ST7565
from machine import Pin, SPI
_cs = Pin(5, Pin.OUT)
_rst = Pin(4, Pin.OUT)
_rs = Pin(2, Pin.OUT)
# _sck = Pin(14, Pin.OUT)
# _mosi = Pin(13, Pin.OUT)
_spi = SPI(1, baudrate=10000000, polarity=1, phase=1)
screen = ST7565(128, 64, _spi, _rs, _cs, _rst)
# from ubmfont import FontDrawUnicode
from bmfont import FontDrawAscii
from framebuf_console import Console
from machine import PWM
backlight = PWM(Pin(0), freq=1000, duty=512) # duty from 0 to 1024
console = Console(screen, 128, 64, font_draw=FontDrawAscii(), color=1, display_update_fun=lambda:screen.show())
# ========
# setup finished

# ========
# main programs
import udp_handler
from utime import sleep
console.log('wait wifi...')
while not wifi_sta.isconnected():
    console.log('.')
    sleep(1)
    pass
console.log('wifi connected:')
console.log(wifi_sta.ifconfig()[0])
console.log(wifi_ap.ifconfig()[0])

udp_handler.main_loop(screen, backlight, console)
