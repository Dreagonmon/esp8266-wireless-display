import sys, os, time
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(CURRENT_PATH, "..", "lib")))
from LCD12864Remote import LCD12864
from framebuf import FrameBuffer, MONO_HLSB
from pbm import read_image

def main():
    screen = LCD12864(("192.168.31.203", 10086))
    image_file = os.path.join(CURRENT_PATH, "test.pbm")
    with open(image_file, "rb") as f:
        w, h, type, data, comment = read_image(f)
    image = FrameBuffer(data, w, h, MONO_HLSB)
    screen.blit(image, (128-w)//2, 0)
    screen.show()

if __name__ == "__main__":
    main()