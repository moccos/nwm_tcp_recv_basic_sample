#!env python3
import argparse
import socket
default_port = 33334

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=default_port)
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
print(f'bind at port {args.port}, SNDBUF {sndbuf} RCVBUF {rcvbuf}')

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', args.port))
s.listen(5)
ss, addr = s.accept()
print(f'accepted connection from {addr}')

size = 500  # default
while True:
    try:
        line = input(f'{size}> ')
        tmp_n = int(line)
        if tmp_n > 0:
            size = tmp_n
            print(f'new recv() size: {size}')
            continue
        else:
            pass
    except EOFError:
        break
    except ValueError:
        pass

    try:
        data = ss.recv(size)
        if len(data) > 0:
            print(f'received {len(data)} bytes')
        else:
            break
    except ConnectionError:
        break
s.close()

