#!env python3
import argparse
import socket
default_address = '127.0.0.1'
default_port = 33334

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=default_port)
parser.add_argument('-a', '--address', default=default_address)
parser.add_argument('-r', '--rcvbuf')
parser.add_argument('-s', '--sndbuf')
args = parser.parse_args()

# print params
s = socket.socket()
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, int(args.rcvbuf))
except (AttributeError, TypeError):
    pass
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, int(args.sndbuf))
except (AttributeError, TypeError):
    pass
rcvbuf = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
sndbuf = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print(f'Connect to {args.address}:{args.port}, SNDBUF {sndbuf} RCVBUF {rcvbuf}')

# connect
s.connect((args.address, args.port))
size = 512  # default

while True:
    try:
        line = input(f'{size}> ')
        tmp_n = int(line)
        if tmp_n > 0:
            size = tmp_n
            print(f'new send() size: {size}')
            continue
        else:
            pass
    except EOFError:
        break
    except ValueError:
        pass
    data = b'*' * size
    ret = s.send(data)
    print(f'sent {ret} bytes')
s.close()

