import socket, time, struct, selectors

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 33335))
serversocket.listen()

class Client:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.fragment = b''
        self.valid = True

    def recv(self):
        try:
            data = self.sock.recv(1024)
            if len(data) == 0:  # 切断された
                print('Connection closed by ' + str(self.addr))
                self.invalidate()
                return
            self.fragment = self.parse(self.fragment + data)
        except BlockingIOError:
            pass

    def parse(self, data):
        try:
            type_ = struct.unpack('!B', data[0:1])[0]
            if type_ == 1:
                id_ = struct.unpack('!H', data[1:3])[0]
                print(f'Join: ID {id_}' )
                return self.parse(data[3:])
            elif type_ == 2:
                chat_len = struct.unpack('!H', data[1:3])[0]
                chat_format = str(chat_len) + 's'
                consumed_len = 3 + chat_len
                chat_text = struct.unpack(chat_format, data[3:consumed_len])[0]
                chat_message = f'Chat: {chat_text.decode()} from {self.addr}\n'
                print(chat_message)
                return self.parse(data[consumed_len:])
            elif type_ == 3:
                print('Leave')
                self.invalidate()
                return b''  # 処理終了
            else:  # 知らないフォーマット。ここでは切断してしまおう
                self.invalidate()
                print('Invalid message format')
                return b''
        except struct.error:  # 長さが想定より短いので今回は処理しない
            return data

    def invalidate(self):
        self.sock.close()
        self.valid = False

    def fileno(self):
        return self.sock

def handle_accept(sock, _mask):
    clientsocket, addr = serversocket.accept()
    clientsocket.setblocking(False)
    new_client = Client(clientsocket, addr)
    clients.append(new_client)
    print('New client ' + str(addr))


clients = []
serversocket.setblocking(False)
sel = selectors.DefaultSelector()
while True:
    try:
        clientsocket, addr = serversocket.accept()
        clientsocket.setblocking(False)
        new_client = Client(clientsocket, addr)
        clients.append(new_client)
        print('New client ' + str(addr))
    except BlockingIOError:  # 何も来ていないだけでエラーではない
        pass

    invalidated = False
    for client in clients:
        try:
            client.recv()
            if not client.valid:
                invalidated = True
        except BlockingIOError:
            pass
    if invalidated:  # 無効になったクライアントをリストから除く
        clients = list(filter(lambda c: c.valid, clients))
    
    time.sleep(0.1)  # CPUを食いつくさないための

