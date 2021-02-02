import socket

host="127.0.0.1"
port=2121

with socket.socket() as soket:
    soket.bind((host,port))
    soket.listen()
    conn,addr=soket.accept()
    with conn:
        print("bağlantı yapıldı",addr)
        while True:
            data=conn.recv(1024) #1024 byte bilgi alınmasını sağlıyoruz
            if not data:
                break
            conn.sendall(data)


