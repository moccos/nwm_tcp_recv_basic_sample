import socket, sys, random, struct, time, selectors

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 33335))
my_id = random.randrange(1, 256)
sock.send(struct.pack('!BH', 1, my_id))  # JOIN
print(f'my id is {my_id}')

while True:
  try:
    input_ = input('>> ')
    str_data = input_.encode()
    msg = struct.pack('!BH', 2, len(str_data)) + str_data
    sock.send(msg)
  except (EOFError, KeyboardInterrupt):
    sock.send(struct.pack('!B', 3))  # Leave
    break

time.sleep(0.2)  # 最後のメッセージ送信完了をちょっと待つ(実験用)
sock.close()
print('bye')
