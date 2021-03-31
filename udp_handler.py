from micropython import const
import socket,gc

CMD_WRITE_SCREEN = const(0x00)
CMD_SET_BACKLIGHT = const(0x01)
CMD_PING = const(0x02)

def _handler(screen, screen_backlight, console, data, client, usoc):
    gc.collect()
    cmd = data[0]
    if cmd == CMD_WRITE_SCREEN:
        screen.buffer = data[1:1025]
        screen.show()
    elif cmd == CMD_SET_BACKLIGHT:
        level = int.from_bytes(data[1:3], 'big')
        screen_backlight.duty(level)
    elif cmd == CMD_PING:
        usoc.sendto(data, client)

def main_loop(screen, screen_backlight, console):
    usoc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    usoc.bind(('0.0.0.0',10086))
    while True:
        data, client = usoc.recvfrom(2048)
        _handler(screen, screen_backlight, console, data, client, usoc)
    usoc.close()