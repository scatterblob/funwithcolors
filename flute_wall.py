import socket
from PIL import Image


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("151.217.40.82", 1234)
    sock.connect(server_address)
    return sock


def send_request(sock, msg, response=False):
    sock.sendall(msg.encode())
    return sock.recv(16) if response else msg


def send_mass_request(array):
    array = get_formatted_pixels(array, 100, 100)
    msg = ''.join(array)
    print(msg)
    print(send_request(s, msg, True))


def send_pixel(x, y, color):
    send_request(s, 'PX {} {} {}\n'.format(x, y, color))


def get_formatted_pixels(pic, offset_x, offset_y):
    formatted = list()
    for p in pic:
        formatted.append('PX {} {} {}\n'.format(p[0] + offset_x, p[1] + offset_y, p[2]))
    return formatted


def get_hex_array(filename):
    im = Image.open(filename)
    rgb_im = im.convert('RGB')
    width, height = im.size
    array = list()
    for y in range(0, height):
        for x in range(0, width):
            array.append((x, y, '%02x%02x%02x' % rgb_im.getpixel((x, y))))
    return array

# while 1:
    # print(send_pixel(1, 1, "FF00E7"))


pixels = get_hex_array(r'C:/Users/fabia/Desktop/taddel_brain.jpg')

s = connect()

send_mass_request(pixels)
