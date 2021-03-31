# ======== main library ========
import socket
import framebuf
import time

DEFAULT_PORT = 10086
CMD_WRITE_SCREEN = 0x00
CMD_SET_BACKLIGHT = 0x01
CMD_PING = 0x02

class LCD12864(framebuf.FrameBuffer):
    def __init__(self, address=None):
        self.__last_show_time = 0
        self.buffer = bytearray(1024)
        self.address = address
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sender.settimeout(0.5)
        super().__init__(self.buffer, 128, 64, framebuf.MONO_VLSB)
        if self.address == None:
            try:
                ip = socket.gethostbyname(socket.gethostname())
                tmp_ip = ip.split(".")
                tmp_ip[3] = "255"
                b_ip = ".".join(tmp_ip)
                ip_data = ip.encode("utf-8")
                self.__send(CMD_PING, ip_data, (b_ip, DEFAULT_PORT))
                _, client = self.sender.recvfrom(2048)
                self.address = client
            except:
                raise Exception("Could not find device, please set address.")
    
    def __send(self, cmd, data=b'', address=None):
        if address == None:
            address = self.address
        self.sender.sendto(bytearray([cmd]) + data, address)

    def show(self, limit_speed = True):
        now = time.time_ns()
        if (now - self.__last_show_time) > 50_000_000 or (not limit_speed):
            self.__send(CMD_WRITE_SCREEN, self.buffer)
            self.__last_show_time = now

    def backlight(self, value):
        ''' backlight from 0 to 100, [0, 100]'''
        level = int(1023 * value / 100)
        self.__send(CMD_SET_BACKLIGHT, level.to_bytes(2, 'big'))
