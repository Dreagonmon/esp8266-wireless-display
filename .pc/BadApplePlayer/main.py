import sys, os, time
from PIL import Image
from pygame import mixer
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(CURRENT_PATH, "..", "lib")))
from LCD12864Remote import LCD12864
DIR = os.path.join(CURRENT_PATH, 'BadApple-fps-16')
# DIR = os.path.join(CURRENT_PATH, 'BadApple-fps-8')
BASE_FILE_NAME = 'BadApple{:04d}.png'
MP3_FILE = os.path.join(CURRENT_PATH, 'BadApple.mp3')

# convert image bytes for ssd1306.
def img_mono_vlsb(img,invert=False):
    img = img.convert("1")
    # ensure image`s height (h%8==0)
    if not img.height%8 == 0:
        nh = img.height//8 + 1
        nimg = Image.new("1",(img.width,nh))
        img = nimg.paste(img,(0,0,img.width,img.height))
        img.load()
    # the number of lines
    rows = img.height//8
    # buffer
    buf = img.getdata()
    data = []
    for row in range(rows):
        for col in range(img.width):
            byt = 0x00
            for bit in range(7,-1,-1):
                # parse byte
                y = row*8 + bit
                pos = y*img.width + col
                # black as image data
                if (buf[pos]==0) ^ invert:
                    byt = byt | 0x01
                if bit > 0:
                    # not last bit
                    byt = byt << 1
            data.append(byt)
    return bytearray(data)

def loadImage(index):
    path = os.path.join(DIR, BASE_FILE_NAME.format(index))
    img = Image.open(path)
    data = img_mono_vlsb(img,invert=True)
    return data


if __name__ == '__main__':
    mixer.init()
    mixer.music.load(MP3_FILE)
    address = ('192.168.31.203', 10086)
    screen = LCD12864(address)
    # screen = LCD12864()
    screen.backlight(5)
    last_time = 0
    mixer.music.play()
    for i in range(1,3509):
    # for i in range(1,1756):
        current_time = time.time_ns()
        while (current_time - last_time < 62_000_000):
        # while (current_time - last_time < 0.125):
            current_time = time.time_ns()
        last_time = current_time
        screen.buffer[:1024] = loadImage(i)[:1024]
        screen.show()
    mixer.music.stop()